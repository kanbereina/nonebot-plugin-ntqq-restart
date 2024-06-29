import os

from nonebot import (
    require,
    get_plugin_config, get_driver
)
from nonebot.plugin import PluginMetadata
from nonebot.log import logger
require("nonebot_plugin_apscheduler")

from .config import Config  # noqa


Driver = get_driver()
PluginConfig = get_plugin_config(Config)


# 仅当系统为Windows时插件生效
if os.name == "nt":
    if PluginConfig.enable_restart:  # 允许插件启动时生效
        if Driver.config.log_level == "DEBUG":
            if not PluginConfig.disable_restart_when_debug:  # 在调试时禁用插件
                from .__main__ import *
            else:
                logger.warning("已设置在调试时禁用此插件, 插件已禁用!")
        else:
            from .__main__ import *
    else:
        logger.warning("已设置禁止此插件加载, 插件已禁用!")
else:
    logger.warning("此插件仅能在Windows系统上使用, 已自动禁用插件!")


__plugin_meta__ = PluginMetadata(
    name="NTQQ自动登录/断连重启",
    description="一个基于WindowsAPI的简易NTQQ重启插件",
    homepage="https://github.com/kanbereina/nonebot-plugin-ntqq-restart",
    usage=".env填写NTQQ路径后加载插件即可自动运行",
    type="application",
    config=Config,
    extra={},
)
