# 切图仔 Plugin 安装流程设计

## 问题背景

Plugin 依赖 Framelink Figma MCP Server，需要用户配置 Figma API Key 环境变量。如何在用户安装 plugin 时自动化引导配置流程？

## 解决方案

### 核心思路

使用 **SessionStart Hook** + **自动化向导脚本** 实现半自动配置流程。

### 技术实现

#### 1. MCP Server 配置 (`.mcp.json`)

```json
{
  "mcpServers": {
    "Framelink_Figma_MCP": {
      "command": "npx",
      "args": [
        "-y",
        "figma-developer-mcp",
        "--figma-api-key=${FIGMA_API_KEY}",
        "--stdio"
      ]
    }
  }
}
```

- 使用 `${FIGMA_API_KEY}` 环境变量语法
- 当 plugin 启用时，MCP server 自动启动并读取环境变量

#### 2. SessionStart Hook (`hooks/hooks.json`)

```json
[
  {
    "event": "SessionStart",
    "command": "bash",
    "args": ["{{pluginDir}}/hooks/check-figma-api-key.sh"]
  }
]
```

- 在每次 Claude Code 启动新会话时触发
- 执行检查脚本

#### 3. 自动化向导脚本 (`hooks/check-figma-api-key.sh`)

脚本功能：

1. **检测环境变量**：检查 `$FIGMA_API_KEY` 是否已配置
2. **首���提示**：使用标记文件（`~/.claude/qietuzai-setup-done`）避免重复提示
3. **自动打开浏览器**：
   - macOS: `open https://www.figma.com/settings`
   - Linux: `xdg-open https://www.figma.com/settings`
   - Windows: `start https://www.figma.com/settings`
4. **显示配置指南**：
   - 自动检测用户的 shell 类型（zsh/bash）
   - 提供具体的命令示例
   - 显示友好的图形界面提示

## 用户体验流程

### 场景 1：首次使用（未配置 API Key）

```
用户通过 /plugin 安装 plugin
    ↓
启动 Claude Code
    ↓
SessionStart Hook 触发
    ↓
检查脚本发现未配置 FIGMA_API_KEY
    ↓
自动打开浏览器到 Figma 设置页面
    ↓
终端显示美观的配置向导：
╔═════════════���══════════════════════════╗
║  🎨 切图仔 - 首次配置向导              ║
╚════════════════════════════════════════╝

⚠️  检测到您还未配置 Figma API Key

📝 配置步骤：

1️⃣  正在为您打开 Figma 设置页面...

2️⃣  在浏览器中：
   • 滚动到 'Personal access tokens' 部分
   • 点击 'Create a new personal access token'
   • 输入 token 名称（如 'Claude Code'）
   • 点击 'Create token' 并复制生成的 token

3️⃣  配置环境变量：
   在终端中运行以下命令：

   echo 'export FIGMA_API_KEY="your-api-key-here"' >> ~/.zshrc
   source ~/.zshrc

4️⃣  重启 Claude Code 使配置生效
    ↓
用户按照提示完成配置
    ↓
重启 Claude Code
    ↓
环境变量生效，MCP server 正常启动
    ↓
可以正常使用 plugin
```

### ���景 2：已配置 API Key

```
启动 Claude Code
    ↓
SessionStart Hook 触发
    ↓
检查脚本发现 FIGMA_API_KEY 已配置
    ↓
静默通过，不显示任何提示
    ↓
MCP server 正常工作
```

### 场景 3：已看过向导但未配置

```
启动 Claude Code
    ↓
SessionStart Hook 触发
    ↓
检查脚本发现：
  - FIGMA_API_KEY 未配置
  - 但标记文件已存在（说明已看过向导）
    ↓
不再显示向导（避免重复打扰）
    ↓
用户需要时可查看 README.md
```

## 优势

1. **自动化程度高**：
   - 自动打开浏览器到正确页面
   - 自动检测 shell 类型
   - 提供复制即用的命令

2. **用户体验好**：
   - 首次使用有清晰引导
   - 配置后不再打扰
   - 视觉友好的终端界面

3. **跨平台支持**：
   - 支持 macOS/Linux/Windows
   - 自动适配不同 shell（zsh/bash/powershell）

4. **安全性**：
   - API Key 存储在本地环境变量
   - 不会泄露到配置文件或代码仓库

5. **可维护性**：
   - 配置逻辑独立在脚本中
   - 易于更新和调试
   - README 作为备用文档

## 技术限制

### 无法实现的功能

1. **完全自动获取 API Key**：
   - Figma 要求用户手动创建 Personal Access Token
   - 无法通过 OAuth 或其他方式自动化

2. **直接设置持久环境变量**：
   - 需要用户手动添加到 shell 配置文件
   - 或使用系统环境变量设置（需要管理员权限）

3. **onInstall Hook**：
   - Claude Code 目前没有 plugin 安装时的钩子
   - 只能使用 SessionStart 在首次启动时触发

### 替代方案考虑

可能的其他方案（但实现复杂度更高）：

1. **交互式 CLI 工具**：
   - 在 SessionStart 时提示用户输入 API Key
   - 自动写入配置文件
   - 问题：用户体验不如浏览器获取清晰

2. **使用 Claude Code 配置存储**：
   - 将 API Key 存储在 Claude Code 的配置中
   - 问题：MCP server 仍然需要环境变量，需要额外的桥接层

3. **OAuth 代理服务**：
   - 搭建代理服务处理 Figma OAuth
   - 问题：增加基础设施复杂度，且 Figma API 主要使用 Personal Token

## 文件结构

```
plugins/qietuzai/
├── .claude-plugin/
│   └── plugin.json           # Plugin 元数据
├── .mcp.json                 # MCP server 配置
├── agents/
│   └── qietuzai.md          # Agent 提示词
├── hooks/
│   ├── hooks.json           # Hook 配置
│   └── check-figma-api-key.sh  # 配置检查脚本
├── README.md                 # 用户文档
└── SETUP-FLOW.md            # 本文档
```

## 总结

这个方案实现了：

- ✅ 自动打开浏览器到配置页面
- ✅ 提供清晰的配置指南
- ✅ 避免重复提示
- ✅ 跨平台支持
- ✅ 安全的 API Key 管理

同时保持了：

- ✅ 配置简单
- ✅ 易于维护
- ✅ 用户友好

是当前技术限制下的最优解决方案。
