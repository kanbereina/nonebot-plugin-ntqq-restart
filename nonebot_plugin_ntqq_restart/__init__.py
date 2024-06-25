import os

from nonebot import require, logger
from nonebot.plugin import PluginMetadata
require("nonebot_plugin_apscheduler")

from .config import Config
# 强制Windows系统插件生效
if os.name == "nt":
    from .__main__ import *
else:
    logger.warning("此插件仅能在Windows系统上使用, 已自动禁用插件!")

__plugin_meta__ = PluginMetadata(
    name="NTQQ自动登录/断连重启",
    description="一个基于WinAPI的简易NTQQ重启插件",
    usage=".env填写NTQQ路径后加载插件即可自动运行",
    type="application",
    config=Config,
    extra={},
)
