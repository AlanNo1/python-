"""
ps:
    1、下载windowsdriver:https://github.com/Microsoft/WinAppDriver
    2、运行 WinAppDriver.exe 192.168.1.10 4723 启动服务
    3、支持的windows程序类型
    UWP - Universal Windows
    PlatformWinForms - Windows
    FormsWPF - Windows Presentation Foundation
    Win32- Classic Windows
    4、窗口组件元素识别工具
    https://learn.microsoft.com/zh-cn/windows/win32/winauto/inspect-objects
    5、pip install appium-python-client===1.0.1 注:最新版本不适配
"""

from appium import webdriver
# 设置 WindowsOptions
desired_capabilities ={
    "app":r"C:\Program Files (x86)\Tencent\WeChat\WeChat.exe"}
# 启动 WebDriver 会话
pc_driver = webdriver.Remote(
    command_executor='http://127.0.0.1:4727',  # 这里指向 WinAppDriver 服务
    desired_capabilities=desired_capabilities
)
pc_driver.find_element_by_name('大秦物联WiFi').click()








