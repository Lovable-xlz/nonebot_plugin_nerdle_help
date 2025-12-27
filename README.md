# nonebot_plugin_nerdle_help
nerdle 小游戏帮助工具

## 安装步骤（Windows 环境下，对 Linux 的兼容性未知）
1. 将文件夹 `nonebot_plugin_nerdle_help` 下载并移动到你的项目所在目录 `.\.venv\Lib\site-packages` 下
2. 打开终端，在项目根目录输入 `pip install -e .\.venv\Lib\site-packages\nonebot_plugin_nerdle_help` 以安装该插件。

   请确保你的环境中存在 `setuptools` 和 `wheel` 库！
3. 在你的项目的 `pyproject.toml` 中添加如下内容：

```python
dependencies = [
    "nonebot-plugin-nerdle-help>=0.0.1",
    # 其余部分保持你的内容不变
]


nonebot-plugin-nerdle-help = ["nonebot_plugin_nerdle_help"]
```

4. 运行你的项目，检查是否能正常加载该插件。

## 使用教程

搭配插件 (https://github.com/Lovable-xlz/nonebot_plugin_nerdle)[https://github.com/Lovable-xlz/nonebot_plugin_nerdle] 一起食用效果最佳！

输入格式形如 `s1` + `!s2` + `?s3`：

`s1` 为待猜测等式（由 `0-9+-*/=` 和 `_` 构成、`_` 表示未确定字符），`s2` 为不包含的字符，`s3` 为包含但未确定位置（出现在 `_` 上）的字符，在等式库内进行匹配并返回符合等式；

`!s2`、`?s3` 部分均为可选项；

`s3` 中允许字符出现多次，按出现次数进行匹配。

## 其他说明

`/nonebot_plugin_nerdle_help/equals` 下的文件生成，请参考 (nerdle 插件)[https://github.com/Lovable-xlz/nonebot_plugin_nerdle] 仓库中的 `cpp` 文件。
