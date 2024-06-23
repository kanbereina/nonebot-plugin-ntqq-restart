from nonebot import require
from nonebot.plugin import PluginMetadata
require("nonebot_plugin_apscheduler")

from .config import Config
from .__main__ import *

__plugin_meta__ = PluginMetadata(
    name="NTQQ自动登录/断连重启",
    description="一个基于WinAPI的简易NTQQ重启插件",
    usage=".env填写NTQQ路径后加载插件即可自动运行",
    type="application",
    config=Config,
    extra={},
)
