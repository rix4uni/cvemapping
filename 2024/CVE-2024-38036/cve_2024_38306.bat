@echo off
chcp 65001 > nul
setlocal

REM 显示标题
echo ==========================================
echo IPv6 协议管理工具
echo ==========================================
echo.

REM 显示当前 IPv6 配置
echo 当前 IPv6 配置:
echo.
ipconfig /all | findstr /C:"IPv6 Address"

REM 询问用户是否要禁用 IPv6 或恢复
echo.
echo 请选择操作:
echo 1. 禁用 IPv6 协议
echo 2. 恢复 IPv6 协议
echo 3. 退出

set /p choice=请输入选项 (1/2/3): 

REM 根据用户选择执行操作
if "%choice%"=="1" (
    echo 正在禁用 IPv6 协议...
    
    REM 禁用 IPv6 相关的功能
    netsh interface ipv6 set teredo disabled >nul 2>&1
    netsh interface ipv6 set 6to4 disabled >nul 2>&1
    netsh interface ipv6 set isatap disabled >nul 2>&1

    REM 修改注册表以禁用 IPv6
    reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters" /v DisabledComponents /t REG_DWORD /d 0xFFFFFFFF /f

    echo IPv6 协议已禁用。请重启计算机以使更改生效。

) else if "%choice%"=="2" (
    echo 正在恢复 IPv6 协议...
    
    REM 启用 IPv6 相关的功能
    netsh interface ipv6 set teredo default >nul 2>&1
    netsh interface ipv6 set 6to4 default >nul 2>&1
    netsh interface ipv6 set isatap default >nul 2>&1

    REM 修改注册表以恢复 IPv6
    reg delete "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters" /v DisabledComponents /f >nul 2>&1

    echo IPv6 协议已恢复。请重启计算机以使更改生效。

) else if "%choice%"=="3" (
    echo 退出程序。
    exit /b
) else (
    echo 无效的选项，请重新运行程序并选择有效的选项。
)

echo.
echo 完成
pause
endlocal 
