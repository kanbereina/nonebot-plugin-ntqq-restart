from typing import Optional

from nonebot.config import Config as NB_Config


class Config(NB_Config):
    NTQQ_Path: Optional[str] = None  # NTQQ的.exe文件的路径
    enable_login_when_nbrun: bool = False  # 允许插件加载时直接运行NTQQ并最小化窗口
    enable_restart_when_disc: bool = True  # 允许Bot断连后重启
    enable_close_qq_when_shutdown: bool = False  # 允许关闭nb时也关闭NTQQ

    restart_after_disc_time: int = 10  # 在Bot断开连接{int}秒后开始重启
    retry_max_time: Optional[int] = 5  # 重试窗口最小化最大时间(秒)


__all__ = ["Config"]
