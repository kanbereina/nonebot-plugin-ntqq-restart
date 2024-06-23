from datetime import datetime, timedelta

import nonebot
from nonebot_plugin_apscheduler import scheduler

from .config import Config
from .utils import NTQQ, run_qq_main, restart_qq_main


# 检查相关值
NTQQ.check_path_value()
NTQQ.check_file_exists()


Driver = nonebot.get_driver()
PluginConfig = nonebot.get_plugin_config(Config)


@Driver.on_startup
async def start_qq_mian():
    if PluginConfig.enable_login_when_nbrun:  # 允许运行nb的时候进行登录
        scheduler.add_job(  # 防一直处于on_startup状态, 无法最小化窗口
            run_qq_main, "date",
            next_run_time=datetime.now() + timedelta(seconds=1)
        )


@Driver.on_bot_connect
async def hide_window_main():
    await NTQQ.hide_qq_window()  # 最小化QQ窗口


@Driver.on_bot_disconnect
async def restart_ntqq_main():
    if PluginConfig.enable_restart_when_disc:  # 允许Bot断连的时候重启NTQQ
        scheduler.add_job(  # 防一直处于on_bot_disconnect状态, 并防止shutdown的时候无法立即停止
            restart_qq_main, "date",
            next_run_time=datetime.now() + timedelta(seconds=1)
        )


@Driver.on_shutdown
async def close_qq_main():
    if PluginConfig.enable_close_qq_when_shutdown:  # 允许关闭nb时, 同时关闭NTQQ
        NTQQ.close_qq_all_process()
