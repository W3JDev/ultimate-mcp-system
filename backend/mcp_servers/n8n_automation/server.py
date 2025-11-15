'''
N8N Automation MCP Server
Main Gradio MCP server for N8N workflow automation
'''
import os
import gradio as gr
from typing import Dict, Any, Optional
from loguru import logger
from .workflow_builder import WorkflowBuilder
from .workflow_tester import WorkflowTester
from .deployer import N8NDeployer

class N8NAutomationMCP:
    '''N8N Automation MCP Server'''

    def __init__(self):
        '''Initialize N8N MCP with all components'''
        self.builder = WorkflowBuilder()
        self.tester = WorkflowTester()
        self.deployer = N8NDeployer(
            api_key=os.getenv("N8N_API_KEY"),
            base_url=os.getenv("N8N_BASE_URL", "http://localhost:5678")
        )
        logger.info("🔄 N8N MCP initialized")

    def create_workflow(self, description: str) -> Dict[str, Any]:
        '''
        Create N8N workflow from natural language description

        Args:
            description: Natural language workflow description

        Returns:
            N8N workflow JSON
        '''
        logger.info(f"📝 Creating workflow: {description}")
        return self.builder.build_from_description(description)

    def test_workflow(self, workflow: Dict, test_data: Dict) -> Dict[str, Any]:
        '''
        Test workflow with validation

        Args:
            workflow: N8N workflow JSON
            test_data: Test input data

        Returns:
            Test results with validation
        '''
        logger.info("🧪 Testing workflow")
        return self.tester.run_test(workflow, test_data)

    def validate_outputs(self, test_result: Dict) -> Dict[str, Any]:
        '''
        Validate workflow output format

        Args:
            test_result: Test execution result

        Returns:
            Validation report
        '''
        logger.info("✅ Validating outputs")
        return self.tester.validate_outputs(test_result)

    def deploy_workflow(self, workflow: Dict) -> Dict[str, Any]:
        '''
        Deploy workflow to N8N instance

        Args:
            workflow: N8N workflow JSON

        Returns:
            Deployment result with URL
        '''
        logger.info("🚀 Deploying workflow")
        return self.deployer.deploy(workflow)

    def process(self, user_input: str) -> str:
        '''
        Process natural language request (called by Orchestrator)

        Args:
            user_input: User's natural language request

        Returns:
            Response string
        '''
        try:
            # Parse intent
            if "create" in user_input.lower() or "build" in user_input.lower():
                workflow = self.create_workflow(user_input)
                return f"✅ **Workflow Created!**\n\n```json\n{workflow}\n```\n\nReady to test or deploy!"

            elif "test" in user_input.lower():
                return "🧪 To test, provide workflow JSON and test data."

            elif "deploy" in user_input.lower():
                return "🚀 To deploy, provide workflow JSON."

            else:
                return self._get_help()

        except Exception as e:
            logger.error(f"N8N MCP error: {e}")
            return f"❌ Error: {str(e)}"

    def _get_help(self) -> str:
        '''Return help message'''
        return '''🔄 **N8N Automation MCP**

**Commands:**
- "Create a workflow that [description]"
- "Test this workflow with [test data]"
- "Deploy workflow to N8N"

**Examples:**
- "Create workflow: When GitHub PR merged → Send Slack message"
- "Build automation: New email → Extract data → Update Google Sheet"
- "Make workflow: Monitor RSS → Post to Twitter"
'''

# Gradio MCP Interface
def create_n8n_mcp_interface():
    '''Create Gradio interface for N8N MCP'''
    mcp = N8NAutomationMCP()

    with gr.Blocks() as interface:
        gr.Markdown("# 🔄 N8N Automation MCP")

        with gr.Tab("Create Workflow"):
            description = gr.Textbox(
                label="Describe your workflow",
                placeholder="When a GitHub PR is merged, send WhatsApp to team...",
                lines=3
            )
            create_btn = gr.Button("Create Workflow")
            workflow_output = gr.JSON(label="Generated Workflow")

            create_btn.click(
                mcp.create_workflow,
                inputs=[description],
                outputs=[workflow_output]
            )

        with gr.Tab("Test Workflow"):
            test_workflow_input = gr.JSON(label="Workflow JSON")
            test_data_input = gr.JSON(label="Test Data")
            test_btn = gr.Button("Run Test")
            test_output = gr.JSON(label="Test Results")

            test_btn.click(
                mcp.test_workflow,
                inputs=[test_workflow_input, test_data_input],
                outputs=[test_output]
            )

        with gr.Tab("Deploy"):
            deploy_workflow_input = gr.JSON(label="Workflow JSON")
            deploy_btn = gr.Button("Deploy to N8N")
            deploy_output = gr.JSON(label="Deployment Result")

            deploy_btn.click(
                mcp.deploy_workflow,
                inputs=[deploy_workflow_input],
                outputs=[deploy_output]
            )

    return interface

if __name__ == "__main__":
    # Can run standalone as MCP server
    interface = create_n8n_mcp_interface()
    interface.launch(mcp_server=True)
