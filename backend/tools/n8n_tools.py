"""
N8N Automation MCP Tools
Tools for workflow creation, testing, and deployment
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp_servers" / "n8n_automation"))

from loguru import logger
from .base import MCPTool, ToolSchema, ToolParameter

# Import N8N components
try:
    from mcp_servers.n8n_automation.workflow_builder import WorkflowBuilder
    from mcp_servers.n8n_automation.workflow_tester import WorkflowTester
    from mcp_servers.n8n_automation.deployer import N8NDeployer
except ImportError as e:
    logger.warning(f"⚠️ N8N components import failed: {e}")
    WorkflowBuilder = None
    WorkflowTester = None
    N8NDeployer = None


# === Tool: Create Workflow ===
def create_workflow_handler(description: str) -> Dict[str, Any]:
    """
    Create N8N workflow from natural language description
    
    Args:
        description: Natural language workflow description
        
    Returns:
        N8N workflow JSON
    """
    if WorkflowBuilder is None:
        return {"error": "N8N WorkflowBuilder not available"}
    
    builder = WorkflowBuilder()
    workflow = builder.build_from_description(description)
    return workflow


create_workflow_tool = MCPTool(
    schema=ToolSchema(
        name="create_n8n_workflow",
        display_name="Create N8N Workflow",
        description="Create an N8N workflow from natural language description",
        category="n8n",
        parameters=[
            ToolParameter(
                name="description",
                type="string",
                description="Natural language description of the workflow (e.g., 'When GitHub PR merged, send Slack message')",
                required=True
            )
        ],
        returns="N8N workflow JSON object",
        examples=[
            "Create workflow: When GitHub PR is merged, send Slack notification",
            "Build automation: New email arrives → Extract data → Update Google Sheet",
            "Make workflow: Monitor RSS feed → Filter by keyword → Post to Twitter"
        ]
    ),
    handler=create_workflow_handler
)


# === Tool: Test Workflow ===
def test_workflow_handler(workflow: Dict, test_data: Dict) -> Dict[str, Any]:
    """
    Test an N8N workflow with validation
    
    Args:
        workflow: N8N workflow JSON
        test_data: Test input data
        
    Returns:
        Test results with validation report
    """
    if WorkflowTester is None:
        return {"error": "N8N WorkflowTester not available"}
    
    tester = WorkflowTester()
    result = tester.run_test(workflow, test_data)
    return result


test_workflow_tool = MCPTool(
    schema=ToolSchema(
        name="test_n8n_workflow",
        display_name="Test N8N Workflow",
        description="Test an N8N workflow with sample data and validation",
        category="n8n",
        parameters=[
            ToolParameter(
                name="workflow",
                type="object",
                description="N8N workflow JSON to test",
                required=True
            ),
            ToolParameter(
                name="test_data",
                type="object",
                description="Sample input data for testing",
                required=True
            )
        ],
        returns="Test execution results with validation report",
        examples=[
            "Test workflow with sample GitHub webhook data",
            "Validate workflow outputs match expected format"
        ]
    ),
    handler=test_workflow_handler
)


# === Tool: Deploy Workflow ===
def deploy_workflow_handler(workflow: Dict, n8n_url: str = None, api_key: str = None) -> Dict[str, Any]:
    """
    Deploy workflow to N8N instance
    
    Args:
        workflow: N8N workflow JSON
        n8n_url: N8N instance URL (optional, uses env var)
        api_key: N8N API key (optional, uses env var)
        
    Returns:
        Deployment result with workflow URL
    """
    if N8NDeployer is None:
        return {"error": "N8N Deployer not available"}
    
    # Use provided values or environment variables
    n8n_url = n8n_url or os.getenv("N8N_BASE_URL", "http://localhost:5678")
    api_key = api_key or os.getenv("N8N_API_KEY")
    
    deployer = N8NDeployer(api_key=api_key, base_url=n8n_url)
    result = deployer.deploy(workflow)
    return result


deploy_workflow_tool = MCPTool(
    schema=ToolSchema(
        name="deploy_n8n_workflow",
        display_name="Deploy N8N Workflow",
        description="Deploy a workflow to N8N instance",
        category="n8n",
        parameters=[
            ToolParameter(
                name="workflow",
                type="object",
                description="N8N workflow JSON to deploy",
                required=True
            ),
            ToolParameter(
                name="n8n_url",
                type="string",
                description="N8N instance URL (defaults to N8N_BASE_URL env var)",
                required=False
            ),
            ToolParameter(
                name="api_key",
                type="string",
                description="N8N API key (defaults to N8N_API_KEY env var)",
                required=False
            )
        ],
        returns="Deployment result with workflow ID and URL",
        examples=[
            "Deploy workflow to production N8N instance",
            "Push workflow to N8N at https://n8n.company.com"
        ]
    ),
    handler=deploy_workflow_handler
)


# === Tool: Validate Workflow Outputs ===
def validate_workflow_handler(test_result: Dict) -> Dict[str, Any]:
    """
    Validate workflow test outputs
    
    Args:
        test_result: Test execution result
        
    Returns:
        Validation report
    """
    if WorkflowTester is None:
        return {"error": "N8N WorkflowTester not available"}
    
    tester = WorkflowTester()
    validation = tester.validate_outputs(test_result)
    return validation


validate_workflow_tool = MCPTool(
    schema=ToolSchema(
        name="validate_n8n_workflow",
        display_name="Validate N8N Workflow",
        description="Validate workflow test outputs match expected format",
        category="n8n",
        parameters=[
            ToolParameter(
                name="test_result",
                type="object",
                description="Test execution result to validate",
                required=True
            )
        ],
        returns="Validation report with pass/fail status",
        examples=[
            "Validate that workflow outputs are correctly formatted",
            "Check workflow test results for errors"
        ]
    ),
    handler=validate_workflow_handler
)


# Export all N8N tools
N8N_TOOLS = [
    create_workflow_tool,
    test_workflow_tool,
    deploy_workflow_tool,
    validate_workflow_tool
]
