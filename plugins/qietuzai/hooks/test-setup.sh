#!/bin/bash
# 测试配置向导
# 用法: bash test-setup.sh

echo "🧪 测试切图仔 Plugin 配置向导"
echo ""

# 临时清除环境变量（仅用于测试）
unset FIGMA_API_KEY

# 设置 CLAUDE_PLUGIN_ROOT（模拟 Claude Code 环境）
export CLAUDE_PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "📁 Plugin 目录: $CLAUDE_PLUGIN_ROOT"
echo ""

# 运行配置检查脚本
bash "$CLAUDE_PLUGIN_ROOT/hooks/check-figma-api-key.sh"

echo ""
echo "✅ 测试完成！"
echo ""
echo "💡 提示："
echo "   - 如果浏览器打开了配置页面，说明脚本工作正常"
echo "   - 配置成功后会在 ~/.claude/qietuzai-setup-done 创建标记文件"
echo "   - 可以通过 'cat ~/.zshrc | grep FIGMA_API_KEY' 验证配置"
