# 🚀 W3J MCP Hub - Complete Deployment Guide

This guide walks you through deploying the entire system to Google Cloud Run and connecting it to your remote PC.

## 📋 Prerequisites

- ✅ Google Cloud account (stellar-state-471406-f8)
- ✅ gcloud CLI installed and authenticated
- ✅ Vertex AI API enabled
- ✅ N8N instance running (https://n8n.aixlabs.fun/)
- ✅ Python 3.11+ on remote PC
- ✅ Code pushed to GitHub (Lets-Coin branch)

---

## 🎯 Deployment Steps

### **Step 1: Deploy to Cloud Run**

```powershell
# From project root
gcloud run deploy w3j-mcp-hub \
  --source . \
  --project stellar-state-471406-f8 \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "GOOGLE_CLOUD_PROJECT=stellar-state-471406-f8,GEMINI_MODEL=gemini-3-pro-preview,N8N_BASE_URL=https://n8n.aixlabs.fun/"
```

**Wait for:**
- ✅ Container build complete
- ✅ Service deployed
- ✅ URL provided (save this!)

**Expected URL:** `https://w3j-mcp-hub-XXXXXX-uc.a.run.app`

---

### **Step 2: Set N8N API Key**

```powershell
gcloud run services update w3j-mcp-hub \
  --set-env-vars N8N_API_KEY=YOUR_N8N_API_KEY_HERE \
  --project stellar-state-471406-f8 \
  --region us-central1
```

**Get N8N API key from:** https://n8n.aixlabs.fun/settings

---

### **Step 3: Setup Remote PC**

On your remote PC (via Rust Desktop):

```powershell
# Clone repo (if not already)
git clone https://github.com/W3JDev/ultimate-mcp-system
cd ultimate-mcp-system
git checkout Lets-Coin

# Activate venv
.\.venv\Scripts\Activate.ps1

# Run automated setup
.\setup_remote_pc.ps1
```

**This script will:**
1. Install websockets
2. Generate secure token
3. Start local agent (port 8765)
4. Create Cloudflare tunnel
5. Provide configuration command

**Copy the output:** You'll get a `wss://` URL and token.

---

### **Step 4: Connect Cloud Run to Remote PC**

Use the values from Step 3:

```powershell
gcloud run services update w3j-mcp-hub \
  --set-env-vars REMOTE_PC_BRIDGE_URL=wss://YOUR-TUNNEL-URL.trycloudflare.com \
  --set-env-vars REMOTE_PC_AUTH_TOKEN=YOUR_GENERATED_TOKEN \
  --project stellar-state-471406-f8 \
  --region us-central1
```

---

## ✅ Verification

### **Test Cloud Run**

```powershell
# Health check
curl https://w3j-mcp-hub-XXXXXX-uc.a.run.app/

# Chat interface
Start-Process "https://w3j-mcp-hub-XXXXXX-uc.a.run.app/"
```

### **Test N8N Integration**

In the chat interface, type:
```
Create a workflow that sends a Slack message when a GitHub issue is created
```

**Expected:** Actual N8N workflow JSON returned (not "coming soon")

### **Test Agent Creation**

```
Create a CrewAI agent for content writing
```

**Expected:** Agent configuration with name, system prompt, tools

### **Test Local Control (via Remote Bridge)**

```
Get system information
```

**Expected:** OS, CPU, memory details from your remote PC

---

## 🌐 Your Final URLs

### **Cloud Run (Public)**
```
https://w3j-mcp-hub-XXXXXX-uc.a.run.app
```
Access from anywhere, connects to:
- ✅ Gemini 3 Pro (AI routing)
- ✅ N8N (workflow creation)
- ✅ Remote PC (via WebSocket bridge)

### **N8N Instance**
```
https://n8n.aixlabs.fun/
```

### **Cloudflare Tunnel (Remote PC)**
```
wss://abc-123-xyz.trycloudflare.com
```
Bridges Cloud Run → Your Remote PC

---

## 🎨 Architecture

```
[User's Browser]
    ↓
[Cloud Run: w3j-mcp-hub]
    ↓ (Gemini 3 Pro AI Routing)
    ├─→ [N8N API: n8n.aixlabs.fun] (Create workflows)
    ├─→ [Agent Tools] (CrewAI/ADK/A2A/Langbase/AGUI)
    └─→ [WebSocket Bridge: wss://tunnel.trycloudflare.com]
            ↓
        [Your Remote PC: localhost:8765]
            ↓ (Local Agent)
        [Execute Commands, List Files, System Info]
```

---

## 🛠 Troubleshooting

### **Cloud Run won't start**
```powershell
# Check logs
gcloud run services logs read w3j-mcp-hub \
  --project stellar-state-471406-f8 \
  --region us-central1
```

### **Gemini not working**
```powershell
# Verify Vertex AI API enabled
gcloud services enable aiplatform.googleapis.com \
  --project stellar-state-471406-f8
```

### **N8N connection fails**
- Verify API key is correct
- Check N8N instance is running
- Test: `curl https://n8n.aixlabs.fun/api/v1/workflows`

### **Remote PC not connecting**
- Check local agent is running: `Get-Job`
- Verify Cloudflare tunnel: `Get-Job`
- Test websocket: `Test-NetConnection -ComputerName localhost -Port 8765`

---

## 📊 Environment Variables Summary

| Variable | Value | Purpose |
|----------|-------|---------|
| `GOOGLE_CLOUD_PROJECT` | `stellar-state-471406-f8` | GCP project ID |
| `GEMINI_MODEL` | `gemini-3-pro-preview` | AI model |
| `N8N_BASE_URL` | `https://n8n.aixlabs.fun/` | N8N instance |
| `N8N_API_KEY` | `eyJhbGci...` | N8N auth |
| `REMOTE_PC_BRIDGE_URL` | `wss://abc.trycloudflare.com` | PC tunnel |
| `REMOTE_PC_AUTH_TOKEN` | `generated_token` | PC auth |
| `PORT` | `8080` (Cloud Run auto) | Server port |

---

## 🎉 Success Indicators

- ✅ Cloud Run URL accessible
- ✅ Chat interface loads
- ✅ "What can you do?" shows 17 tools
- ✅ N8N workflow creation works
- ✅ Agent creation returns config (not "coming soon")
- ✅ Local commands execute on remote PC
- ✅ Gemini 3 Pro responses are intelligent

---

## 🚀 Next Steps

1. **Test all tools:** N8N, Agents, Local control
2. **Create demo workflows** for hackathon
3. **Document use cases** in README
4. **Share Cloud Run URL** with team
5. **Monitor usage:** Cloud Run console

---

## 📞 Support

- **GitHub:** https://github.com/W3JDev/ultimate-mcp-system
- **Branch:** Lets-Coin
- **Issues:** GitHub Issues tab

---

## 🏆 What You Built

**W3J MCP Hub** - A fully operational AI-powered automation system that:
- 🤖 Uses Gemini 3 Pro for intelligent routing
- 🔄 Creates N8N workflows from natural language
- 👥 Builds AI agent teams (CrewAI, ADK, etc.)
- 💻 Controls remote PCs via secure WebSocket bridge
- ☁️ Deployed on Google Cloud Run (global access)
- 🔒 Secure with token authentication
- 🚀 Production-ready with 17 working tools

**Congratulations!** 🎉
