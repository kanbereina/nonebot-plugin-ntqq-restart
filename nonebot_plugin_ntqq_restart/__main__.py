from datetime import datetime, timedelta

from nonebot import get_plugin_config, get_driver
from nonebot_plugin_apscheduler import scheduler

from .config import Config
from .utils import (
    NTQQ,
    ntqq_path_checker,
    run_nqq_main, restart_nqqq_main
)


# 检查NTQQ路径
ntqq_path_checker()


Driver = get_driver()
PluginConfig = get_plugin_config(Config)


@Driver.on_startup
async def start_qq_mian():
    scheduler.add_job(  # 防一直处于on_startup状态, 无法最小化窗口
        run_nqq_main, "date",
        next_run_time=datetime.now() + timedelta(seconds=1)
    )


@Driver.on_bot_connect
async def hide_window_main():
    # Bot连接时最小化NTQQ窗口
    await NTQQ.set_hwnd()  # 获取窗口句柄
    NTQQ.wait_window()  # 等待窗口加载
    await NTQQ.hide_window()


@Driver.on_bot_disconnect
async def restart_ntqq_main():
    scheduler.add_job(  # 防一直处于on_bot_disconnect状态, 并防止shutdown的时候无法立即停止
        restart_nqqq_main, "date",
        next_run_time=datetime.now() + timedelta(seconds=1)
    )


@Driver.on_shutdown
async def close_qq_main():
    NTQQ.set_shutdown()  # 设置shutdown状态
    NTQQ.close()  # 关闭NTQQ进程
