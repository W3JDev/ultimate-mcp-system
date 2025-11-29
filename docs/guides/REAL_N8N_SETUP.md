# 🎯 REAL N8N Setup - Exact Fields You're Seeing

**This matches the ACTUAL n8n UI you're looking at right now.**

---

## Step 1: Install Community Package (2 min)

1. Open https://n8n.aixlabs.fun/
2. Click **Settings** (gear icon, bottom left)
3. Click **Community nodes**
4. Click **Install a community node**
5. Paste: `n8n-nodes-mcp-client`
6. Click **Install**
7. Wait ~30 seconds
8. **Close n8n tab completely**
9. Wait 10 seconds
10. Open https://n8n.aixlabs.fun/ again

---

## Step 2: Create SSE Credential (3 min)

### 2.1 Start Creating Credential
1. Click **Credentials** (left sidebar)
2. Click **Add Credential** (top right)
3. Search: `MCP`
4. Select: **MCP Client (SSE) API**

### 2.2 Fill in the EXACT Fields

**Field 1: SSE URL** ⭐
```
https://backend.composio.dev/v3/mcp/be4a071b-1b59-413b-9483-56a9a3cd2bb4/mcp?user_id=pg-test-3259f522-976a-4bcb-b8fb-feabf399a58e
```

**Field 2: SSE Connection Timeout**
```
60000
```
*(Leave as default 60000)*

**Field 3: Messages POST Endpoint**
```
https://backend.composio.dev/v3/mcp/be4a071b-1b59-413b-9483-56a9a3cd2bb4/mcp/messages
```

**Field 4: Additional Headers (JSON)**
```json
{
  "x-api-key": "ak_VnzNckpdAt9k0xMhVtzd"
}
```

**Field 5: Credential Name**
```
Composio MCP - All Apps
```

### 2.3 Save
- Click **Save** (top right)

---

## Step 3: Test It Works (1 min)

1. Click **Workflows** (left sidebar)
2. Click **Add workflow** (top right)
3. Click the **+** button
4. Search: `MCP Client`
5. Select the **MCP Client** node
6. In the node:
   - **Credential**: Select "Composio MCP - All Apps"
   - **Operation**: Select "List Tools"
7. Click **Test step** (bottom of node)

### ✅ Success = You see tools like:
- GMAIL_SEND_EMAIL
- LINKEDIN_CREATE_POST
- TWITTER_CREATE_TWEET
- REDDIT_SUBMIT_POST
- 50+ more...

---

## 🎯 Copy-Paste Summary

**For quick reference:**

### SSE URL
```
https://backend.composio.dev/v3/mcp/be4a071b-1b59-413b-9483-56a9a3cd2bb4/mcp?user_id=pg-test-3259f522-976a-4bcb-b8fb-feabf399a58e
```

### Messages POST Endpoint
```
https://backend.composio.dev/v3/mcp/be4a071b-1b59-413b-9483-56a9a3cd2bb4/mcp/messages
```

### Additional Headers
```json
{
  "x-api-key": "ak_VnzNckpdAt9k0xMhVtzd"
}
```

---

## 📸 What You Should See

**After installing n8n-nodes-mcp-client:**
- Settings → Community nodes → Should show "n8n-nodes-mcp-client" in the list

**When creating credential:**
- Type: **MCP Client (SSE) API** ← This is the exact name
- 4 fields: SSE URL, Timeout, POST Endpoint, Headers

**After testing:**
- List Tools should return 50+ tools
- Each tool shows name, description, input schema

---

## 🐛 Troubleshooting

### "Cannot find MCP Client in nodes list"
→ Community package not installed. Redo Step 1, make sure you restart n8n.

### "Connection timeout"
→ Check the SSE URL has `?user_id=` at the end. Copy exactly from above.

### "401 Unauthorized"
→ Check Additional Headers JSON is exactly: `{"x-api-key": "ak_VnzNckpdAt9k0xMhVtzd"}`

### "No tools showing"
→ Make sure Messages POST Endpoint ends with `/messages`

---

## 🚀 Next Steps After Setup

1. **Fix workflow errors** - Replace Gmail/LinkedIn nodes with MCP Client nodes
2. **Use exact tool names** from List Tools response
3. **Check** `N8N_WORKFLOW_FIX_GUIDE.md` for specific fixes

---

**This guide uses the ACTUAL field names from your n8n v2.22.18 UI** ✅
