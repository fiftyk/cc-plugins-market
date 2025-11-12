#!/bin/bash

# 检查是否已经配置过 FIGMA_API_KEY
if [ -z "$FIGMA_API_KEY" ]; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║  🎨 切图仔 (Qietuzai) Plugin - 配置向导                   ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    echo "⚠️  检测到您还未配置 Figma API Key"
    echo ""
    echo "🌐 正在启动图形化配置界面..."
    echo ""

    # 获取脚本所在目录（使用 CLAUDE_PLUGIN_ROOT 如果可用）
    if [ -n "$CLAUDE_PLUGIN_ROOT" ]; then
        SCRIPT_DIR="$CLAUDE_PLUGIN_ROOT/hooks"
    else
        SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    fi

    # 启动 Python HTTP 服务器（后台运行）
    python3 "$SCRIPT_DIR/setup-server.py" > /dev/null 2>&1 &
    SERVER_PID=$!

    # 等待服务器启动
    sleep 2

    # 打开浏览器到配置页面
    CONFIG_URL="http://localhost:3456"

    echo "✨ 配置页面已在浏览器中打开: $CONFIG_URL"
    echo ""
    echo "📝 请在浏览器中完成以下步骤："
    echo "   1. 访问 Figma 设置页面获取 API Key"
    echo "   2. 在表单中输入您的 API Key"
    echo "   3. 点击保存"
    echo "   4. 重启 Claude Code"
    echo ""
    echo "💡 如果浏览器没有自动打开，请手动访问: $CONFIG_URL"
    echo ""

    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        open "$CONFIG_URL" 2>/dev/null
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        xdg-open "$CONFIG_URL" 2>/dev/null
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        # Windows
        start "$CONFIG_URL" 2>/dev/null
    fi
else
    # API Key 已配置，静默通过
    exit 0
fi
