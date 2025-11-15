# 🤖 AGENT INSTRUCTIONS - Ultimate MCP System

**⚠️ READ THIS FIRST - Critical Context for All AI Agents**

## 🆔 PROJECT IDENTITY
- **Name**: Ultimate MCP System
- **Purpose**: All-in-one MCP orchestrator: N8N automation + Multi-framework agent builder + Local PC control
- **Status**: In Development - Phase 1
- **Repository**: https://github.com/W3JDev/ultimate-mcp-system
- **Documentation**: [Google Drive](https://drive.google.com/drive/folders/1QCvj02pdFGpRZB839pNu1RXo5j-5eroF)
- **Tracker**: [Google Sheets](https://docs.google.com/spreadsheets/d/1ldyDrULAOKL0xufNkzaEfI5xvzROsdFqZTIFYKIKZMk)
- **Created**: November 15, 2025
- **Hackathon**: MCP 1st Birthday (Nov 14-30, 2025)

---

## ⚠️ EXISTING INFRASTRUCTURE (CRITICAL - READ FIRST!)

### ✅ What ALREADY EXISTS:
**Backend on GCP Cloud Run**:
- Platform: Google Cloud Platform
- Service: Cloud Run (serverless containers)
- Deployment command: `gcloud run deploy SERVICE_NAME --source . --region REGION`
- Status: Running

### ❌ What DOESN'T Exist Yet (We're Building):
- N8N automation MCP server
- Multi-framework agent builder MCP
- Local PC control MCP  
- Master orchestrator
- Frontend UI

**🚨 CRITICAL RULES**:
1. NEVER suggest migrating from GCP Cloud Run to Supabase or alternatives
2. NEVER suggest platforms other than GCP for deployment
3. USE existing GCP infrastructure - ADD to it, don't replace
4. When in doubt about infrastructure, CHECK THIS FILE FIRST

---

## 💻 TECHNOLOGY STACK

### Core Framework
- **Language**: Python 3.11+
- **MCP Framework**: Gradio 6.0+ (for MCP servers)
- **Orchestration**: Custom multi-MCP router

### Agent Frameworks (All Integrated)
- **ADK** (AI Development Kit) - Agent building
- **A2A** (Agent-to-Agent) - Inter-agent communication
- **Langbase** - Memory & RAG capabilities
- **CrewAI** - Multi-agent orchestration
- **AGUI** - Agent GUI interfaces

### Automation & Integration
- **N8N**: Workflow automation platform
- **Composio**: 500+ app integrations (optional helper)

### APIs & Services
- **Claude API** (Anthropic) - Primary reasoning
- **GPT-4 API** (OpenAI) - Content generation
- **GitHub API** - Code management
- **WhatsApp API** (unofficial) - Messaging
- **GCP APIs** - Cloud services

### Deployment & Infrastructure  
- **Primary Host**: GCP Cloud Run ⚠️ (EXISTING)
- **Containers**: Docker
- **CI/CD**: GitHub Actions
- **Monitoring**: GCP Cloud Logging
- **Version Control**: GitHub

---

## 📁 PROJECT STRUCTURE

\`\`\`
ultimate-mcp-system/
├── AGENT.md                    ← YOU ARE HERE (Critical context)
├── README.md                   ← Project overview & quick start
├── DEPLOYMENT.md               ← GCP Cloud Run deployment guide
├── CURRENT_STATUS.md           ← Real-time status (updated daily)
│
├── backend/                    ← Main MCP system
│   ├── README.md               ← Backend overview & architecture
│   ├── AGENT.md                ← Backend-specific agent instructions
│   ├── main.py                 ← Master Orchestrator entry point
│   ├── orchestrator.py         ← Request routing & MCP coordination
│   ├── memory.py               ← Context management & state
│   │
│   ├── mcp_servers/            ← Individual MCP server implementations
│   │   ├── README.md           ← MCP servers overview
│   │   │
│   │   ├── n8n_automation/     ← N8N workflow automation MCP
│   │   │   ├── README.md       ← N8N MCP detailed docs
│   │   │   ├── server.py       ← N8N MCP server
│   │   │   ├── workflow_builder.py
│   │   │   ├── workflow_tester.py
│   │   │   └── deployer.py
│   │   │
│   │   ├── agent_builder/      ← Multi-framework agent creator MCP
│   │   │   ├── README.md       ← Agent builder detailed docs
│   │   │   ├── server.py       ← Agent builder MCP server
│   │   │   ├── adk_integration.py
│   │   │   ├── a2a_protocol.py
│   │   │   ├── crewai_wrapper.py
│   │   │   ├── langbase_connector.py
│   │   │   └── agui_interface.py
│   │   │
│   │   ├── local_control/      ← PC command execution MCP
│   │   │   ├── README.md       ← Local control detailed docs
│   │   │   ├── server.py       ← Local control MCP server
│   │   │   ├── system_commands.py
│   │   │   ├── browser_automation.py
│   │   │   └── file_operations.py
│   │   │
│   │   └── cloud_services/     ← GCP, WhatsApp, GitHub Actions
│   │       ├── README.md       ← Cloud services detailed docs
│   │       ├── server.py       ← Cloud services MCP server
│   │       ├── gcp_integration.py
│   │       ├── whatsapp.py
│   │       └── github_actions.py
│   │
│   ├── utils/                  ← Helper utilities
│   │   ├── README.md           ← Utils documentation
│   │   ├── routing.py          ← Intent → MCP routing logic
│   │   ├── auth.py             ← API key management
│   │   └── logging.py          ← Structured logging
│   │
│   ├── requirements.txt        ← Python dependencies (exact versions)
│   ├── Dockerfile              ← For GCP Cloud Run deployment
│   └── .env.example            ← API keys template (NEVER commit .env)
│
├── frontend/                   ← UI (if needed)
│   ├── README.md               ← Frontend purpose & setup
│   └── app.py                  ← Gradio interface (TBD)
│
├── docs/                       ← Comprehensive documentation
│   ├── README.md               ← Docs index
│   ├── architecture.md         ← System design & data flow
│   ├── api-spec.md             ← API endpoints & schemas
│   ├── deployment.md           ← Detailed deployment guide
│   ├── troubleshooting.md      ← Common issues & solutions
│   └── contributing.md         ← How to contribute
│
├── scripts/                    ← Automation scripts
│   ├── README.md               ← Scripts documentation
│   ├── setup.sh                ← First-time project setup
│   ├── deploy.sh               ← GCP Cloud Run deployment
│   ├── test.sh                 ← Run all tests
│   └── dev.sh                  ← Start local development server
│
├── tests/                      ← Test suite
│   ├── README.md               ← Testing guide
│   ├── test_n8n_mcp.py
│   ├── test_agent_builder.py
│   ├── test_local_control.py
│   └── test_orchestrator.py
│
├── .github/                    ← GitHub configuration
│   ├── workflows/
│   │   ├── test.yml            ← CI testing
│   │   └── deploy.yml          ← CD to GCP
│   └── ISSUE_TEMPLATE/
│
├── .gitignore                  ← Git ignore rules
├── .env.example                ← Environment variables template
└── docker-compose.yml          ← Local development setup

Every folder has README.md explaining its purpose and contents.
Every major file has inline documentation.
\`\`\`

---

## 🚀 CURRENT STATUS

### Phase 1: Foundation (Current)
- [x] Documentation structure created
- [x] GitHub repository initialized
- [x] Google Drive folder setup
- [x] Tracking sheet created
- [ ] Master Orchestrator skeleton
- [ ] Basic MCP routing
- [ ] Development environment setup

### Next Phase: N8N Integration
- [ ] N8N API wrapper
- [ ] Workflow builder
- [ ] Testing framework
- [ ] Deployment automation

---

## 🛠️ HOW TO WORK ON THIS PROJECT

### First-Time Setup

\`\`\`bash
# 1. Clone the repository
git clone https://github.com/W3JDev/ultimate-mcp-system.git
cd ultimate-mcp-system

# 2. Create Python virtual environment
python3 -m venv venv

# 3. Activate environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r backend/requirements.txt

# 5. Setup environment variables
cp backend/.env.example backend/.env
# IMPORTANT: Edit backend/.env and add your API keys
nano backend/.env  # or use your preferred editor

# 6. Verify installation
python backend/main.py --check
\`\`\`

### Run Locally

\`\`\`bash
# Activate environment (if not already active)
source venv/bin/activate  # Windows: venv\Scripts\activate

# Start the development server
cd backend
python main.py

# Expected output:
# ✅ Master Orchestrator initialized
# ✅ N8N MCP loaded
# ✅ Agent Builder MCP loaded
# ✅ Local Control MCP loaded
# ✅ Cloud Services MCP loaded
# 🌐 Server running at http://localhost:7860

# Access the UI:
# Open browser: http://localhost:7860
\`\`\`

### Deploy to GCP Cloud Run

\`\`\`bash
# CRITICAL: Use GCP Cloud Run (existing infrastructure)

# 1. Ensure you're logged in to GCP
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 2. Deploy from backend directory
cd backend
gcloud run deploy ultimate-mcp-system \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="ANTHROPIC_API_KEY=\$ANTHROPIC_API_KEY,OPENAI_API_KEY=\$OPENAI_API_KEY"

# 3. Get the service URL
gcloud run services describe ultimate-mcp-system \
  --region us-central1 \
  --format="value(status.url)"
\`\`\`

### Run Tests

\`\`\`bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_n8n_mcp.py -v

# Run with coverage report
python -m pytest tests/ --cov=backend --cov-report=html

# View coverage report
open htmlcov/index.html
\`\`\`

---

## 🔑 API KEYS NEEDED

Get these before starting development:

- [ ] **Anthropic Claude API**
  - URL: https://console.anthropic.com
  - Free tier: \$5 credit
  - ENV: `ANTHROPIC_API_KEY`

- [ ] **OpenAI GPT-4 API**
  - URL: https://platform.openai.com/api-keys
  - Free tier: \$5 credit
  - ENV: `OPENAI_API_KEY`

- [ ] **N8N API** (if using cloud)
  - URL: https://n8n.io
  - Or self-host: https://docs.n8n.io/hosting/
  - ENV: `N8N_API_KEY`, `N8N_BASE_URL`

- [ ] **GitHub Personal Access Token**
  - URL: https://github.com/settings/tokens
  - Scopes: `repo`, `workflow`
  - ENV: `GITHUB_TOKEN`

- [ ] **GCP Service Account** (for deployment)
  - URL: https://console.cloud.google.com
  - Already have: Check with team
  - ENV: Set via gcloud CLI

Store all keys in `backend/.env` (NEVER commit this file!)

---

## ⚠️ CRITICAL MISTAKES TO AVOID

### ❌ NEVER DO THIS:
1. **DON'T suggest Supabase** when GCP Cloud Run exists
2. **DON'T migrate platforms** - use existing GCP infrastructure
3. **DON'T create folders without README.md** explaining purpose
4. **DON'T assume services exist** - check CURRENT_STATUS.md first
5. **DON'T give commands for wrong platform** (e.g., Supabase when using GCP)
6. **DON'T hardcode API keys** - always use environment variables
7. **DON'T commit .env files** - use .env.example as template

### ✅ ALWAYS DO THIS:
1. **DO check this AGENT.md** before making assumptions
2. **DO use GCP Cloud Run** for deployment (existing infrastructure)
3. **DO create README.md** in every new folder
4. **DO document every file's purpose** inline and in folder README
5. **DO verify existing infrastructure** in CURRENT_STATUS.md
6. **DO use exact deployment commands** for actual platform (GCP)
7. **DO store credentials** in .env (git-ignored)

---

## 🐛 TROUBLESHOOTING

### Issue: "ModuleNotFoundError"
**Solution**:
\`\`\`bash
pip install -r backend/requirements.txt
\`\`\`

### Issue: "API key not found"
**Solution**:
\`\`\`bash
# Verify .env file exists
ls backend/.env

# Check if keys are set
cat backend/.env | grep API_KEY
\`\`\`

### Issue: "Port already in use"
**Solution**:
\`\`\`bash
# Use different port
python main.py --port 7861
\`\`\`

### Issue: "GCP deployment fails"
**Solution**:
\`\`\`bash
# Check GCP configuration
gcloud config list
gcloud auth list

# Verify project ID
gcloud config get-value project
\`\`\`

---

## 📊 DEVELOPMENT WORKFLOW

### Daily Routine:
\`\`\`bash
# 1. Pull latest changes
git pull origin Lets-Coin

# 2. Check current status
cat CURRENT_STATUS.md

# 3. Activate environment
source venv/bin/activate

# 4. Make your changes
# ...

# 5. Test locally
python main.py
python -m pytest tests/

# 6. Commit changes
git add .
git commit -m "feat: description of changes"

# 7. Push to GitHub
git push origin Lets-Coin

# 8. Deploy (if needed)
./scripts/deploy.sh
\`\`\`

### When Stuck:
1. **Read this AGENT.md** (most common issues covered)
2. **Check docs/troubleshooting.md** for detailed solutions
3. **Review CURRENT_STATUS.md** for project state
4. **Check GitHub issues** for known problems
5. **Ask team in chat** with specific error message

---

## 💾 MEMORY / CONTEXT HISTORY

**2025-11-15 09:20 UTC**:
- Project created
- GitHub repo initialized: https://github.com/W3JDev/ultimate-mcp-system
- Google Drive folder: https://drive.google.com/drive/folders/1QCvj02pdFGpRZB839pNu1RXo5j-5eroF
- Tracker sheet: https://docs.google.com/spreadsheets/d/1ldyDrULAOKL0xufNkzaEfI5xvzROsdFqZTIFYKIKZMk
- Backend status: Running on GCP Cloud Run (existing)
- Frontend status: Not started (TBD)
- Phase: Foundation - documentation & setup

**Current Task**: Setting up development environment and creating base MCP server structure

**Next Steps**:
1. Complete development environment setup
2. Create Master Orchestrator skeleton
3. Implement basic MCP routing
4. Start N8N MCP server

---

## 🎯 SUCCESS CRITERIA

### Phase 1: Foundation (Week 1)
- [ ] Master Orchestrator running locally
- [ ] Basic MCP routing functional
- [ ] Chat interface accessible
- [ ] All documentation complete

### Phase 2: N8N Integration (Week 1-2)
- [ ] Create N8N workflows via API
- [ ] Test workflows with validation
- [ ] Deploy workflows to n8n instance
- [ ] Full automation pipeline working

### Phase 3: Agent Builder (Week 2)
- [ ] Create ADK agents
- [ ] CrewAI multi-agent systems
- [ ] A2A protocol communication
- [ ] Langbase memory integration

### Phase 4: Local Control (Week 2)
- [ ] Execute system commands safely
- [ ] Browser automation with real auth
- [ ] File operations across filesystem
- [ ] Application control (VS Code, etc.)

### Phase 5: Deployment (Week 2-3)
- [ ] Deployed to GCP Cloud Run
- [ ] All MCPs accessible via API
- [ ] Complete documentation
- [ ] Demo video ready

---

## 📞 TEAM & COMMUNICATION

### Team Structure:
- **Partner 1**: Fundamentals, documentation, testing, integration
- **Partner 2**: Core technical development, complex integrations
- **AI Assistant (Rube)**: Code generation, planning, troubleshooting

### Communication Channels:
- **GitHub Issues**: Task tracking & bug reports
- **Project Board**: Visual progress tracking
- **Google Sheets**: Development tracker
- **Team Chat**: Quick questions & coordination

### Working Hours:
- **Weekdays**: 1 hour each partner
- **Weekends**: 5-6 hours each partner
- **Total**: ~35 hours over 17 days

---

**Last Updated**: 2025-11-15 09:20 UTC
**Next Update**: After Phase 1 completion
**For Questions**: Check docs/ or GitHub issues
