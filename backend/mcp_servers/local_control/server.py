#!/usr/bin/env python3
'''
Local Control MCP Server
PC automation and control (commands, apps, files, input, browser)
Port: 7864
'''
import os
import sys
import subprocess
import platform
import psutil
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
import gradio as gr

# Load environment variables
load_dotenv()

# Configure logging
logger.add("../../logs/local_control.log", rotation="1 day", retention="7 days")

class LocalControlMCP:
    '''Local Control MCP - System automation and control'''
    
    def __init__(self):
        self.system = platform.system()
        logger.info(f"💻 Local Control MCP initialized on {self.system}")
    
    # === System Commands ===
    def execute_command(self, command):
        '''Execute a system command'''
        try:
            if not command.strip():
                return "Error: Empty command"
            
            logger.info(f"📟 Executing: {command}")
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout if result.stdout else result.stderr
            logger.info(f"✅ Command executed successfully")
            
            return f"Exit Code: {result.returncode}\n\nOutput:\n{output}"
        except subprocess.TimeoutExpired:
            return "Error: Command timed out (30s limit)"
        except Exception as e:
            logger.error(f"❌ Command failed: {e}")
            return f"Error: {str(e)}"
    
    # === App Control ===
    def list_processes(self):
        '''List running processes'''
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append({
                        'PID': proc.info['pid'],
                        'Name': proc.info['name'],
                        'CPU%': f"{proc.info['cpu_percent']:.1f}",
                        'Memory%': f"{proc.info['memory_percent']:.1f}"
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by memory usage
            processes.sort(key=lambda x: float(x['Memory%']), reverse=True)
            processes = processes[:20]  # Top 20
            
            output = "TOP 20 PROCESSES (by memory):\n\n"
            output += f"{'PID':<8} {'Name':<30} {'CPU%':<8} {'Memory%':<10}\n"
            output += "-" * 60 + "\n"
            
            for p in processes:
                output += f"{p['PID']:<8} {p['Name']:<30} {p['CPU%']:<8} {p['Memory%']:<10}\n"
            
            return output
        except Exception as e:
            return f"Error: {str(e)}"
    
    def kill_process(self, pid):
        '''Kill a process by PID'''
        try:
            if not pid:
                return "Error: No PID provided"
            
            pid = int(pid)
            proc = psutil.Process(pid)
            proc_name = proc.name()
            
            proc.terminate()
            proc.wait(timeout=5)
            
            logger.info(f"✅ Killed process {pid} ({proc_name})")
            return f"Successfully terminated process {pid} ({proc_name})"
        except psutil.NoSuchProcess:
            return f"Error: Process {pid} not found"
        except psutil.AccessDenied:
            return f"Error: Access denied (try running as administrator)"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # === File Operations ===
    def list_files(self, directory):
        '''List files in a directory'''
        try:
            if not directory:
                directory = str(Path.home())
            
            path = Path(directory).expanduser()
            
            if not path.exists():
                return f"Error: Directory not found: {directory}"
            
            if not path.is_dir():
                return f"Error: Not a directory: {directory}"
            
            files = []
            for item in path.iterdir():
                try:
                    stat = item.stat()
                    files.append({
                        'name': item.name,
                        'type': 'DIR' if item.is_dir() else 'FILE',
                        'size': stat.st_size if item.is_file() else 0
                    })
                except:
                    pass
            
            output = f"DIRECTORY: {path}\n\n"
            output += f"{'Type':<6} {'Name':<40} {'Size':<15}\n"
            output += "-" * 65 + "\n"
            
            for f in sorted(files, key=lambda x: (x['type'] != 'DIR', x['name'])):
                size_str = f"{f['size']:,} bytes" if f['type'] == 'FILE' else ""
                output += f"{f['type']:<6} {f['name']:<40} {size_str:<15}\n"
            
            return output
        except Exception as e:
            return f"Error: {str(e)}"
    
    def read_file(self, filepath):
        '''Read file contents'''
        try:
            if not filepath:
                return "Error: No file path provided"
            
            path = Path(filepath).expanduser()
            
            if not path.exists():
                return f"Error: File not found: {filepath}"
            
            if not path.is_file():
                return f"Error: Not a file: {filepath}"
            
            # Check file size (limit to 1MB)
            if path.stat().st_size > 1_000_000:
                return "Error: File too large (max 1MB)"
            
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            return f"FILE: {path}\n\n{content}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # === Input Control ===
    def simulate_typing(self, text):
        '''Simulate keyboard typing'''
        try:
            # Note: Requires pyautogui to be installed
            try:
                import pyautogui
                pyautogui.write(text, interval=0.05)
                return f"✅ Typed: {text}"
            except ImportError:
                return "Error: pyautogui not installed. Run: pip install pyautogui"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def press_key(self, key):
        '''Press a keyboard key'''
        try:
            try:
                import pyautogui
                pyautogui.press(key)
                return f"✅ Pressed: {key}"
            except ImportError:
                return "Error: pyautogui not installed. Run: pip install pyautogui"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # === Browser Automation ===
    def open_url(self, url):
        '''Open URL in default browser'''
        try:
            import webbrowser
            webbrowser.open(url)
            return f"✅ Opened in browser: {url}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # === System Info ===
    def get_system_info(self):
        '''Get system information'''
        try:
            cpu_count = psutil.cpu_count()
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            info = f"""
SYSTEM INFORMATION
==================

Operating System: {platform.system()} {platform.release()}
Machine: {platform.machine()}
Processor: {platform.processor() or 'N/A'}

CPU:
  Cores: {cpu_count}
  Usage: {cpu_percent}%

Memory:
  Total: {memory.total / (1024**3):.2f} GB
  Available: {memory.available / (1024**3):.2f} GB
  Used: {memory.percent}%

Disk (/):
  Total: {disk.total / (1024**3):.2f} GB
  Free: {disk.free / (1024**3):.2f} GB
  Used: {disk.percent}%

Python Version: {sys.version}
"""
            return info
        except Exception as e:
            return f"Error: {str(e)}"

def create_ui():
    '''Create the Gradio UI'''
    
    mcp = LocalControlMCP()
    
    with gr.Blocks(theme=gr.themes.Soft(), title="Local Control MCP") as demo:
        gr.Markdown('''
        # 💻 Local Control MCP
        **PC automation and system control**
        
        ⚠️ **Warning:** Be careful with system commands - they execute with your user permissions!
        ''')
        
        with gr.Tab("📟 System Commands"):
            gr.Markdown("### Execute System Commands")
            cmd_input = gr.Textbox(
                label="Command",
                placeholder="ls -la  or  dir  or  echo 'Hello World'",
                lines=2
            )
            cmd_btn = gr.Button("Execute Command", variant="primary")
            cmd_output = gr.Textbox(label="Output", lines=15)
            
            cmd_btn.click(
                mcp.execute_command,
                inputs=[cmd_input],
                outputs=cmd_output
            )
            
            gr.Examples(
                examples=[
                    ["dir" if platform.system() == "Windows" else "ls -la"],
                    ["echo 'Hello from MCP!'"],
                    ["python --version"],
                    ["git status"],
                ],
                inputs=cmd_input
            )
        
        with gr.Tab("🖥️ App Control"):
            gr.Markdown("### Process Management")
            
            with gr.Row():
                with gr.Column():
                    list_btn = gr.Button("List Processes", variant="secondary")
                    process_output = gr.Textbox(label="Processes", lines=20)
                    list_btn.click(
                        mcp.list_processes,
                        inputs=[],
                        outputs=process_output
                    )
                
                with gr.Column():
                    kill_pid = gr.Textbox(label="PID to Kill", placeholder="12345")
                    kill_btn = gr.Button("Kill Process", variant="stop")
                    kill_output = gr.Textbox(label="Result")
                    kill_btn.click(
                        mcp.kill_process,
                        inputs=[kill_pid],
                        outputs=kill_output
                    )
        
        with gr.Tab("📁 File Operations"):
            gr.Markdown("### File System Operations")
            
            with gr.Tab("List Files"):
                dir_input = gr.Textbox(
                    label="Directory",
                    placeholder="~  or  C:\\Users\\  or  /home/",
                    value=str(Path.home())
                )
                dir_btn = gr.Button("List Files", variant="primary")
                dir_output = gr.Textbox(label="Files", lines=15)
                dir_btn.click(
                    mcp.list_files,
                    inputs=[dir_input],
                    outputs=dir_output
                )
            
            with gr.Tab("Read File"):
                file_input = gr.Textbox(
                    label="File Path",
                    placeholder="~/documents/file.txt"
                )
                file_btn = gr.Button("Read File", variant="primary")
                file_output = gr.Textbox(label="Content", lines=15)
                file_btn.click(
                    mcp.read_file,
                    inputs=[file_input],
                    outputs=file_output
                )
        
        with gr.Tab("⌨️ Input Control"):
            gr.Markdown("### Keyboard & Mouse Simulation")
            
            with gr.Tab("Type Text"):
                type_input = gr.Textbox(
                    label="Text to Type",
                    placeholder="Hello, World!",
                    lines=3
                )
                type_btn = gr.Button("Simulate Typing", variant="primary")
                type_output = gr.Textbox(label="Result")
                type_btn.click(
                    mcp.simulate_typing,
                    inputs=[type_input],
                    outputs=type_output
                )
            
            with gr.Tab("Press Key"):
                key_input = gr.Dropdown(
                    choices=['enter', 'tab', 'space', 'escape', 'up', 'down', 'left', 'right'],
                    label="Key",
                    value='enter'
                )
                key_btn = gr.Button("Press Key", variant="primary")
                key_output = gr.Textbox(label="Result")
                key_btn.click(
                    mcp.press_key,
                    inputs=[key_input],
                    outputs=key_output
                )
        
        with gr.Tab("🌐 Browser Automation"):
            gr.Markdown("### Browser Control")
            url_input = gr.Textbox(
                label="URL",
                placeholder="https://github.com",
                value="https://github.com"
            )
            url_btn = gr.Button("Open URL", variant="primary")
            url_output = gr.Textbox(label="Result")
            url_btn.click(
                mcp.open_url,
                inputs=[url_input],
                outputs=url_output
            )
            
            gr.Markdown("""
            **Note:** For advanced browser automation, install Playwright:
            ```bash
            pip install playwright
            playwright install chromium
            ```
            """)
        
        with gr.Tab("ℹ️ System Info"):
            gr.Markdown("### System Information")
            info_btn = gr.Button("Get System Info", variant="secondary")
            info_output = gr.Textbox(label="Information", lines=20)
            info_btn.click(
                mcp.get_system_info,
                inputs=[],
                outputs=info_output
            )
    
    return demo

def main():
    '''Launch the Local Control MCP server'''
    logger.info("🚀 Starting Local Control MCP...")
    
    demo = create_ui()
    
    logger.info("✅ Local Control MCP ready")
    print("\n" + "="*60)
    print("[OK] Local Control MCP Running")
    print("[WEB] Access at: http://localhost:7864")
    print("[MCP] Type: Local PC Control & Automation")
    print("="*60 + "\n")
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7864,
        share=False
    )

if __name__ == "__main__":
    main()
