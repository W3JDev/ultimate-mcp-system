# 🚀 Advanced Usage Examples

Complex examples demonstrating advanced features of the Ultimate MCP System.

## Example 1: Multi-Step Workflow with Error Handling

### Goal
Create a complex workflow with conditional logic, retries, and error notifications.

### Description
```
When new customer signs up:
1. Validate email format
2. Check if email exists in database
3. If new customer:
   a. Create Stripe customer
   b. Send welcome email
   c. Add to CRM
   d. If premium plan: Create subscription
4. If any step fails:
   a. Log error to database
   b. Send Slack alert to #errors
   c. Retry up to 3 times
5. On success: Send confirmation to customer
```

### Implementation

**Step 1**: Generate workflow
```python
import requests

response = requests.post(
    "http://localhost:7862/api/workflow/generate",
    json={
        "description": """
        Multi-step signup workflow:
        - Validate email
        - Check existing customer
        - Create Stripe customer
        - Send welcome email
        - Add to CRM
        - Create subscription if premium
        - Error handling with retries
        - Slack notifications
        """
    }
)

workflow = response.json()['workflow']
```

**Step 2**: Test with sample data
```python
test_data = {
    "email": "test@example.com",
    "name": "Test User",
    "plan": "premium"
}

response = requests.post(
    "http://localhost:7862/api/workflow/test",
    json={
        "workflow": workflow,
        "test_data": test_data
    }
)

print(response.json())
```

**Step 3**: Deploy to production
```python
response = requests.post(
    "http://localhost:7862/api/workflow/deploy",
    json={
        "workflow": workflow,
        "n8n_url": "https://n8n.example.com",
        "api_key": "your_api_key"
    }
)

workflow_id = response.json()['workflow_id']
print(f"Deployed: {workflow_id}")
```

---

## Example 2: Multi-Agent Research Team

### Goal
Create a team of AI agents that collaborate to research a topic.

### Architecture
```
Research Manager (Coordinator)
    ├── Web Researcher (Gathers data)
    ├── Data Analyst (Processes info)
    ├── Fact Checker (Verifies claims)
    └── Report Writer (Creates output)
```

### Implementation

**Step 1**: Create agents
```python
import requests

# Research Manager
manager = requests.post(
    "http://localhost:7863/api/agent/create",
    json={
        "name": "Research Manager",
        "framework": "crewai",
        "config": {
            "role": "Manager",
            "goal": "Coordinate research team",
            "backstory": "Experienced research coordinator",
            "model": "gpt-4"
        }
    }
).json()

# Web Researcher
researcher = requests.post(
    "http://localhost:7863/api/agent/create",
    json={
        "name": "Web Researcher",
        "framework": "crewai",
        "config": {
            "role": "Researcher",
            "goal": "Find relevant information online",
            "tools": ["web_search", "web_scraper"],
            "model": "gpt-4"
        }
    }
).json()

# Data Analyst
analyst = requests.post(
    "http://localhost:7863/api/agent/create",
    json={
        "name": "Data Analyst",
        "framework": "crewai",
        "config": {
            "role": "Analyst",
            "goal": "Process and structure data",
            "tools": ["data_processor"],
            "model": "claude-3-sonnet"
        }
    }
).json()

# Report Writer
writer = requests.post(
    "http://localhost:7863/api/agent/create",
    json={
        "name": "Report Writer",
        "framework": "crewai",
        "config": {
            "role": "Writer",
            "goal": "Create comprehensive reports",
            "tools": ["document_creator"],
            "model": "claude-3-opus"
        }
    }
).json()
```

**Step 2**: Define team tasks
```python
tasks = [
    {
        "agent": researcher['agent_id'],
        "description": "Research latest AI developments",
        "expected_output": "List of key findings"
    },
    {
        "agent": analyst['agent_id'],
        "description": "Analyze research findings",
        "expected_output": "Structured analysis"
    },
    {
        "agent": writer['agent_id'],
        "description": "Write executive summary",
        "expected_output": "Professional report"
    }
]
```

**Step 3**: Execute research
```python
# Team executes tasks sequentially
for task in tasks:
    response = requests.post(
        f"http://localhost:7863/api/agent/{task['agent']}/execute",
        json={
            "task": task['description'],
            "context": previous_results
        }
    )
    
    previous_results = response.json()['output']
    print(f"Task completed: {task['description']}")

print("Final Report:", previous_results)
```

---

## Example 3: RAG-Based Document Assistant

### Goal
Create an agent that answers questions from company documents.

### Implementation

**Step 1**: Prepare documents
```python
documents = [
    "/company/policies.pdf",
    "/company/handbook.pdf",
    "/company/procedures.pdf"
]

# Upload and index documents
response = requests.post(
    "http://localhost:7863/api/agent/create",
    json={
        "name": "Document Assistant",
        "framework": "langbase",
        "config": {
            "model": "claude-3-sonnet",
            "documents": documents,
            "chunk_size": 1000,
            "overlap": 200,
            "embedding_model": "text-embedding-ada-002"
        }
    }
)

agent_id = response.json()['agent_id']
```

**Step 2**: Query documents
```python
questions = [
    "What is our vacation policy?",
    "How do I submit expenses?",
    "What are the remote work guidelines?"
]

for question in questions:
    response = requests.post(
        f"http://localhost:7863/api/agent/{agent_id}/query",
        json={
            "query": question,
            "top_k": 3,  # Return top 3 relevant chunks
            "include_sources": True
        }
    )
    
    result = response.json()
    print(f"Q: {question}")
    print(f"A: {result['answer']}")
    print(f"Sources: {result['sources']}")
    print("---")
```

---

## Example 4: Automated Testing Pipeline

### Goal
Create a workflow that runs tests when code is pushed to GitHub.

### Implementation

```python
workflow_description = """
When code is pushed to GitHub:
1. Receive webhook from GitHub
2. Clone repository
3. Run unit tests
4. Run integration tests
5. If tests pass:
   a. Build Docker image
   b. Push to registry
   c. Deploy to staging
   d. Send success notification to Slack
6. If tests fail:
   a. Create GitHub issue
   b. Send failure notification with logs
   c. Alert on-call engineer
"""

# Generate and deploy
workflow = generate_workflow(workflow_description)
deploy_workflow(workflow)
```

---

## Example 5: System Monitoring and Auto-Healing

### Goal
Monitor system health and automatically fix common issues.

### Implementation

**Step 1**: Create monitoring workflow
```python
monitoring_workflow = """
Every 5 minutes:
1. Check system health:
   - CPU usage
   - Memory usage
   - Disk space
   - Network connectivity
   - Process status
2. If CPU > 90%:
   - Identify top processes
   - Kill non-essential processes
   - Send alert
3. If Disk > 90%:
   - Clean up old logs
   - Clear temp files
   - Send alert
4. If process crashed:
   - Restart process
   - Send alert
   - Log incident
5. Store metrics in database
"""
```

**Step 2**: Create auto-heal agent
```python
response = requests.post(
    "http://localhost:7863/api/agent/create",
    json={
        "name": "Auto-Heal Agent",
        "framework": "adk",
        "config": {
            "model": "claude-3-sonnet",
            "tools": [
                "system_monitor",
                "process_manager",
                "log_cleaner",
                "alert_sender"
            ],
            "instructions": """
            Monitor system health and automatically fix issues:
            - High CPU: Kill non-essential processes
            - High memory: Clear caches
            - Low disk: Clean old files
            - Process crash: Restart service
            Always log actions and send alerts.
            """
        }
    }
)
```

---

## Example 6: Browser Automation for Web Scraping

### Goal
Scrape multiple websites and aggregate data.

### Implementation

```python
import requests

# Define websites to scrape
targets = [
    {
        "url": "https://example.com/products",
        "selectors": {
            "title": ".product-title",
            "price": ".product-price",
            "availability": ".stock-status"
        }
    },
    {
        "url": "https://another-site.com/items",
        "selectors": {
            "title": "h2.item-name",
            "price": "span.price",
            "availability": "div.availability"
        }
    }
]

results = []

for target in targets:
    # Navigate to site
    requests.post(
        "http://localhost:7864/api/browser/navigate",
        json={"url": target['url']}
    )
    
    # Extract data
    response = requests.post(
        "http://localhost:7864/api/browser/extract",
        json={"selectors": target['selectors']}
    )
    
    data = response.json()
    results.append({
        "site": target['url'],
        "data": data
    })
    
    print(f"Scraped {target['url']}: {len(data)} items")

# Aggregate results
print(f"Total items scraped: {sum(len(r['data']) for r in results)}")
```

---

## Example 7: Intelligent File Organization

### Goal
Automatically organize files based on content and metadata.

### Implementation

```python
import requests

# Create file organization agent
response = requests.post(
    "http://localhost:7863/api/agent/create",
    json={
        "name": "File Organizer",
        "framework": "adk",
        "config": {
            "model": "claude-3-sonnet",
            "tools": [
                "file_reader",
                "file_mover",
                "content_analyzer"
            ],
            "instructions": """
            Organize files based on:
            - File type (documents, images, code, etc.)
            - Content analysis (topics, keywords)
            - Creation date
            - Size
            Create folders and move files appropriately.
            """
        }
    }
)

agent_id = response.json()['agent_id']

# Run organization
source_dir = "/Users/me/Downloads"
response = requests.post(
    f"http://localhost:7863/api/agent/{agent_id}/execute",
    json={
        "task": f"Organize all files in {source_dir}",
        "parameters": {
            "source": source_dir,
            "create_subfolders": True,
            "group_by": ["type", "date", "content"]
        }
    }
)

print(response.json()['summary'])
```

---

## Example 8: API Integration Hub

### Goal
Connect multiple APIs and sync data between them.

### Implementation

```python
sync_workflow = """
Every hour:
1. Fetch new Stripe customers
2. For each customer:
   a. Check if exists in CRM
   b. If not, create CRM record
   c. Add to Mailchimp list
   d. Create Airtable entry
   e. Send welcome email
3. Fetch CRM updates
4. Sync changes to all platforms
5. Log sync results
6. Send daily summary report
"""

# Generate workflow
workflow = generate_workflow(sync_workflow)

# Add error handling
workflow = add_error_handling(workflow, {
    "retry_count": 3,
    "retry_delay": 60,
    "on_failure": "send_alert"
})

# Deploy
deploy_workflow(workflow, environment="production")
```

---

## Example 9: Custom Business Logic

### Goal
Implement complex business rules with agents.

### Implementation

```python
# Create business rules agent
response = requests.post(
    "http://localhost:7863/api/agent/create",
    json={
        "name": "Discount Calculator",
        "framework": "adk",
        "config": {
            "model": "claude-3-sonnet",
            "tools": ["database_query", "calculation"],
            "instructions": """
            Calculate customer discount based on:
            - Purchase history (>$1000 = 10% off)
            - Account age (>1 year = 5% off)
            - Referrals (>5 = 10% off)
            - Current promotion (check database)
            - Max discount: 30%
            Return final discount percentage.
            """
        }
    }
)

# Use in workflow
customer_data = {
    "id": "cust_123",
    "total_purchases": 1500,
    "account_age_days": 400,
    "referrals": 7
}

discount = calculate_discount(agent_id, customer_data)
print(f"Discount: {discount}%")
```

---

## Example 10: End-to-End Automation

### Goal
Combine all MCP servers for complete automation.

### Implementation

```python
# 1. Create agents
support_agent = create_agent("Customer Support", framework="adk")
data_agent = create_agent("Data Processor", framework="langbase")

# 2. Create workflows
ticket_workflow = create_workflow("""
When support ticket received:
1. Use support_agent to analyze ticket
2. If can auto-resolve: Send response
3. If needs human: Assign to team member
4. Log in CRM
""")

# 3. Set up monitoring
monitor_workflow = create_workflow("""
Monitor system every minute:
- Check ticket queue
- Check agent health
- Check API limits
- Send alerts if needed
""")

# 4. Deploy everything
deploy_agent(support_agent)
deploy_agent(data_agent)
deploy_workflow(ticket_workflow)
deploy_workflow(monitor_workflow)

print("✅ Full automation deployed")
```

---

## Tips for Advanced Usage

### 1. Error Handling
Always include comprehensive error handling:
```python
try:
    result = execute_workflow(workflow)
except WorkflowError as e:
    log_error(e)
    send_alert(e)
    retry_with_exponential_backoff()
```

### 2. Testing
Test complex workflows in stages:
1. Test individual nodes
2. Test small chains
3. Test full workflow
4. Load test

### 3. Monitoring
Implement monitoring at every step:
- Execution time
- Success/failure rates
- Resource usage
- Cost tracking

### 4. Optimization
Optimize for performance:
- Cache repeated API calls
- Batch operations
- Parallelize when possible
- Use async processing

### 5. Security
Secure your automation:
- Validate all inputs
- Use environment variables for secrets
- Implement rate limiting
- Log all actions

## Next Steps

- Review [Best Practices](../guides/best-practices.md)
- Check [API Documentation](../api/rest-api.md)
- Explore [Integration Examples](integration-examples.md)
- Read [Architecture Guide](../architecture/system-architecture.md)

## Need Help?

- [Troubleshooting Guide](../guides/troubleshooting.md)
- [GitHub Issues](https://github.com/W3JDev/ultimate-mcp-system/issues)
- [Community Discussions](https://github.com/W3JDev/ultimate-mcp-system/discussions)
