# 独立实现
import json
from pathlib import Path
from typing import List
from collections import Counter

from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.matcher import Matcher


class NerdleHelp:
    def __init__(self) -> None:
        """初始化, 从多个文件读取等式列表"""
        plugin_path = Path(__file__).parent
        equals_dir = plugin_path / "equals"

        self.equals: List[str] = []

        # 使用glob模式匹配所有dic-*.json文件
        for file_path in equals_dir.glob("dic-*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.equals.extend(data)
                    else:
                        print(f"警告: {file_path.name} 文件格式不是列表，跳过")
            except Exception as e:
                print(f"加载 {file_path.name} 时出错: {e}")

        print(f"成功从 {len(list(equals_dir.glob('dic-*.json')))} 个文件加载 {len(self.equals)} 个等式")

    async def get_matching_equals(self, target_pattern: str, excluded_chars: str, required_chars: str) -> List[str]:
        """获取匹配的单词"""
        # 长度匹配
        candidates = [equal for equal in self.equals if len(equal) == len(target_pattern)]
        
        # 位置匹配
        candidates = [
            equal for equal in candidates 
            if all(
                target_pattern[i] == "_" or equal[i] == target_pattern[i] 
                for i in range(len(equal))
            )
        ]
        
        # 排除不能出现的字符
        if excluded_chars:
            candidates = [
                equal for equal in candidates 
                if not any(char in equal for char in excluded_chars)
            ]
        
        # 处理必须出现但位置不确定的字符
        if required_chars:
            # 统计required_chars中每个字符的出现次数
            required_counts = Counter(required_chars)
            
            # 统计target_pattern中已经确定位置的字符
            fixed_chars = {char for char in target_pattern if char != "_"}
            
            candidates = [
                equal for equal in candidates 
                if self._satisfies_required_chars(equal, target_pattern, required_counts, fixed_chars)
            ]
        
        return candidates
    
    def _satisfies_required_chars(self, equal: str, pattern: str, required_counts: Counter, fixed_chars: set) -> bool:
        """
        检查单词是否满足required_chars的要求
        
        对于每个字符，equal中_对应位置的该字符出现次数 >= required_chars中该字符的出现次数
        （已确定位置的字符不计入）
        """
        # 统计equal中在pattern下划线位置的字符
        flexible_positions_chars = []
        for i, char in enumerate(equal):
            if pattern[i] == "_":  # 这个位置是灵活的
                flexible_positions_chars.append(char)
        
        # 统计灵活位置的字符出现次数
        flexible_counts = Counter(flexible_positions_chars)
        
        # 检查每个required字符是否满足条件
        for char, required_count in required_counts.items():
            # 获取灵活位置中该字符的出现次数
            flexible_count = flexible_counts.get(char, 0)
            
            # 如果灵活位置的出现次数小于要求，则不满足
            if flexible_count < required_count:
                return False
        
        return True
    
    async def main(
        self,
        matcher: Matcher,
        event: MessageEvent
    ) -> None:
        """处理消息"""
        # 解析输入
        input_str = event.get_message().__str__().strip()
        
        # 提取三部分：目标模式、排除字符、必须字符
        target_pattern = input_str
        excluded_chars = ""
        required_chars = ""
        
        # 检查是否有!分隔符
        if "!" in input_str:
            parts = input_str.split("!", 1)
            target_pattern = parts[0]
            remaining = parts[1]
            
            # 检查是否有?分隔符
            if "?" in remaining:
                star_parts = remaining.split("?", 1)
                excluded_chars = star_parts[0]
                required_chars = star_parts[1]
            else:
                excluded_chars = remaining
        # 如果没有!但有?分隔符
        elif "?" in input_str:
            parts = input_str.split("?", 1)
            target_pattern = parts[0]
            required_chars = parts[1]
        
        matching_equals = await self.get_matching_equals(target_pattern, excluded_chars, required_chars)
        
        if len(matching_equals) == 0:                                    # 如果没有匹配到等式, 则返回
            await matcher.send("没有匹配到等式捏")
        elif len(matching_equals) > 50:                                  # 如果匹配到的等式太多, 则返回
            await matcher.send("匹配到的等式太多了(>50), 建议您缩小一下范围")
        else:                                                           # 返回匹配到的等式
            await matcher.send(
                "以下是匹配到的等式：\n"+
                "\n".join(matching_equals)
            )
            
nerdle_help = NerdleHelp()