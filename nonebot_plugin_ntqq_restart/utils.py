import asyncio
import os
from pathlib import Path
from time import time as now_time
from datetime import datetime, timedelta
from typing import List, Dict, Optional

import autoit
import subprocess
import win32gui
import win32con
import win32process
from psutil import Process as PsutilProcess
# nonebot
from nonebot import get_plugin_config
from nonebot.log import logger
from nonebot_plugin_apscheduler import scheduler

from .config import Config
from .models import Process


PluginConfig = get_plugin_config(Config)
MaxRetyTime = 6  # 窗口最小化最大尝试时间


def ntqq_path_checker():
    """检查NTQQ路径值"""
    # 检查路径是否为None
    if PluginConfig.ntqq_path is None:
        msg = "你没有设置NTQQ的路径, 插件无法正常工作!"
        logger.error(msg)
        raise FileNotFoundError(msg) from None

    # 检查文件是否实际存在
    path = Path(PluginConfig.ntqq_path)
    if not os.path.exists(path):
        msg = "未找到QQ.exe, 请检查文件是否存在!"
        logger.error(msg)
        raise FileNotFoundError(msg) from None

    # 检查名称是否为QQ.exe
    if (file_name := path.name) != "QQ.exe":
        logger.warning(f"文件'{file_name}'可能不是NTQQ!")


class WinAPI:
    @staticmethod
    def get_all_process() -> List[Process]:
        """获取当前系统下的所有进程信息"""
        # 获取所有窗口句柄列表
        hwnd_list: List[int] = list()
        win32gui.EnumWindows(  # 调用此API需要两个参数
            lambda _hwnd, _hwnd_list:  # 创建两个匿名参数
            _hwnd_list.append(_hwnd),
            hwnd_list  # 将结果绑定至'hwnd_list'
        )

        # 构建进程ID与窗口句柄的键值对关系
        dict_pid_to_hwnd: Dict[str, List[int]] = dict()
        for hwnd in hwnd_list:
            if win32gui.IsWindow(hwnd):  # 检查是否为窗口
                # 此处返回一个长度为2的列表: [int, int], 1位置是父进程ID
                pid: int = win32process.GetWindowThreadProcessId(hwnd)[1]
                pid_str = str(pid)
                # 进行分类
                if pid_str in dict_pid_to_hwnd:  # 已创建此键
                    self_hwnd_list: List[int] = dict_pid_to_hwnd[pid_str]
                    self_hwnd_list.append(hwnd)
                else:  # 未创建此键
                    dict_pid_to_hwnd.update({pid_str: [hwnd]})

        # 开始构建模型
        process_list: List[Process] = list()
        for pid_str in dict_pid_to_hwnd:
            # 获得进程名
            pname = PsutilProcess(
                pid := int(pid_str)
            ).name()

            process_list.append(
                Process(
                    id=pid, id_str=pid_str, name=pname,
                    hwnd_list=dict_pid_to_hwnd[pid_str]
                )
            )
        return process_list

    @staticmethod
    def find_process_by_pid(pid: int) -> Optional[Process]:
        """用进程PID获取进程对象"""
        processes: List[Process] = WinAPI.get_all_process()
        for process in processes:
            if process.id == pid:
                return process

        return None

    @staticmethod
    async def wait_process_exist(pid: int, max_time: int = 5):
        """等待进程出现"""
        start_time = now_time()

        while True:
            try:
                if (
                        now_time() - start_time
                ) <= max_time:
                    logger.debug(f"Process PID-{pid} is {PsutilProcess(pid).status()}")
                    break
                else:
                    logger.error("进程等待超时!")
                    break
            except Exception:
                await asyncio.sleep(0.1)
                continue


class _NTQQ:
    def __init__(self):
        self._path: str = PluginConfig.ntqq_path  # NTQQ路径
        self._pid: Optional[int] = None  # 进程ID
        self._hwnd: Optional[int] = None  # 窗口句柄ID

        self._connect_status: bool = False  # Bot是否已连接
        self._shutdown_status: bool = False  # 是否激活shutdown钩子

    def is_connect(self) -> bool:
        """是否处于Bot连接状态"""
        return self._connect_status

    def is_shutdown(self) -> bool:
        """是否激活shutdown钩子"""
        return self._shutdown_status

    def set_connect(self):
        self._connect_status = True

    def set_shutdown(self):
        self._shutdown_status = True

    def get_pid(self) -> int:
        """获取当前NTQQ进程ID"""
        assert self._pid is not None, "NTQQ进程不存在!"
        return self._pid

    def run(self):
        """运行NTQQ"""
        logger.debug("正在启动NTQQ...")

        try:
            self._pid = subprocess.Popen(
                self._path, shell=False,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            ).pid
            logger.success(f"启动NTQQ成功, 当前进程: {self._pid}")
        except Exception as e:
            logger.error("启动NTQQ失败!")
            raise e from None

    async def set_hwnd(self):
        """查找并设置真实窗口句柄"""
        try:
            await WinAPI.wait_process_exist(self._pid)  # 等待进程
            process = WinAPI.find_process_by_pid(self._pid)  # 获得进程信息
        except Exception as e:
            logger.error(e)
            raise e from None

        # 开始匹配窗口句柄
        assert process is not None, "查询NTQQ的进程信息失败!"
        hwnd_list = process.hwnd_list
        for hwnd in hwnd_list:
            try:
                if win32gui.IsWindowEnabled(hwnd):  # 可激活
                    if win32gui.GetClassName(hwnd) == "Chrome_WidgetWin_1":  # 聊天窗口类名
                        self._hwnd = hwnd
                        logger.debug(f"已获取NTQQ窗口句柄: {hwnd}")
                        return None
            except Exception:
                win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                await asyncio.sleep(1)
                win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
                continue

        logger.error("识别窗口句柄失败!")
        raise ValueError from None

    def wait_window(self):
        """等待QQ窗口"""
        logger.debug("正在等待NTQQ窗口...")
        try:
            autoit.win_wait_by_handle(self._hwnd, timeout=10)
            autoit.win_wait_active_by_handle(self._hwnd, timeout=8)
        except Exception:
            logger.warning("等待超时, 窗口可能加载失败!")
            return None

        logger.debug("NTQQ窗口已加载完毕!")

    async def hide_window(self):
        """最小化窗口"""
        global MaxRetyTime
        start_time = now_time()  # 开始时间

        while True:
            if (
                    now_time() - start_time
            ) <= MaxRetyTime:
                if not win32gui.IsIconic(self._hwnd):  # 未窗口完成最小化
                    win32gui.ShowWindow(self._hwnd, win32con.SW_MINIMIZE)  # 最小化
                    logger.debug("尝试对NTQQ发送最小化窗口请求...")
                    await asyncio.sleep(0.5)
                    continue
                else:
                    break
            else:
                logger.error("尝试窗口最小化NTQQ失败!")
                raise ValueError from None

        logger.info("已隐藏NTQQ窗口!")

    def close(self):
        """关闭NTQQ"""
        assert self._pid is not None, "获取NTQQ进程ID失败!"
        logger.debug(f"正在终止NTQQ进程: {self._pid}")

        try:
            PsutilProcess(self._pid).kill()
            logger.info("已关闭NTQQ!")
        except Exception as e:
            logger.warning(f"终止失败, NTQQ进程(PID: {NTQQ.get_pid()})可能已经关闭!")


NTQQ = _NTQQ()


async def run_nqq_main():
    """启动NTQQ"""
    NTQQ.run()  # 运行NTQQ


async def restart_nqqq_main():
    """重启NTQQ"""

    async def _restart_ntqq():
        NTQQ.close()  # 关闭NTQQ
        await run_nqq_main()  # 启动NTQQ

    if not NTQQ.is_shutdown():  # 防止在shutdown钩子激活后运行
        # 计算相应时间
        restart_time = PluginConfig.restart_time
        logger.info(f"将在Bot断连{restart_time}秒后尝试重启NTQQ...")

        # 重启NTQQ
        next_run_time = datetime.now() + timedelta(seconds=restart_time)
        scheduler.add_job(
            _restart_ntqq, "date",
            next_run_time=next_run_time
        )


__all__ = ["NTQQ", "ntqq_path_checker", "run_nqq_main", "restart_nqqq_main"]
