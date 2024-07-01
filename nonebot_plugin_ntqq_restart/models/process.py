from typing import List, Annotated

from pydantic import BaseModel


class Process(BaseModel):
    id: Annotated[int, "进程ID"]
    id_str: Annotated[str, "进程ID的字符串形式"]
    name: Annotated[str, "完整进程名, 可能包含.exe后缀"]
    hwnd_list: Annotated[List[int], "进程下的窗口句柄ID"]
    # hwnd_str_list: Annotated[List[str], "进程下的窗口句柄ID的字符串形式"]


__all__ = ["Process"]
