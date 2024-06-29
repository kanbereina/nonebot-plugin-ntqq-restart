from typing import Optional

from nonebot.config import Config as NB_Config


class Config(NB_Config):
    ntqq_path: Optional[str] = None  # NTQQ的.exe文件的路径
    enable_restart: Optional[bool] = True  # 允许运行此插件
    disable_restart_when_debug: Optional[bool] = False  # 日志等级为Debug时自动禁用插件

    restart_time: int = 10  # 设置此项后, 将在断连{Restart_Time}(秒)后重启NTQQ


__all__ = ["Config"]
