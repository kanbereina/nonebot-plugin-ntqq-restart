import os
import asyncio
from time import time as now_seconds
from datetime import datetime, timedelta
from pathlib import Path

import autoit
import nonebot
from nonebot.log import logger
from nonebot_plugin_apscheduler import scheduler

from .config import Config


PluginConfig = nonebot.get_plugin_config(Config)


class NTQQ:
    @staticmethod
    def check_path_value():
        """检查路径是否为None"""
        if PluginConfig.ntqq_path is None:
            msg = "你没有设置NTQQ的路径, 插件无法正常工作!"
            logger.error(msg)
            raise FileNotFoundError(msg) from None

    @staticmethod
    def check_file_exists():
        """检查文件是否实际存在"""
        path = Path(PluginConfig.ntqq_path)
        if not os.path.exists(path):
            msg = "未找到QQ.exe, 请检查文件是否存在!"
            logger.error(msg)
            raise FileNotFoundError(msg) from None

    @staticmethod
    def check_qq_process_exists() -> bool:
        """
        检查NTQQ进程是否存在
        :return: bool
        """
        autoit.auto_it_set_option("WinTitleMatchMode", 3)  # 标题全匹配模式
        try:
            pid = autoit.win_get_process("QQ")
            logger.debug(f"检查NTQQ进程: PID-{pid}")
        except Exception:
            return False

        return True

    @staticmethod
    def run_qq():
        """
        运行NTQQ
        :return: 进程PID
        """
        path = Path(PluginConfig.ntqq_path)
        os.popen(f'start "QQ" "{str(path)}"')
        logger.info("正在运行NTQQ...")

    @staticmethod
    def close_qq_all_process() -> bool:
        """
        终止NTQQ运行
        :return: bool
        """
        try:
            logger.info("正在终止所有NTQQ的进程...")
            os.popen("taskkill /F /IM QQ.exe")
        except Exception:
            return False

        return True

    @staticmethod
    def wait_qq_run():
        """等待QQ窗口"""
        logger.debug("等待NTQQ窗口...")
        try:
            autoit.win_wait("QQ", timeout=12)
            autoit.win_wait_active("QQ", timeout=10)
        except Exception:
            msg = "等待NTQQ超时, 请重启nb或手动进行登录!"
            logger.error(msg)
            raise TimeoutError(msg) from None

        logger.debug("NTQQ窗口已加载!")

    @staticmethod
    async def hide_qq_window():
        """最小化QQ窗口"""
        first_time = now_seconds()

        while True:
            # 重试最小化窗口最大时间
            now_time = now_seconds()
            time_length = now_time - first_time

            if time_length <= PluginConfig.retry_max_time:
                if autoit.win_get_state("QQ") != 23:
                    autoit.win_set_state("QQ", flag=autoit.properties.SW_MINIMIZE)
                    logger.debug("尝试对NTQQ发送最小化窗口请求...")
                    await asyncio.sleep(0.5)
                    continue

            break

        logger.info("已隐藏NTQQ窗口!")


async def run_qq_main():
    # 如果QQ进程存在, 终止所有进程
    if NTQQ.check_qq_process_exists():
        i = 0  # 循环终止进程
        while i < 3:
            if NTQQ.close_qq_all_process():
                break

            logger.warning(f"终止QQ进程失败, 将重试...({i+1}/3)")
            await asyncio.sleep(1)
            i += 1
            continue

        await asyncio.sleep(1)  # 防止进程终止过快导致启动失败

    NTQQ.run_qq()  # 运行QQ

    NTQQ.wait_qq_run()  # 等待窗口运行


async def restart_qq_main():
    """重启QQ"""
    # 计算相应时间
    restart_time = PluginConfig.restart_after_disc_time
    logger.info(f"将在Bot断连{restart_time}秒后尝试重启NTQQ...")

    next_run_time = datetime.now() + timedelta(seconds=restart_time)
    scheduler.add_job(
        run_qq_main, "date",
        next_run_time=next_run_time
    )


__all__ = ["NTQQ", "run_qq_main", "restart_qq_main"]
