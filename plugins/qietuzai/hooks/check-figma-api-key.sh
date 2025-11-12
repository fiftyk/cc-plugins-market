#!/bin/bash

# 检查是否已经配置过 FIGMA_API_KEY
if [ -z "$FIGMA_API_KEY" ]; then
    # 检查是否是第一次提示（使用一个标记文件）
    FLAG_FILE="$HOME/.claude/qietuzai-setup-done"

    if [ ! -f "$FLAG_FILE" ]; then
        echo ""
        echo "╔════════════════════════════════════════════════════════════╗"
        echo "║  🎨 切图仔 (Qietuzai) Plugin - 首次配置向导               ║"
        echo "╚════════════════════════════════════════════════════════════╝"
        echo ""
        echo "⚠️  检测到您还未配置 Figma API Key"
        echo ""
        echo "📝 配置步骤："
        echo ""
        echo "1️⃣  正在为您打开 Figma 设置页面..."
        echo ""

        # 根据操作系统打开浏览器
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            open "https://www.figma.com/settings" 2>/dev/null
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            xdg-open "https://www.figma.com/settings" 2>/dev/null
        elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
            # Windows
            start "https://www.figma.com/settings" 2>/dev/null
        fi

        echo "2️⃣  在浏览器中："
        echo "   • 滚动到 'Personal access tokens' 部分"
        echo "   • 点击 'Create a new personal access token'"
        echo "   • 输入 token 名称（如 'Claude Code'）"
        echo "   • 点击 'Create token' 并复制生成的 token"
        echo ""
        echo "3️⃣  配置环境变量："
        echo ""

        # 检测 shell 类型并提供相应的配置说明
        if [ -n "$ZSH_VERSION" ]; then
            SHELL_CONFIG="~/.zshrc"
        elif [ -n "$BASH_VERSION" ]; then
            SHELL_CONFIG="~/.bashrc"
        else
            SHELL_CONFIG="~/.profile"
        fi

        echo "   在终端中运行以下命令："
        echo ""
        echo "   echo 'export FIGMA_API_KEY=\"your-api-key-here\"' >> $SHELL_CONFIG"
        echo "   source $SHELL_CONFIG"
        echo ""
        echo "   （请将 your-api-key-here 替换为您刚复制的 token）"
        echo ""
        echo "4️⃣  重启 Claude Code 使配置生效"
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "💡 提示：配置完成后，此消息将不再显示"
        echo ""
        echo "📚 详细文档：查看 plugin 目录中的 README.md"
        echo ""

        # 创建标记文件，避免每次都提示
        mkdir -p "$HOME/.claude"
        touch "$FLAG_FILE"
    fi
else
    # API Key 已配置，静默通过
    exit 0
fi
