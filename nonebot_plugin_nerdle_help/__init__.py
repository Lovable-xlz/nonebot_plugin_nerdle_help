# 由 nonebot_plugin_wordle_help 的 __init__.py 修改而来
import contextlib

from nonebot import on_regex

from .handle import nerdle_help

# 注册正则表达式, 优先级为10, 阻断式, 处理函数为nerdle_help.main
on_regex(
    r'^(?=.*[0-9\+\-\*/=])(?=.*_)[0-9\+\-\*/=_]+(?:!([0-9\+\-\*/=]*))?(?:\?([0-9\+\-\*/=]*))?$',
    priority=10,
    block=True,
    handlers=[nerdle_help.main]
)

with contextlib.suppress(Exception):
    from nonebot.plugin import PluginMetadata
    __plugin_meta__ = PluginMetadata(
        name="nerdle小助手",
        description="nerdle游戏小助手",
        usage="输入格式形如 s1 + !s2 + ?s3（中间不含空格），其中 s1 为待猜测等式（由0-9+-*/=和 _ 构成、_ 表示未确定字符），s2 为不包含的字符，s3 为包含但未确定位置（出现在 _ 上）的字符，在等式库内进行匹配并返回符合等式\n!s2、?s3 部分均为可选项\ns3 中允许字符出现多次，按出现次数进行匹配",
        type="application",
        homepage="?",
        supported_adapters={"~onebot.v11"},
        extra={
            'author':   'Haitang0520',
            'version':  '0.0.1',
            'priority': 10,
        }
    )
