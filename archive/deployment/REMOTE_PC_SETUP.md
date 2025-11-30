# Remote PC Control Setup

Connect Cloud Run to your remote PC (accessed via Rust Desktop) for full local control from anywhere.

## 🏗 Architecture

```
Cloud Run (GCP)
    ↓ WebSocket
[Public Tunnel: Cloudflare/ngrok]
    ↓
Your Remote PC (Rust Desktop)
    ↓ WebSocket Server
[Local Agent: port 8765]
    ↓
Execute Commands, File Ops, System Control
```

---

## 📋 Setup Steps

### **1. On Your Remote PC (Rust Desktop)**

```powershell
# Navigate to project
cd C:\Users\W3jde\PROJECTS\MCP\ultimate-mcp-system

# Activate venv
.\.venv\Scripts\Activate.ps1

# Install WebSocket dependency
pip install websockets

# Generate secure token
$TOKEN = [System.Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32))
Write-Host "Your token: $TOKEN"

# Start local agent
python backend/local_agent.py --port 8765 --token $TOKEN
```

**Agent now listening on:** `ws://localhost:8765`

---

### **2. Expose Agent with Cloudflare Tunnel (FREE)** ☁️

```powershell
# Install cloudflared
winget install cloudflare.cloudflared

# Create tunnel
cloudflared tunnel create w3j-local-agent

# Get tunnel URL (will show something like: abc123.trycloudflare.com)
cloudflared tunnel --url http://localhost:8765

# Keep this running in background
Start-Job -ScriptBlock { cloudflared tunnel --url http://localhost:8765 }
```

**Copy the public URL:** `https://abc123.trycloudflare.com`

---

### **3. Configure Cloud Run to Use Remote PC**

Update `.env` on Cloud Run:

```env
# Remote PC Bridge
REMOTE_PC_BRIDGE_URL=wss://abc123.trycloudflare.com
REMOTE_PC_AUTH_TOKEN=YOUR_TOKEN_FROM_STEP_1
```

---

### **4. Update Local Tools to Use Remote Bridge**

Add this to `backend/tools/local_tools.py`:

```python
# Check if remote bridge is configured
REMOTE_BRIDGE_URL = os.getenv("REMOTE_PC_BRIDGE_URL")

if REMOTE_BRIDGE_URL:
    # Use remote PC via bridge
    from remote_bridge import RemotePCClient
    remote_client = RemotePCClient()
    
    def execute_command_handler(command: str, timeout: int = 30):
        return remote_client.execute_command(command, timeout)
else:
    # Use local execution (current behavior)
    # ... existing code ...
```

---

## 🚀 Deployment Flow

### **Development (Local)**
```powershell
# Terminal 1: Run local agent
python backend/local_agent.py --port 8765 --token YOUR_TOKEN

# Terminal 2: Run orchestrator
python backend/main.py
```

### **Production (Cloud Run + Remote PC)**

```powershell
# On Remote PC (Rust Desktop):
python backend/local_agent.py --port 8765 --token YOUR_TOKEN
cloudflared tunnel --url http://localhost:8765

# Deploy to Cloud Run:
.\scripts\deploy_gcp.ps1 -ProjectId stellar-state-471406-f8

# Set environment variables on Cloud Run:
gcloud run services update mcp-orchestrator `
  --set-env-vars REMOTE_PC_BRIDGE_URL=wss://your-tunnel.trycloudflare.com `
  --set-env-vars REMOTE_PC_AUTH_TOKEN=YOUR_TOKEN
```

---

## 🔒 Security Considerations

1. **Token Security:** Keep your auth token secret! Never commit to git.
2. **HTTPS Only:** Always use `wss://` (WebSocket Secure) in production.
3. **Firewall:** Only expose port 8765 through Cloudflare, not directly.
4. **Rust Desktop:** Your Rust Desktop session must stay active for agent to work.

---

## ✅ Testing

```powershell
# Test local agent
python backend/remote_bridge.py

# Should output:
# ✅ Connected successfully
# Result: {'success': True, 'stdout': 'Hello from remote PC!'}
```

---

## 🎯 What This Enables

From Cloud Run, you can now:
- ✅ Execute commands on your remote PC
- ✅ List/read files on remote PC
- ✅ Monitor system resources
- ✅ Control applications
- ✅ Access PC through Rust Desktop from anywhere

**Your Cloud Run instance now has full access to your remote PC!** 🚀

---

## 📊 Alternative: SSH Tunnel

If you prefer SSH over WebSocket:

```powershell
# On Remote PC
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Start-Service sshd

# Create reverse tunnel to Cloud Run
ssh -R 8765:localhost:8765 user@your-cloud-run-ip
```

Then Cloud Run connects to `localhost:8765` → tunnels to your PC.

---

## 🔧 Troubleshooting

**Agent won't start:**
```powershell
# Check if port is available
Test-NetConnection -ComputerName localhost -Port 8765

# Kill process using port
Get-Process | Where-Object {$_.Name -eq "python"} | Stop-Process
```

**Cloudflare tunnel disconnects:**
```powershell
# Use persistent tunnel instead
cloudflared tunnel create w3j-persistent
cloudflared tunnel route dns w3j-persistent agent.yourdomain.com
cloudflared tunnel run w3j-persistent
```

**Cloud Run can't connect:**
- Verify `REMOTE_PC_BRIDGE_URL` starts with `wss://` (not `ws://`)
- Check auth token matches on both sides
- Test tunnel URL in browser first
