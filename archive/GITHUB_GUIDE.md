# 📤 GitHub Upload Guide - W3J MCP Hub

## ⚠️ CRITICAL: Before Pushing to GitHub

### 1. Verify .gitignore is Protecting Secrets

```powershell
# Check .gitignore exists and contains .env
cat .gitignore | Select-String ".env"

# Test what will be committed (DRY RUN)
git status
git add --dry-run .
```

**Must be in `.gitignore`:**
```
.env
.env.local
.env.*.local
credentials.json
*_key.json
*.pem
*.key
```

### 2. Remove Any Committed Secrets (If Accidentally Pushed)

```powershell
# Check git history for secrets
git log --all --full-history --source -- .env

# If found, remove from history (DANGEROUS - backup first!)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (overwrites remote history)
git push origin --force --all
```

### 3. Scan for Exposed Secrets

```powershell
# Install git-secrets (one-time setup)
# Windows: Download from https://github.com/awslabs/git-secrets

# Scan repository
git secrets --scan

# Or manually search
git grep -E "(ANTHROPIC_API_KEY|OPENAI_API_KEY|COMPOSIO_API_KEY)" .

# Check staged files
git diff --staged | Select-String "API_KEY"
```

## First-Time Setup

### 1. Initialize Git Repository

```powershell
# If not already initialized
git init

# Configure user (first time only)
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### 2. Verify .gitignore

```powershell
# View .gitignore
cat .gitignore

# Should include:
# - .env
# - __pycache__/
# - *.pyc
# - .vscode/
# - logs/
# - .pytest_cache/
# - htmlcov/
```

### 3. Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `ultimate-mcp-system` (or your choice)
3. **Set to Private** (recommended for API keys)
4. Do NOT initialize with README (you have one)
5. Click "Create repository"

### 4. Add Remote and Push

```powershell
# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/ultimate-mcp-system.git

# Or if using SSH
git remote add origin git@github.com:YOUR_USERNAME/ultimate-mcp-system.git

# Verify remote
git remote -v

# Stage all files
git add .

# Review what will be committed (IMPORTANT!)
git status

# Commit
git commit -m "Initial commit: W3J MCP Hub with Composio integration"

# Push to GitHub
git push -u origin main

# If branch is named differently
git branch -M main
git push -u origin main
```

## Daily Workflow

### Make Changes and Commit

```powershell
# Check status
git status

# Stage specific files
git add backend/integrations/composio_integration.py
git add backend/mcp_servers/agent_builder/server.py

# Or stage all changes
git add .

# Commit with descriptive message
git commit -m "feat: Add Composio integration with 100+ tools"

# Push to GitHub
git push
```

### Good Commit Messages

```
feat: Add new feature
fix: Bug fix
docs: Documentation update
test: Add or modify tests
refactor: Code refactoring
chore: Maintenance tasks
style: Code formatting
perf: Performance improvement
```

Examples:
```powershell
git commit -m "feat: Integrate Composio MCP for Gmail/Slack/GitHub"
git commit -m "fix: Resolve ADK agent execution timeout"
git commit -m "docs: Add Docker deployment guide"
git commit -m "test: Add integration tests for Composio"
```

## Branch Management

### Create Feature Branch

```powershell
# Create and switch to new branch
git checkout -b feature/n8n-bidirectional

# Make changes, commit
git add .
git commit -m "feat: Add N8N bidirectional integration"

# Push branch to GitHub
git push -u origin feature/n8n-bidirectional

# Create Pull Request on GitHub
```

### Merge Feature Branch

```powershell
# Switch back to main
git checkout main

# Pull latest changes
git pull

# Merge feature branch
git merge feature/n8n-bidirectional

# Delete branch (local and remote)
git branch -d feature/n8n-bidirectional
git push origin --delete feature/n8n-bidirectional
```

## Updating from Remote

```powershell
# Fetch latest from GitHub
git fetch origin

# Pull and merge
git pull

# If conflicts, resolve manually then:
git add .
git commit -m "Merge: Resolve conflicts"
git push
```

## Managing Large Files

```powershell
# Install Git LFS (Large File Storage)
git lfs install

# Track large files (models, datasets, etc.)
git lfs track "*.pkl"
git lfs track "*.h5"
git lfs track "*.bin"

# Add .gitattributes
git add .gitattributes
git commit -m "chore: Configure Git LFS"
```

## Undo Changes

### Before Commit
```powershell
# Discard changes in working directory
git checkout -- backend/file.py

# Unstage file
git reset HEAD backend/file.py

# Discard all local changes
git reset --hard HEAD
```

### After Commit (Not Pushed)
```powershell
# Undo last commit, keep changes
git reset --soft HEAD~1

# Undo last commit, discard changes
git reset --hard HEAD~1
```

### After Push (Shared)
```powershell
# Revert specific commit (creates new commit)
git revert <commit-hash>
git push
```

## GitHub Actions (CI/CD)

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r backend/requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: python -m pytest tests/unit -v
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## Managing Secrets in GitHub

### Set Repository Secrets

1. Go to repository Settings
2. Click "Secrets and variables" → "Actions"
3. Click "New repository secret"
4. Add secrets:
   - `COMPOSIO_API_KEY`
   - `GEMINI_API_KEY`
   - `ANTHROPIC_API_KEY`
   - etc.

### Use in Workflows

```yaml
- name: Run integration tests
  env:
    COMPOSIO_API_KEY: ${{ secrets.COMPOSIO_API_KEY }}
    GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
  run: python -m pytest tests/integration -v
```

## Creating Releases

```powershell
# Tag a version
git tag -a v1.0.0 -m "Release v1.0.0: Composio integration complete"

# Push tags to GitHub
git push --tags
```

On GitHub:
1. Go to "Releases"
2. Click "Create a new release"
3. Select tag: `v1.0.0`
4. Title: "v1.0.0 - Composio Integration"
5. Description: Changelog
6. Publish release

## Repository Structure Best Practices

```
ultimate-mcp-system/
├── .github/
│   └── workflows/       # CI/CD pipelines
├── backend/             # Main application code
├── docs/                # Documentation
├── tests/               # Test suites
├── .gitignore          # ⚠️ CRITICAL: Protects secrets
├── .env.example        # Template without real keys
├── README.md           # Project overview
├── DOCKER_GUIDE.md     # Docker instructions
├── TESTING_GUIDE.md    # Testing instructions
└── GITHUB_GUIDE.md     # This file
```

## Common Issues

### Push Rejected
```powershell
# Pull first, then push
git pull --rebase
git push
```

### Large File Error
```powershell
# Use Git LFS
git lfs install
git lfs track "*.large"
git add .gitattributes
git commit -m "Add LFS tracking"
```

### Authentication Failed
```powershell
# Use Personal Access Token (PAT)
# GitHub → Settings → Developer settings → Personal access tokens → Generate new token

# Use token as password when pushing
git push
# Username: your_github_username
# Password: ghp_YourPersonalAccessToken
```

## Pre-Push Checklist

✅ `.env` is in `.gitignore`  
✅ No API keys in code  
✅ Sensitive files excluded  
✅ Tests passing  
✅ No large files (use LFS)  
✅ Meaningful commit message  
✅ Code reviewed locally  
✅ Documentation updated  

## Quick Reference

```powershell
# Status
git status

# Add changes
git add .

# Commit
git commit -m "message"

# Push
git push

# Pull
git pull

# View history
git log --oneline

# View diff
git diff

# Discard changes
git checkout -- file

# Undo commit
git reset --soft HEAD~1
```

## Next Steps

1. ✅ Verify .gitignore protects `.env`
2. 📤 Push to GitHub
3. 🔐 Set up repository secrets
4. 🤖 Configure GitHub Actions
5. 📝 Create first release tag
6. 🌐 Enable GitHub Pages (docs)
7. 🏆 Submit to hackathon!
