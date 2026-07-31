#!/usr/bin/env bash
# 东阿阿胶 · 京东营销合规检测工具 v2.0 —— 一键启动（macOS / Linux）

set -e
cd "$(dirname "$0")"

echo ""
echo "========================================"
echo "  东阿阿胶 · 京东营销合规检测工具 v2.0"
echo "========================================"
echo ""

if ! command -v node >/dev/null 2>&1; then
  echo "[错误] 未检测到 Node.js"
  echo "请先安装 Node.js 18 或更高版本：https://nodejs.org"
  exit 1
fi

echo "[1/2] 正在启动本地服务..."
if [ -z "${DEEPSEEK_API_KEY:-}" ]; then
  echo "      提示：未设置 DEEPSEEK_API_KEY 环境变量"
  echo "      AI 复核功能需要在页面右上角「API 设置」中填入自己的 DeepSeek API Key"
else
  echo "      已检测到 DEEPSEEK_API_KEY，AI 复核可直接使用"
fi
echo ""

URL="http://localhost:3456"
if command -v open >/dev/null 2>&1; then
  (sleep 1 && open "$URL") &
elif command -v xdg-open >/dev/null 2>&1; then
  (sleep 1 && xdg-open "$URL") &
fi

echo "[2/2] 请在浏览器打开 $URL"
echo ""
echo "按 Ctrl+C 停止服务。"
echo "========================================"
echo ""

exec node proxy-server.js
