#!/usr/bin/env python3
"""
Core Issue Diagnostic for Ultimate MCP System
Identifies blocking issues preventing full functionality
"""

import subprocess
import sys
import importlib.util
import os
import socket
from pathlib import Path

def print_header(title):
    print(f"\n{title}")
    print("=" * len(title))

def check_dependency(name):
    """Check if a dependency is available and get its version"""
    try:
        if name == 'audioop':
            import audioop
            return True, "Built-in module"
        else:
            spec = importlib.util.find_spec(name)
            if spec:
                module = importlib.import_module(name)
                version = getattr(module, '__version__', 'unknown')
                return True, version
            else:
                return False, "Not found"
    except Exception as e:
        return False, str(e)

def check_port(port):
    """Check if a port is available"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result != 0  # True if available

def main():
    print("🔍 ULTIMATE MCP SYSTEM - CORE DIAGNOSTIC")
    print("=" * 60)
    
    # 1. Python Environment
    print_header("1️⃣ PYTHON ENVIRONMENT")
    print(f"   Version: {sys.version.split()[0]}")
    print(f"   Executable: {sys.executable}")
    print(f"   Working Dir: {os.getcwd()}")
    
    # 2. Critical Dependencies
    print_header("2️⃣ CRITICAL DEPENDENCIES")
    deps = ['gradio', 'anthropic', 'fastapi', 'uvicorn', 'loguru', 'audioop']
    failed_deps = []
    
    for dep in deps:
        success, info = check_dependency(dep)
        status = "✅" if success else "❌"
        print(f"   {status} {dep}: {info}")
        if not success:
            failed_deps.append(dep)
    
    # 3. Import Tests (safe approach)
    print_header("3️⃣ IMPORT TESTS")
    
    # Test individual components safely
    imports_to_test = [
        ('tools.registry', 'Tool Registry'),
        ('memory', 'Memory Manager'),
        ('orchestrator', 'Orchestrator'),
    ]
    
    failed_imports = []
    for module, name in imports_to_test:
        try:
            # Add backend to path temporarily
            if 'backend' not in sys.path:
                sys.path.insert(0, 'backend')
            
            importlib.import_module(module)
            print(f"   ✅ {name}: Import successful")
        except Exception as e:
            print(f"   ❌ {name}: {str(e)[:80]}...")
            failed_imports.append((module, str(e)))
    
    # 4. Environment Variables
    print_header("4️⃣ ENVIRONMENT VARIABLES")
    env_vars = ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'N8N_API_KEY']
    missing_env = []
    
    for var in env_vars:
        value = os.getenv(var)
        if value and len(value) > 10:
            print(f"   ✅ {var}: Configured ({len(value)} chars)")
        else:
            print(f"   ⚠️  {var}: Missing or short")
            missing_env.append(var)
    
    # 5. Port Availability
    print_header("5️⃣ PORT AVAILABILITY")
    ports = [7860, 7862, 7863, 7864]
    busy_ports = []
    
    for port in ports:
        available = check_port(port)
        status = "✅" if available else "⚠️"
        state = "Available" if available else "In use"
        print(f"   {status} Port {port}: {state}")
        if not available:
            busy_ports.append(port)
    
    # 6. File System
    print_header("6️⃣ FILE SYSTEM")
    
    # Check key directories and files
    paths_to_check = [
        ('backend/', 'Backend directory'),
        ('backend/main.py', 'Main server'),
        ('backend/orchestrator.py', 'Orchestrator'),
        ('backend/logs/', 'Logs directory'),
        ('.env', 'Environment file'),
    ]
    
    missing_files = []
    for path, desc in paths_to_check:
        exists = Path(path).exists()
        status = "✅" if exists else "❌"
        print(f"   {status} {desc}: {path}")
        if not exists:
            missing_files.append(path)
    
    # 7. Test Basic Functionality
    print_header("7️⃣ BASIC FUNCTIONALITY TEST")
    
    try:
        # Test our successful test script
        result = subprocess.run([
            sys.executable, 'test_all_systems.py'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("   ✅ Core MCP functionality: Working")
            if "4/4" in result.stdout:
                print("   ✅ All MCP servers: Operational")
            else:
                print("   ⚠️  Some MCP servers: Issues detected")
        else:
            print("   ❌ Core functionality: Failed")
            print(f"   Error: {result.stderr[:100]}...")
    except subprocess.TimeoutExpired:
        print("   ⚠️  Core functionality: Test timeout")
    except Exception as e:
        print(f"   ❌ Core functionality: {str(e)}")
    
    # SUMMARY
    print_header("📊 DIAGNOSTIC SUMMARY")
    
    critical_issues = []
    warnings = []
    
    if failed_deps:
        critical_issues.append(f"Missing dependencies: {', '.join(failed_deps)}")
    
    if failed_imports:
        critical_issues.append(f"Import failures: {len(failed_imports)} modules")
    
    if missing_files:
        critical_issues.append(f"Missing files: {', '.join(missing_files)}")
    
    if missing_env:
        warnings.append(f"Missing env vars: {', '.join(missing_env)}")
    
    if busy_ports:
        warnings.append(f"Busy ports: {', '.join(map(str, busy_ports))}")
    
    if not critical_issues and not warnings:
        print("🎉 NO CRITICAL ISSUES FOUND!")
        print("✅ System appears ready for deployment")
    else:
        if critical_issues:
            print("❌ CRITICAL ISSUES:")
            for issue in critical_issues:
                print(f"   • {issue}")
        
        if warnings:
            print("⚠️  WARNINGS:")
            for warning in warnings:
                print(f"   • {warning}")
    
    print("\n" + "=" * 60)
    return len(critical_issues) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)