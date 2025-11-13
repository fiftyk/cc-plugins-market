# 切图仔 (Qietuzai) Plugin

自动从 Figma 设计稿生成前端 UI 代码的 Claude Code Agent。

## 功能特性

- 🎨 自动从 Figma 提取设计数据
- 📦 智能下载图片资源（SVG/PNG）
- 🔍 自动检测项目类型（Nuxt/Next.js/React/Vue/Angular）
- 📝 生成符合框架规范的代码
- ✅ 自动验证资源路径和引用

## 安装步骤

### 1. 安装 Plugin

在 Claude Code 中使用 `/plugin` 命令安装此 plugin。

### 2. 图形化配置向导 ✨

**首次启动 Claude Code 时，会自动触发图形化配置向导：**

1. 🌐 **自动启动配置页面**：系统会在浏览器中打开本地配置页面
2. 🎨 **美观的图形界面**：提供友好的表单界面，无需手动编辑配置文件
3. 📋 **获取 API Key**：点击链接跳转到 Figma 设置页面，创建并复制 token
4. ⌨️ **输入并保存**：在表单中粘贴 API Key，点击保存即可自动配置
5. ✅ **自动写入配置**：系统自动将 API Key 写入环境变量
6. 🔄 **重启 Claude Code**：配置完成后重启即可使用

整个过程只需 1-2 分钟，完全图形化操作！

#### 重新配置

如果需要重新配置 API Key：

```bash
# 方法 1: 删除环境变量，重启 Claude Code 会自动提示配置
unset FIGMA_API_KEY

# 方法 2: 直接修改配置文件
vim ~/.zshrc  # 或 ~/.bashrc
# 找到并修改 FIGMA_API_KEY 的值
source ~/.zshrc
```

#### 手动配置（高级）

如果你更喜欢手动配置：

macOS/Linux:
```bash
echo 'export FIGMA_API_KEY="your-api-key-here"' >> ~/.zshrc  # 或 ~/.bashrc
source ~/.zshrc
```

Windows (PowerShell):
```powershell
[System.Environment]::SetEnvironmentVariable('FIGMA_API_KEY', 'your-api-key-here', 'User')
```

### 3. 验证安装

重启后，可以使用以下命令验证 MCP server 是否正常运行：

```bash
claude mcp list
```

应该能看到 `Framelink_Figma_MCP` 服务器已启动。

## 使用方法

### 基础用法

安装配置完成后，直接向 Claude Code 提供 Figma 设计链接即可：

```
帮我把这个 Figma 设计稿做成组件 https://figma.com/design/xxx?node-id=123-456
```

Agent 会自动执行以下流程：
1. **检测项目类型**（Nuxt/Next.js/React/Vue/Angular）
2. **解析 Figma URL**（提取 fileKey 和 nodeId）
3. **自动导出设计预览图**（用于精确的视觉分析）
4. **获取设计数据**（节点结构、样式、资源等）
5. **智能下载资源**（SVG/PNG，自动选择最佳格式）
6. **生成代码**（符合项目框架规范）
7. **验证引用路径**（确保资源正确加载）

### 使用场景示例

#### 场景 1：实现完整页面组件
```
帮我把这个 Figma 的首页设计实现成 Vue 组件
https://figma.com/design/abc123?node-id=1-100
```

#### 场景 2：仅下载设计资源
```
从这个 Figma 链接下载所有图片到项目中
https://figma.com/design/abc123?node-id=1-100
```

#### 场景 3：替换占位图
```
把 HeroSection.vue 组件里的占位图换成 Figma 里的真实设计
https://figma.com/design/abc123?node-id=2-50
```

#### 场景 4：修复资源引用问题
```
我下载的图片在页面上显示 404，帮我检查修复
```

### 工作流程详解

#### 阶段 0：项目类型检测（强制执行）
Agent 会首先分析项目结构，识别使用的框架：
- 读取 `package.json` 识别依赖
- 检查框架配置文件（`nuxt.config.ts`、`next.config.js` 等）
- 分析目录结构

不同框架的资源管理方式：
```
Nuxt 3:      assets/ + import (构建工具处理)
Next.js:     public/ + 直接路径（以 / 开头）
CRA:         src/ + import (Webpack 处理)
Vite:        src/assets/ + import
Angular:     src/assets/ + 直接路径
```

#### 阶段 1-2：解析 URL 与获取数据
- 自动转换 URL 格式（`node-id=123-456` → `nodeId: "123:456"`）
- 获取节点结构、样式、填充等完整数据
- 识别位图、矢量图、文本等不同类型元素

#### 阶段 3：自动导出设计预览图
- 无需手动截图，自动导出高清预览图
- 用于视觉细节分析（多层阴影、复杂渐变等）
- 确保布局还原的精确度

#### 阶段 4：智能下载资源
根据节点类型自动选择最佳格式：
- **矢量图标** → SVG（无损缩放）
- **需要透明的图片** → PNG
- **普通照片** → JPEG
- **大尺寸图片** → 考虑压缩或 WebP

资源会下载到正确的目录，并使用语义化的文件名（kebab-case）。

#### 阶段 5：生成代码
根据项目类型生成正确的引用代码。例如：

**Nuxt 3:**
```vue
<script setup>
import heroImage from '~/assets/images/hero/main-visual.png'
</script>

<template>
  <img :src="heroImage" alt="Hero Visual" />
</template>
```

**Next.js:**
```jsx
import Image from 'next/image'

export default function Hero() {
  return (
    <Image
      src="/images/hero/main-visual.png"
      width={1200}
      height={600}
      alt="Hero Visual"
    />
  )
}
```

#### 阶段 6：验证与清理
- 检查文件完整性和大小
- 验证引用路径正确性
- 运行构建测试（如需要）
- 清理临时文件

## 重要注意事项

### ⚠️ 必读事项

1. **首次使用前必须配置 Figma API Key**
   - 插件首次启动会自动打开配置向导
   - 或访问 [Figma Settings](https://www.figma.com/settings) 手动创建 Personal Access Token
   - API Key 存储在环境变量 `FIGMA_API_KEY` 中

2. **项目类型自动检测**
   - Agent 会在每次任务开始时自动检测项目类型
   - 不同框架的资源引用方式完全不同，错误的引用会导致 404
   - 如果项目类型检测错误，请及时告知 Agent

3. **Figma URL 格式要求**
   - 完整 URL：`https://figma.com/design/[fileKey]?node-id=[nodeId]`
   - 必须包含 `node-id` 参数才能精确定位设计节点
   - 支持多节点选择（用分号分隔）

4. **资源路径使用绝对路径**
   - Agent 下载资源时会自动使用绝对路径
   - 确保在正确的项目目录中运行 Claude Code

5. **自动导出的预览图**
   - Agent 会自动导出设计预览图用于视觉分析
   - 预览图存储在临时目录，完成后自动清理
   - 如需保留预览图，请提前告知

### 📋 最佳实践

1. **提供清晰的 node-id**
   - 在 Figma 中选中要导出的节点/Frame
   - 复制 URL 时确保包含 `node-id` 参数
   - 避免选择整个页面，而是选择具体的设计节点

2. **合理组织资源目录**
   - Agent 会根据项目类型自动选择目录
   - 建议按功能模块分类（如 `hero/`、`features/`、`icons/`）

3. **图片格式选择建议**
   - 图标、Logo → SVG（矢量图，无损缩放）
   - UI 元素、插图 → PNG（支持透明）
   - 照片、背景图 → JPEG（文件更小）
   - 大尺寸图片 → 考虑使用 WebP 格式

4. **文件大小控制**
   - PNG 照片建议 < 500KB
   - SVG 图标建议 < 10KB
   - JPEG 照片建议 < 300KB
   - Agent 会在下载后验证文件大小并给出优化建议

5. **命名规范**
   - Agent 使用 kebab-case 命名（如 `hero-main-visual.png`）
   - 文件名具有语义化，便于理解和维护

### 🔧 技术细节

1. **支持的 Figma 节点类型**
   - FRAME（容器、组件）
   - VECTOR（矢量图标）
   - RECTANGLE/ELLIPSE 等基本形状
   - TEXT（文本元素）
   - IMAGE（位图填充）

2. **资源引用方式对照**
   ```
   Nuxt 3:    import img from '~/assets/images/xxx.png'
   Next.js:   <Image src="/images/xxx.png" ... />
   CRA:       import img from './assets/images/xxx.png'
   Vite:      import img from './assets/images/xxx.png'
   Angular:   src="/assets/images/xxx.png"
   ```

3. **API 限制**
   - Figma API 有速率限制（每小时请求数）
   - 大量资源下载可能需要分批处理
   - Agent 会自动处理速率限制和重试

## 支持的项目类型

- ✅ Nuxt 3
- ✅ Next.js
- ✅ React (CRA)
- ✅ Vue + Vite
- ✅ Angular

## 常见问题

### Q1: 安装后提示找不到 Figma API Key？

**可能原因：**
- 环境变量未正确设置
- Claude Code 未重启以加载新的环境变量
- 环境变量名称错误

**解决方案：**
1. 确保环境变量名称为 `FIGMA_API_KEY`（全大写）
2. 检查环境变量是否已写入配置文件：
   ```bash
   echo $FIGMA_API_KEY  # macOS/Linux
   ```
3. 完全重启 Claude Code（不是重载窗口）
4. 如果仍然失败，尝试手动配置：
   ```bash
   vim ~/.zshrc  # 或 ~/.bashrc
   # 添加：export FIGMA_API_KEY="your-api-key"
   source ~/.zshrc
   ```

### Q2: 图片下载后显示 404？

**可能原因：**
- 项目类型检测错误
- 资源目录不正确
- 引用方式不符合框架要求

**诊断步骤：**
1. 检查 Agent 检测的项目类型是否正确
2. 确认图片文件确实存在于正确的目录
3. 检查组件中的引用路径

**解决方案：**
告诉 Agent 具体情况，例如：
```
我的项目是 Nuxt 3，图片下载到了 assets/images/，
但是页面显示 404，请帮我检查修复
```

Agent 会自动：
- 验证项目类型
- 检查文件位置
- 更新为正确的引用方式

### Q3: Figma API 返回 "节点未找到" 错误？

**可能原因：**
- node-id 格式错误
- 节点已被删除或移动
- 没有访问权限

**解决方案：**
1. 确保 Figma URL 包含正确的 `node-id` 参数
2. 在 Figma 中重新选择节点并复制 URL
3. 确保你的 API Key 有权限访问该文件
4. Agent 会自动转换 node-id 格式（横线→冒号）

### Q4: 下载的 SVG 图标显示模糊？

**可能原因：**
- 矢量图被错误地下载为位图（PNG）
- 浏览器缩放导致

**解决方案：**
1. 告诉 Agent 重新下载为 SVG 格式
2. Agent 会检查节点类型并强制使用 SVG
3. 确保在代码中正确使用 SVG（可作为组件或 img 标签）

### Q5: 资源文件太大，加载慢？

**解决方案：**
1. Agent 会在下载后提示文件大小
2. 对于过大的文件，Agent 会建议优化或转换格式
3. 可以要求 Agent：
   ```
   把这些 PNG 图片压缩一下，或者转换成 WebP 格式
   ```

### Q6: 如何处理 Figma 中的响应式设计？

**建议做法：**
1. 在 Figma 中分别选择不同尺寸的设计节点
2. 分别提供 URL 让 Agent 下载
3. 使用 CSS 媒体查询或框架的响应式工具切换
4. 或者让 Agent 生成响应式的 CSS 代码

### Q7: MCP server 启动失败？

**可能原因：**
- npx 未安装或不可用
- 网络问题导致无法下载 MCP server

**解决方案：**
1. 确保 Node.js 和 npm 已正确安装：
   ```bash
   node --version
   npm --version
   ```
2. 手动测试 MCP server：
   ```bash
   npx -y figma-developer-mcp --help
   ```
3. 检查 Claude Code 的 MCP server 状态：
   ```bash
   claude mcp list
   ```

### Q8: 不同团队成员使用不同的 API Key？

**建议做法：**
1. 每个团队成员使用自己的 Figma Personal Access Token
2. 不要将 API Key 提交到代码仓库
3. 使用 `.env` 文件或环境变量管理（已在 `.gitignore` 中）
4. 在团队文档中说明如何获取和配置 API Key

## 相关资源

- [Framelink Figma MCP 文档](https://www.framelink.ai/docs/quickstart)
- [Figma API 文档](https://www.figma.com/developers/api)

## 反馈与支持

如有问题或建议，欢迎提 Issue。
