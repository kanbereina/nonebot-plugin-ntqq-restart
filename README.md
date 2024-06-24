<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-ntqq-restart

_✨ 一个简易的Bot断连重启NTQQ的插件 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/kanbereina/nonebot-plugin-ntqq-restart.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-ntqq-restart">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-ntqq-restart.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>


## 📖 介绍

⚠注意：本插件基于**Autoit**和**cmd命令**实现NTQQ重启，如果你不是**Windows**用户，此插件**可能无效**！

此插件主要用于帮助**llonebot**用户防止**NTQQ过期导致的Bot断连**的情况

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-ntqq-restart

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-ntqq-restart
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-ntqq-restart
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-ntqq-restart
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-ntqq-restart
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot-plugin-ntqq-restart"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| NTQQ_Path | 是 | 无 | NTQQ的.exe文件的完整路径 |
| enable_restart_when_disc | 否 | True | 允许Bot断连后重启NTQQ |
| enable_login_when_nbrun | 否 | False | 允许nb加载时运行NTQQ |
| enable_close_qq_when_shutdown | 否 | False | 允许nb关闭时关闭NTQQ |
| restart_after_disc_time | 否 | 10 | 在Bot断连的{int}秒后重启NTQQ |
| retry_max_time | 否 | 5 | 重试NTQQ窗口最小化的最大时间(秒) |

## 🎉 使用
### ①插件配置
你可以参照[**配置文件示例**](https://github.com/kanbereina/nonebot-plugin-ntqq-restart/blob/master/.env.prod.example)或**文档-配置**以配置插件参数
### ②NTQQ端设置（此两个选项保持打开状态）
![NTQQ端设置](https://github.com/kanbereina/nonebot-plugin-ntqq-restart/blob/master/doc/ntqq_config_example.PNG)
### ③配置后直接运行nonebot即可
> **nb run**
### 效果图
![插件运行效果](https://github.com/kanbereina/nonebot-plugin-ntqq-restart/blob/master/doc/run_example.PNG)
