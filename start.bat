@echo off
chcp 65001 >nul
title 东阿阿胶京东营销合规检测工具

echo.
echo ========================================
echo   东阿阿胶 · 京东营销合规检测工具 v2.0
echo ========================================
echo.

where node >nul 2>nul
if errorlevel 1 (
    echo [错误] 未检测到 Node.js
    echo.
    echo 请先安装 Node.js 18 或更高版本：https://nodejs.org
    echo 安装后重新运行本脚本。
    echo.
    pause
    exit /b 1
)

echo [1/2] 正在启动本地服务...
if "%DEEPSEEK_API_KEY%"=="" (
    echo       提示：未设置 DEEPSEEK_API_KEY 环境变量
    echo       AI 复核功能需要在页面右上角「API 设置」中填入自己的 DeepSeek API Key
) else (
    echo       已检测到 DEEPSEEK_API_KEY，AI 复核可直接使用
)
echo.

start "" http://localhost:3456
echo [2/2] 浏览器已打开 http://localhost:3456
echo.
echo 关闭本窗口即停止服务。
echo ========================================
echo.

node "%~dp0proxy-server.js"

pause
