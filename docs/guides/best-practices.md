# 🎯 Best Practices

Guidelines for optimal usage of the Ultimate MCP System.

## General Principles

### 1. Start Simple, Then Scale
```
❌ Bad: Build complex multi-agent system on day 1
✅ Good: Start with single workflow, add complexity incrementally
```

### 2. Test Everything
```
❌ Bad: Deploy directly to production
✅ Good: Test locally → staging → production
```

### 3. Monitor and Log
```
❌ Bad: Hope everything works
✅ Good: Log all actions, monitor metrics, set up alerts
```

### 4. Secure by Default
```
❌ Bad: Hardcode API keys, expose ports publicly
✅ Good: Use environment variables, limit access, implement authentication
```

### 5. Document Your Work
```
❌ Bad: Complex workflow with no documentation
✅ Good: Document purpose, inputs, outputs, error cases
```

---

## Workflow Best Practices

### Naming Conventions

**Good Names**:
```
✅ "github-issue-to-slack-notification"
✅ "customer-signup-stripe-crm-sync"
✅ "daily-database-backup-to-s3"
```

**Bad Names**:
```
❌ "workflow1"
❌ "test"
❌ "my_workflow"
```

### Structure

**Clear Flow**:
```
Trigger → Validation → Action(s) → Success Handler → Error Handler
```

**Example**:
```python
workflow = {
    "trigger": "webhook",
    "nodes": [
        {"type": "validate", "check": "email_format"},
        {"type": "action", "do": "create_customer"},
        {"type": "success", "do": "send_confirmation"},
        {"type": "error", "do": "log_and_alert"}
    ]
}
```

### Error Handling

**Always Include**:
1. Validation at entry point
2. Try/catch blocks
3. Retry logic
4. Fallback actions
5. Error notifications
6. Logging

**Example**:
```python
workflow_description = """
When webhook received:
1. Validate payload (required: email, name)
2. Try to create user:
   - Retry up to 3 times if fails
   - Wait 5 seconds between retries
3. If all retries fail:
   - Log error to database
   - Send Slack alert
   - Queue for manual review
4. If succeeds:
   - Send confirmation email
   - Log success
"""
```

### Performance

**Optimization Tips**:
- Use batch operations when possible
- Implement caching for repeated data
- Set appropriate timeouts
- Limit payload sizes
- Use pagination for large datasets

**Example**:
```python
# Bad: Process 1000 items individually
for item in items:
    process(item)  # 1000 API calls

# Good: Batch process
batch_process(items, batch_size=100)  # 10 API calls
```

---

## Agent Best Practices

### Model Selection

**Choose Based on Task**:

| Task | Recommended Model | Reasoning |
|------|------------------|-----------|
| Simple Q&A | claude-3-haiku | Fast, cost-effective |
| General purpose | claude-3-sonnet | Balanced quality/cost |
| Complex reasoning | claude-3-opus, gpt-4 | Highest quality |
| Code generation | gpt-4, claude-3-opus | Best code quality |

### Temperature Settings

```python
# Factual tasks (support, data extraction)
temperature = 0.0 - 0.3

# General purpose (chatbots, assistants)
temperature = 0.4 - 0.7

# Creative tasks (writing, brainstorming)
temperature = 0.8 - 1.0
```

### System Prompts

**Good System Prompt**:
```
You are a helpful customer support agent for Acme Corp.

Your responsibilities:
- Answer product questions
- Help with account issues
- Escalate to human if needed

Guidelines:
- Be professional and friendly
- Never share sensitive data
- Cite sources when possible
- Admit when you don't know

Available tools:
- search_knowledge_base()
- get_order_status()
- escalate_to_human()
```

**Bad System Prompt**:
```
You are an AI assistant.
```

### Context Management

**Keep Context Relevant**:
```python
# Bad: Include everything
context = full_conversation_history  # 10,000 tokens

# Good: Include only relevant
context = last_5_messages + important_facts  # 500 tokens
```

---

## System Automation Best Practices

### Command Safety

**Safe Commands**:
```bash
✅ ls -la
✅ cat file.txt
✅ df -h
✅ ps aux
✅ curl https://api.example.com
```

**Dangerous Commands (Avoid)**:
```bash
❌ rm -rf /
❌ chmod 777 -R /
❌ dd if=/dev/zero of=/dev/sda
❌ :(){ :|:& };:
```

### Sandboxing

**Always**:
- Run with minimal permissions
- Limit file system access
- Set timeouts
- Validate inputs
- Log all actions

**Example**:
```python
def execute_safe(command):
    # Validate command
    if not is_safe(command):
        raise SecurityError("Unsafe command")
    
    # Run with timeout
    result = subprocess.run(
        command,
        timeout=30,
        capture_output=True,
        cwd="/safe/directory"
    )
    
    # Log execution
    log_command(command, result)
    
    return result
```

### Browser Automation

**Best Practices**:
- Use headless mode for better performance
- Set explicit waits, not sleep()
- Handle popups and cookies
- Take screenshots for debugging
- Clean up browser instances

**Example**:
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    try:
        # Navigate with timeout
        page.goto(url, wait_until="networkidle", timeout=30000)
        
        # Wait for element
        page.wait_for_selector(".content", timeout=10000)
        
        # Take screenshot for debugging
        page.screenshot(path="debug.png")
        
        # Extract data
        data = page.evaluate("() => document.querySelector('.content').textContent")
        
    finally:
        # Always cleanup
        browser.close()
```

---

## Security Best Practices

### API Keys

**Storage**:
```python
# Bad: Hardcoded
api_key = "sk-ant-api03-xxx"

# Good: Environment variables
import os
api_key = os.getenv("ANTHROPIC_API_KEY")
```

**Rotation**:
- Rotate every 90 days
- Use different keys for dev/staging/prod
- Immediately revoke if compromised

### Access Control

**Implement**:
- Authentication for all endpoints
- Role-based access control
- IP whitelisting (if applicable)
- Rate limiting

**Example**:
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/api/workflow")
async def create_workflow(token: str = Depends(security)):
    if not verify_token(token):
        raise HTTPException(status_code=401)
    # Process request
```

### Data Privacy

**Always**:
- Encrypt sensitive data at rest
- Use HTTPS for all communications
- Don't log sensitive information
- Comply with GDPR/CCPA
- Implement data retention policies

---

## Monitoring Best Practices

### Metrics to Track

**System Metrics**:
- Request count and rate
- Response times (p50, p95, p99)
- Error rates
- Resource usage (CPU, memory, disk)

**Business Metrics**:
- Workflows executed
- Agents created
- API calls made
- Cost per operation

### Logging Levels

```python
# DEBUG: Detailed diagnostic info
logger.debug(f"Processing item {item_id} with params {params}")

# INFO: General informational messages
logger.info(f"Workflow {workflow_id} completed successfully")

# WARNING: Something unexpected but not an error
logger.warning(f"API rate limit approaching: {current_rate}/{limit}")

# ERROR: Something failed
logger.error(f"Failed to process request: {error}")

# CRITICAL: System is in bad state
logger.critical(f"Database connection lost, system halted")
```

### Alerting

**Set Up Alerts For**:
- Error rate > 5%
- Response time > 5 seconds
- API rate limit > 80%
- Disk space < 10%
- Memory usage > 90%

**Alert Channels**:
- Slack for team notifications
- Email for summaries
- PagerDuty for critical issues
- SMS for on-call engineers

---

## Cost Optimization

### API Usage

**Strategies**:
1. **Cache responses**: Don't call AI for same query twice
2. **Batch requests**: Combine when possible
3. **Right-size models**: Use smaller models when appropriate
4. **Implement rate limiting**: Prevent runaway costs

**Example**:
```python
from functools import lru_cache
from datetime import timedelta

@lru_cache(maxsize=1000)
def get_ai_response(query: str) -> str:
    # This will cache for identical queries
    return ai_client.generate(query)
```

### Resource Management

**Best Practices**:
- Shut down unused servers
- Use auto-scaling
- Implement request queuing
- Clean up old data regularly

---

## Testing Best Practices

### Unit Tests

**Test**:
- Individual functions
- Edge cases
- Error conditions
- Input validation

**Example**:
```python
def test_memory_manager():
    memory = MemoryManager()
    memory.add_message("user", "Hello")
    
    assert len(memory.short_term) == 1
    assert memory.short_term[0]["content"] == "Hello"
    
    # Test max length
    for i in range(20):
        memory.add_message("user", f"Message {i}")
    
    assert len(memory.short_term) == 10  # Max limit
```

### Integration Tests

**Test**:
- API endpoints
- Database connections
- External service integrations
- Authentication flows

### End-to-End Tests

**Test**:
- Complete user flows
- Multi-server interactions
- Error recovery
- Performance under load

---

## Deployment Best Practices

### Environment Strategy

```
Development → Staging → Production
```

**Development**:
- Use test API keys
- Enable debug logging
- No rate limiting
- Frequent deploys

**Staging**:
- Production-like data
- Production API keys (separate)
- Same infrastructure as prod
- Test before prod deploy

**Production**:
- Real data
- Production API keys
- High availability
- Blue-green deployments

### Docker Best Practices

**Dockerfile**:
```dockerfile
# Use specific versions, not latest
FROM python:3.11-slim

# Run as non-root user
RUN useradd -m appuser
USER appuser

# Copy only requirements first (better caching)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Then copy code
COPY . .

# Health check
HEALTHCHECK --interval=30s CMD curl -f http://localhost:7860/health

CMD ["python", "backend/main.py"]
```

### CI/CD

**Pipeline**:
1. Lint code (black, flake8, isort)
2. Run unit tests
3. Build Docker image
4. Run integration tests
5. Security scan
6. Deploy to staging
7. Run E2E tests
8. Deploy to production (manual approval)

---

## Documentation Best Practices

### What to Document

**For Each Workflow**:
- Purpose
- Trigger conditions
- Expected inputs
- Expected outputs
- Error scenarios
- Dependencies

**For Each Agent**:
- Capabilities
- Limitations
- Best use cases
- Example queries
- Configuration options

### Code Comments

**When to Comment**:
```python
# Good: Explain why, not what
# Use exponential backoff to avoid overwhelming the API
retry_delay = 2 ** attempt

# Bad: State the obvious
# Increment i by 1
i += 1
```

---

## Maintenance Best Practices

### Regular Tasks

**Daily**:
- Check error logs
- Monitor resource usage
- Review alerts

**Weekly**:
- Review metrics and trends
- Update dependencies
- Test backups

**Monthly**:
- Security audit
- Cost review
- Performance optimization
- Documentation updates

**Quarterly**:
- Rotate API keys
- Review architecture
- Capacity planning
- Disaster recovery drill

---

## Common Pitfalls to Avoid

### 1. Not Handling Errors
```python
# Bad
result = api_call()
process(result)

# Good
try:
    result = api_call()
    process(result)
except APIError as e:
    log_error(e)
    retry_with_backoff()
```

### 2. Ignoring Timeouts
```python
# Bad
response = requests.get(url)

# Good
response = requests.get(url, timeout=30)
```

### 3. Not Validating Input
```python
# Bad
def create_user(email):
    return database.create(email)

# Good
def create_user(email):
    if not is_valid_email(email):
        raise ValueError("Invalid email")
    return database.create(email)
```

### 4. Exposing Secrets
```python
# Bad
logger.info(f"API key: {api_key}")

# Good
logger.info("API key configured")
```

### 5. Not Using Version Control
```
❌ workflow_final_v2_REAL_final.json
✅ git commit -m "Add email notification workflow"
```

---

## Quick Reference Checklist

### Before Deploying

- [ ] All tests passing
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Secrets in environment variables
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Monitoring set up
- [ ] Backups configured
- [ ] Rollback plan ready

### After Deploying

- [ ] Verify deployment successful
- [ ] Check logs for errors
- [ ] Monitor metrics
- [ ] Test critical paths
- [ ] Update status page
- [ ] Notify team

---

## Related Documentation

- [User Guide](user-guide.md)
- [Troubleshooting Guide](troubleshooting.md)
- [API Documentation](../api/rest-api.md)
- [Architecture Guide](../architecture/system-architecture.md)
