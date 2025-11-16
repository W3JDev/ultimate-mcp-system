# Virtual Environment Deprecation Notice

⚠️ **IMPORTANT: Virtual Environment Migration in Progress**

## Current State

This project currently has **two** Python virtual environments:

- `.venv/` - **NEW STANDARD** (Python 3.13 compatible)
- `venv/` - **DEPRECATED** (Legacy, will be removed)

## Action Required

### For Developers
1. **Stop using `venv/`** - Switch to `.venv/` immediately
2. **Update your activation commands**:
   ```powershell
   # OLD (deprecated)
   .\venv\Scripts\Activate.ps1
   
   # NEW (standard)
   .\.venv\Scripts\Activate.ps1
   ```

3. **Update your IDE settings** to point to `.venv/Scripts/python.exe`

### For AI Agents and Scripts
- All automation should reference `.venv/` paths
- Update any hardcoded `venv/` references
- Check activation scripts and deployment configurations

## Migration Timeline

- **Phase 1** (Current): Documentation and new standards established
- **Phase 2** (Next): All scripts updated to use `.venv`
- **Phase 3** (Future): `venv/` directory removed after confirmation

## What to Do Now

1. **Activate the correct environment**:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Verify you're using the right Python**:
   ```powershell
   where python
   # Should show: C:\...\ultimate-mcp-system\.venv\Scripts\python.exe
   ```

3. **Install dependencies in `.venv` if needed**:
   ```powershell
   pip install -r backend/requirements.txt
   pip install audioop-lts
   pip install 'huggingface_hub<1.0.0'
   ```

## Why This Change?

1. **Python 3.13 Compatibility**: New environment has proper audioop-lts support
2. **Standard Convention**: `.venv` is the Python community standard
3. **Tool Support**: Better IDE and tooling support for `.venv` naming
4. **Clarity**: Eliminates confusion about which environment to use

## Need Help?

- Check [Environment Setup Guide](docs/guides/environment_setup.md)
- Ensure you're following the new patterns in component `AGENT.md` files
- If you encounter issues, verify you're using `.venv` not `venv`

---

*This notice will be removed once `venv/` directory is deprecated and deleted.*