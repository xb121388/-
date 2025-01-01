import os
import subprocess
import time
import json

# 设置 ngrok 路径
ngrok_path = r"C:\Users\16679\OneDrive\桌面\ngrok.exe"


def start_local_server(port=8000, directory="project"):
    """
    启动本地 HTTP 服务器，指定根目录为 HTML 项目所在的目录
    """
    try:
        print(f"Starting local server on http://localhost:{port} with root directory: {directory}")
        # 使用 subprocess 启动 Python 本地服务器并指定目录
        server = subprocess.Popen(
            ["python", "-m", "http.server", str(port), "--bind", "0.0.0.0", "--directory", directory],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(2)  # 等待服务器启动
        return server
    except Exception as e:
        print(f"Error starting local server: {e}")
        return None


def start_ngrok(port=8000):
    """
    使用 ngrok 将本地服务器映射到公网
    """
    try:
        print("Starting ngrok...")
        # 明确使用 ngrok 的路径
        ngrok = subprocess.Popen(
            [ngrok_path, "http", str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(5)  # 等待 ngrok 启动

        # 从 ngrok 的 API 获取公网地址
        ngrok_output = subprocess.check_output(["curl", "-s", "http://127.0.0.1:4040/api/tunnels"])
        tunnels = json.loads(ngrok_output)
        public_url = tunnels["tunnels"][0]["public_url"]
        print(f"Public URL: {public_url}")
        return ngrok, public_url
    except Exception as e:
        print(f"Error starting ngrok: {e}")
        return None, None


def main():
    port = 8000  # 设置本地服务器端口
    project_directory = r"C:\Users\16679\OneDrive\桌面\2023-New-Year-s-Eve-Code-main"  # 指定项目目录

    # 确保目录存在
    if not os.path.exists(project_directory):
        print(f"Error: Project directory '{project_directory}' does not exist.")
        return

    server = start_local_server(port, project_directory)
    if server is None:
        print("Failed to start local server. Exiting...")
        return

    ngrok, public_url = start_ngrok(port)
    if public_url:
        print(f"Your server is publicly accessible at: {public_url}")
        print("Press Ctrl+C to stop the server and ngrok.")

    try:
        # 保持脚本运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping server and ngrok...")
        if server:
            server.terminate()
        if ngrok:
            ngrok.terminate()


if __name__ == "__main__":
    main()
