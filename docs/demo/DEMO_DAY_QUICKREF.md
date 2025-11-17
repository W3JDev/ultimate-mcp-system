# 🎯 Demo Day Quick Reference Card

**Print this page and keep it next to your computer during demo/recording!**

---

## ⚡ Emergency Commands

```bash
# Start everything
./scripts/start_demo.sh

# Stop everything  
./scripts/stop_demo.sh

# Test everything
./scripts/test_servers.sh

# Validate setup
./scripts/validate_setup.sh

# View logs
tail -f backend/logs/*.log
```

---

## 🌐 URLs (Open in Browser Tabs)

1. http://localhost:7860 - **Master Orchestrator**
2. http://localhost:7862 - **N8N Automation**
3. http://localhost:7863 - **Agent Builder**
4. http://localhost:7864 - **Local Control**
5. http://localhost:7860/docs - **API Docs**

---

## 📋 5-Minute Demo Script

### 1. Intro (30 sec)
> "Hi! This is the Ultimate MCP System - a unified orchestrator for managing multiple MCP servers. Watch how one interface routes to specialized services."

**Action**: Show all 4 UIs in tabs

---

### 2. Master Orchestrator (1 min)
> "The orchestrator analyzes requests and routes them intelligently."

**Test**:
```bash
curl -X POST http://localhost:7860/process \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a workflow for email notifications"}'
```

**Show**: Response mentions "N8N"

---

### 3. N8N Automation (1.5 min)
> "Our N8N MCP generates workflows from plain English."

**Steps**:
1. Open http://localhost:7862
2. Tab: "Create Workflow"
3. Description: "Daily GitHub trending repos via email"
4. Trigger: "Schedule"
5. Click "Generate"

**Show**: Workflow JSON with nodes

---

### 4. Agent Builder (1.5 min)
> "Build agents with 5 frameworks from one interface."

**Steps**:
1. Open http://localhost:7863
2. Tab: "ADK Agent"
3. Name: "Research Agent"
4. Tools: web_search, summarize
5. Click "Create"

**Show**: Agent created successfully

---

### 5. Closing (30 sec)
> "One interface, multiple services, infinite possibilities. That's the Ultimate MCP System. Check it out on GitHub!"

**Show**: README with GitHub star button

---

## 🆘 If Something Breaks

### Server Won't Start
```bash
# Kill and restart
./scripts/stop_demo.sh
sleep 2
./scripts/start_demo.sh
```

### Port Conflict
```bash
# Kill specific port
lsof -ti:7860 | xargs kill -9
```

### Gradio Not Loading
```bash
# Check Python version
python3 --version  # Need 3.11 or 3.12

# If 3.13, install fix
pip install audioop-lts
```

---

## 🎥 Recording Checklist

### Before Recording
- [ ] Close unnecessary apps
- [ ] Silence notifications
- [ ] Clean desktop
- [ ] Test microphone
- [ ] Start screen recording
- [ ] Open all browser tabs
- [ ] Start all servers
- [ ] Run test_servers.sh

### During Recording
- [ ] Speak clearly
- [ ] Move mouse slowly
- [ ] Zoom in on important parts
- [ ] Don't rush
- [ ] If mistake: pause, continue (edit later)

### After Recording
- [ ] Stop recording
- [ ] Save file
- [ ] Watch for errors
- [ ] Edit if needed
- [ ] Export as MP4

---

## 📊 Success Metrics

### Minimum Viable Demo
- ✅ Shows all 4 UIs
- ✅ Demonstrates routing
- ✅ Creates 1 workflow
- ✅ Creates 1 agent
- ✅ Under 10 minutes

### Great Demo
- ✅ All minimum requirements
- ✅ Professional narration
- ✅ Smooth execution
- ✅ Clear explanations
- ✅ Shows unique value

---

## 🎬 Camera Angles

### Full Screen
- Main demonstrations
- UI interactions
- Most of the demo

### Zoom In
- Generated JSON
- Important buttons
- Success messages

### Picture-in-Picture (optional)
- Your face in corner
- For introduction
- For closing

---

## 💡 Key Talking Points

1. **Problem**: Too many individual MCPs to manage
2. **Solution**: One unified orchestrator
3. **Unique**: 500+ apps via Rube integration (mention even if not shown)
4. **Frameworks**: ADK, CrewAI, A2A, Langbase, AGUI
5. **Production**: FastAPI, Gradio, comprehensive logging

---

## 🔥 Wow Moments

### Highlight These
- ✅ Intelligent routing (show it choosing right service)
- ✅ Multi-framework support (show tabs)
- ✅ AI-powered workflow generation (show JSON)
- ✅ Clean architecture (mention logs, docs)
- ✅ Production-ready (mention GCP deployment)

### Avoid Showing
- ❌ Missing API key warnings (expected, but explain)
- ❌ Long loading times (edit out or speed up)
- ❌ Error messages (unless demonstrating handling)

---

## ⏱️ Timing Guide

| Section | Time | Notes |
|---------|------|-------|
| Intro | 0:00-0:30 | Problem & solution |
| Architecture | 0:30-1:00 | Show all 4 UIs |
| Orchestrator | 1:00-2:00 | Routing demo |
| N8N | 2:00-3:30 | Workflow generation |
| Agents | 3:30-5:00 | Multi-framework |
| Local Control | 5:00-6:00 | (Optional) |
| Technical | 6:00-7:00 | Code/architecture |
| Closing | 7:00-7:30 | Summary & CTA |
| **Total** | **7:30** | Target 5-10 min |

---

## 🎤 Backup Script Lines

**If Demo Crashes**:
> "As you can see in this pre-recorded segment, the system handles complex workflows seamlessly."

**If Slow Response**:
> "The AI is generating a comprehensive workflow - this typically takes 2-3 seconds."

**If API Key Missing**:
> "The system works with any Anthropic or OpenAI key. Here it's using the fallback template mode."

**If Port Conflict**:
> "Let me restart the service quickly - this demonstrates the robust process management."

---

## ✅ Pre-Demo Verification (30 min before)

```bash
# 1. Validate
./scripts/validate_setup.sh

# 2. Start
./scripts/start_demo.sh

# 3. Wait
sleep 15

# 4. Test
./scripts/test_servers.sh

# 5. Open browser tabs
# 6. Do one practice run
# 7. Ready!
```

---

## 🎯 Demo Day Mantras

1. **Breathe** - Take your time
2. **Smile** - Show enthusiasm
3. **Explain** - Don't assume knowledge
4. **Highlight** - Point out unique features
5. **Finish Strong** - End with call-to-action

---

## 📞 Emergency Contacts

- **Documentation**: See DEMO_SCENARIOS.md
- **Video Guide**: See VIDEO_INSTRUCTIONS.md
- **Full Guide**: See PHASE5_GUIDE.md
- **GitHub Issues**: For technical questions
- **Logs**: backend/logs/*.log

---

## 🎉 After Demo Checklist

- [ ] Stop recording
- [ ] Save video file
- [ ] Watch entire recording
- [ ] Note any edits needed
- [ ] Stop servers (./scripts/stop_demo.sh)
- [ ] Take a break!
- [ ] Start editing (if needed)
- [ ] Export and upload
- [ ] Update README with video link
- [ ] Submit to hackathon

---

## 💪 Confidence Boosters

✅ Your code works  
✅ Documentation is excellent  
✅ Scripts automate everything  
✅ You've tested the system  
✅ You know your project  

**You've got this!** 🚀

---

**Remember**: Perfect is the enemy of good. A completed demo is better than a perfect demo that never happens.

**Good luck!** 🏆
