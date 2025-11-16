#!/usr/bin/env python3
"""
Simple MCP Client Test Script

This script demonstrates how to interact with the MCP Hub Server.
It sends JSON-RPC messages and validates responses.
"""
import json
import subprocess
import sys


def send_message(process, message):
    """Send a JSON-RPC message to the server"""
    json_str = json.dumps(message)
    print(f"→ {json_str}")
    process.stdin.write(json_str + '\n')
    process.stdin.flush()


def read_response(process):
    """Read a JSON-RPC response from the server"""
    line = process.stdout.readline()
    if not line:
        return None
    
    response = json.loads(line)
    print(f"← {json.dumps(response, indent=2)}\n")
    return response


def test_mcp_server():
    """Test the MCP server with a full protocol flow"""
    print("=" * 60)
    print("MCP Hub Server Test Client")
    print("=" * 60)
    print()
    
    # Start the server
    server_path = "backend/mcp_hub_server.py"
    process = subprocess.Popen(
        [sys.executable, server_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    try:
        # Test 1: Initialize
        print("Test 1: Initialize Protocol")
        print("-" * 60)
        send_message(process, {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        })
        response = read_response(process)
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert "result" in response
        print("✅ Initialize successful\n")
        
        # Test 2: Initialized notification
        print("Test 2: Send Initialized Notification")
        print("-" * 60)
        send_message(process, {
            "jsonrpc": "2.0",
            "method": "initialized"
        })
        print("✅ Initialized notification sent (no response expected)\n")
        
        # Test 3: List tools
        print("Test 3: List Available Tools")
        print("-" * 60)
        send_message(process, {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        })
        response = read_response(process)
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 2
        assert "result" in response
        assert "tools" in response["result"]
        print(f"✅ Found {len(response['result']['tools'])} tools\n")
        
        # Test 4: Call echo tool
        print("Test 4: Call Echo Tool")
        print("-" * 60)
        send_message(process, {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "echo",
                "arguments": {
                    "message": "Hello, MCP!"
                }
            }
        })
        response = read_response(process)
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 3
        assert "result" in response
        print("✅ Echo tool executed successfully\n")
        
        # Test 5: Call add tool
        print("Test 5: Call Add Tool")
        print("-" * 60)
        send_message(process, {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "add",
                "arguments": {
                    "a": 15,
                    "b": 27
                }
            }
        })
        response = read_response(process)
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 4
        assert "result" in response
        print("✅ Add tool executed successfully\n")
        
        # Test 6: Call get_time tool
        print("Test 6: Call Get Time Tool")
        print("-" * 60)
        send_message(process, {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "get_time",
                "arguments": {}
            }
        })
        response = read_response(process)
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 5
        assert "result" in response
        print("✅ Get time tool executed successfully\n")
        
        # Test 7: Call non-existent tool (error handling)
        print("Test 7: Error Handling - Non-existent Tool")
        print("-" * 60)
        send_message(process, {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "tools/call",
            "params": {
                "name": "nonexistent",
                "arguments": {}
            }
        })
        response = read_response(process)
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 6
        assert "error" in response
        assert response["error"]["code"] == -32000  # Tool not found
        print("✅ Error handling works correctly\n")
        
        print("=" * 60)
        print("All tests passed! ✅")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        # Print server stderr for debugging
        stderr = process.stderr.read()
        if stderr:
            print("\nServer stderr:")
            print(stderr)
        return 1
    
    finally:
        # Terminate the server
        process.terminate()
        process.wait(timeout=5)
    
    return 0


if __name__ == "__main__":
    sys.exit(test_mcp_server())
