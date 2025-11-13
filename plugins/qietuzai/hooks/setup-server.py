#!/usr/bin/env python3
"""
Qietuzai Plugin Setup Server
提供图形化界面配置 Figma API Key
"""

import http.server
import socketserver
import urllib.parse
import json
import os
import sys
from pathlib import Path

PORT = 3456

# HTML 页面
HTML_FORM = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>切图仔 Plugin - 配置向导</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 600px;
            width: 100%;
            padding: 40px;
        }

        .header {
            text-align: center;
            margin-bottom: 32px;
        }

        .icon {
            font-size: 64px;
            margin-bottom: 16px;
        }

        h1 {
            color: #1a202c;
            font-size: 28px;
            margin-bottom: 8px;
        }

        .subtitle {
            color: #718096;
            font-size: 14px;
        }

        .step {
            background: #f7fafc;
            border-left: 4px solid #667eea;
            padding: 16px;
            margin-bottom: 24px;
            border-radius: 4px;
        }

        .step-title {
            color: #2d3748;
            font-weight: 600;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .step-content {
            color: #4a5568;
            font-size: 14px;
            line-height: 1.6;
        }

        .step-content a {
            color: #667eea;
            text-decoration: none;
        }

        .step-content a:hover {
            text-decoration: underline;
        }

        .form-group {
            margin-bottom: 24px;
        }

        label {
            display: block;
            color: #2d3748;
            font-weight: 600;
            margin-bottom: 8px;
            font-size: 14px;
        }

        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 14px;
            transition: all 0.2s;
            font-family: 'Monaco', 'Menlo', monospace;
        }

        input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .hint {
            color: #718096;
            font-size: 12px;
            margin-top: 8px;
        }

        .button-group {
            display: flex;
            gap: 12px;
            margin-top: 32px;
        }

        button {
            flex: 1;
            padding: 14px 24px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-primary {
            background: #667eea;
            color: white;
        }

        .btn-primary:hover {
            background: #5568d3;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }

        .btn-secondary {
            background: #e2e8f0;
            color: #4a5568;
        }

        .btn-secondary:hover {
            background: #cbd5e0;
        }

        .error {
            background: #fed7d7;
            border: 1px solid #fc8181;
            color: #c53030;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 16px;
            font-size: 14px;
        }

        .loading {
            display: none;
            text-align: center;
            margin-top: 16px;
        }

        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="icon">🎨</div>
            <h1>切图仔 Plugin</h1>
            <p class="subtitle">配置 Figma API Key</p>
        </div>

        <div class="step">
            <div class="step-title">
                <span>📝</span>
                <span>第 1 步：获取 Figma API Key</span>
            </div>
            <div class="step-content">
                访问 <a href="https://www.figma.com/settings" target="_blank">Figma 设置页面</a>，
                在 "Personal access tokens" 部分创建一个新的 token。
            </div>
        </div>

        <div class="step">
            <div class="step-title">
                <span>🔑</span>
                <span>第 2 步：输入 API Key</span>
            </div>
            <div class="step-content">
                将刚才复制的 token 粘贴到下方输入框中。
            </div>
        </div>

        <form id="setupForm">
            <div class="form-group">
                <label for="apiKey">Figma API Key *</label>
                <input
                    type="password"
                    id="apiKey"
                    name="apiKey"
                    placeholder="figd_xxxxxxxxxxxx"
                    required
                    autocomplete="off"
                >
                <div class="hint">
                    💡 您的 API Key 将被安全地存储在本地环境变量中
                </div>
            </div>

            <div class="button-group">
                <button type="button" class="btn-secondary" onclick="window.close()">
                    取消
                </button>
                <button type="submit" class="btn-primary">
                    保存配置
                </button>
            </div>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p style="margin-top: 12px; color: #718096;">正在保存配置...</p>
            </div>
        </form>
    </div>

    <script>
        document.getElementById('setupForm').addEventListener('submit', async (e) => {
            e.preventDefault();

            const apiKey = document.getElementById('apiKey').value;
            const loading = document.getElementById('loading');
            const submitBtn = e.target.querySelector('button[type="submit"]');

            // 显示加载状态
            submitBtn.disabled = true;
            loading.style.display = 'block';

            try {
                const response = await fetch('/save', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ apiKey })
                });

                const result = await response.json();

                if (result.success) {
                    // 跳转到成功页面
                    window.location.href = '/success?shell=' + encodeURIComponent(result.shell || 'bash');
                } else {
                    alert('保存失败: ' + result.error);
                    submitBtn.disabled = false;
                    loading.style.display = 'none';
                }
            } catch (error) {
                alert('保存失败: ' + error.message);
                submitBtn.disabled = false;
                loading.style.display = 'none';
            }
        });
    </script>
</body>
</html>
"""

SUCCESS_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>配置成功</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 600px;
            width: 100%;
            padding: 40px;
            text-align: center;
        }

        .success-icon {
            font-size: 64px;
            margin-bottom: 24px;
        }

        h1 {
            color: #1a202c;
            font-size: 28px;
            margin-bottom: 16px;
        }

        .message {
            color: #4a5568;
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 32px;
        }

        .info-box {
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 24px;
            text-align: left;
        }

        .info-box h3 {
            color: #2d3748;
            font-size: 14px;
            margin-bottom: 12px;
        }

        .info-box p {
            color: #718096;
            font-size: 14px;
            line-height: 1.6;
        }

        .command {
            background: #2d3748;
            color: #48bb78;
            padding: 12px 16px;
            border-radius: 8px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 13px;
            margin: 8px 0;
            text-align: left;
        }

        button {
            background: #667eea;
            color: white;
            padding: 14px 32px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }

        button:hover {
            background: #5568d3;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="success-icon">✅</div>
        <h1>配置成功！</h1>
        <p class="message">
            您的 Figma API Key 已成功保存到系统环境变量中。
        </p>

        <div class="info-box">
            <h3>📋 配置详情</h3>
            <p>✅ API Key 已保存到插件配置文件 <strong>.mcp.json</strong></p>
            <p>✅ 备份已添加到: <strong>{shell_config}</strong></p>
            <div class="command">export FIGMA_API_KEY="****"</div>
        </div>

        <div class="info-box">
            <h3>🔄 下一步</h3>
            <p>请<strong>重启 Claude Code</strong> 使配置生效，然后即可开始使用切图仔 Plugin！</p>
            <p style="margin-top: 8px; font-size: 12px; color: #e53e3e;">⚠️ 注意：请勿将 <strong>.mcp.json</strong> 提交到 git，以保护您的 API Key 安全</p>
        </div>

        <button onclick="window.close()">关闭此页面</button>
    </div>

    <script>
        // 10 秒后自动关闭
        setTimeout(() => {
            window.close();
        }, 10000);
    </script>
</body>
</html>
"""


class SetupHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_FORM.encode('utf-8'))
        elif self.path.startswith('/success'):
            # 解析查询参数
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            shell = params.get('shell', ['bash'])[0]

            # 确定配置文件路径
            shell_configs = {
                'zsh': '~/.zshrc',
                'bash': '~/.bashrc',
                'fish': '~/.config/fish/config.fish'
            }
            shell_config = shell_configs.get(shell, '~/.bashrc')

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            html = SUCCESS_HTML.replace('{shell_config}', shell_config)
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            api_key = data.get('apiKey', '').strip()

            if not api_key:
                self.send_json_response({'success': False, 'error': 'API Key 不能为空'})
                return

            # 检测 shell 类型
            shell = os.environ.get('SHELL', '/bin/bash')
            if 'zsh' in shell:
                config_file = Path.home() / '.zshrc'
                shell_name = 'zsh'
            elif 'fish' in shell:
                config_file = Path.home() / '.config' / 'fish' / 'config.fish'
                shell_name = 'fish'
            else:
                config_file = Path.home() / '.bashrc'
                shell_name = 'bash'

            try:
                # 1. 更新 .mcp.json 文件（替换占位符）
                # 获取插件根目录
                script_dir = Path(__file__).parent
                plugin_root = script_dir.parent
                mcp_json_path = plugin_root / '.mcp.json'

                if not mcp_json_path.exists():
                    raise FileNotFoundError(f'.mcp.json 文件不存在: {mcp_json_path}')

                # 读取并替换占位符
                mcp_content = mcp_json_path.read_text()
                if '${FIGMA_API_KEY}' in mcp_content:
                    mcp_content = mcp_content.replace('${FIGMA_API_KEY}', api_key)
                    mcp_json_path.write_text(mcp_content)

                # 2. 同时也保存到 shell 配置文件（作为备份）
                # 读取现有配置
                if config_file.exists():
                    content = config_file.read_text()
                else:
                    content = ''

                # 检查是否已经存在 FIGMA_API_KEY
                if 'FIGMA_API_KEY' in content:
                    # 更新现有的
                    import re
                    pattern = r'export FIGMA_API_KEY=.*'
                    if re.search(pattern, content):
                        content = re.sub(pattern, f'export FIGMA_API_KEY="{api_key}"', content)
                    else:
                        content += f'\nexport FIGMA_API_KEY="{api_key}"\n'
                else:
                    # 添加新的
                    content += f'\n# Qietuzai Plugin - Figma API Key\nexport FIGMA_API_KEY="{api_key}"\n'

                # 写入配置文件
                config_file.parent.mkdir(parents=True, exist_ok=True)
                config_file.write_text(content)

                self.send_json_response({
                    'success': True,
                    'shell': shell_name,
                    'config_file': str(config_file),
                    'mcp_json': str(mcp_json_path)
                })

                # 配置成功后，延迟关闭服务器
                import threading
                def shutdown_server():
                    import time
                    time.sleep(2)
                    print('\n✅ 配置已保存，服务器即将关闭...')
                    os._exit(0)

                threading.Thread(target=shutdown_server, daemon=True).start()

            except Exception as e:
                self.send_json_response({
                    'success': False,
                    'error': str(e)
                })
        else:
            self.send_error(404)

    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def log_message(self, format, *args):
        # 减少日志输出
        pass


def main():
    try:
        with socketserver.TCPServer(("", PORT), SetupHandler) as httpd:
            print(f"✨ 配置服务器已启动: http://localhost:{PORT}")
            print(f"📝 请在浏览器中完成配置...")
            print(f"⏹  完成后服务器会自动关闭\n")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 服务器已关闭")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ 端口 {PORT} 已被占用，请检查是否有其他配置向导正在运行")
            sys.exit(1)
        else:
            raise


if __name__ == '__main__':
    main()
