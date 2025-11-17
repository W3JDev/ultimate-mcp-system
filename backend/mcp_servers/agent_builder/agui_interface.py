"""
AGUI Interface - Agent GUI interfaces
"""

from typing import Any, Dict, List, Optional

from loguru import logger


class AGUIInterface:
    """AGUI integration for agent interfaces"""

    def __init__(self):
        """Initialize AGUI interface"""
        self.interfaces = {}
        logger.info("🖥️  AGUI interface initialized")

    def create_interface(
        self,
        name: str,
        agent_id: str,
        layout: str = "chat",
        theme: str = "light",
    ) -> Dict[str, Any]:
        """
        Create GUI interface for agent

        Args:
            name: Interface name
            agent_id: Associated agent ID
            layout: Interface layout (chat/dashboard/form)
            theme: Interface theme (light/dark)

        Returns:
            Interface configuration
        """
        logger.info(f"🖥️  Creating interface: {name}")

        interface_config = {
            "name": name,
            "agent_id": agent_id,
            "layout": layout,
            "theme": theme,
            "components": self._get_default_components(layout),
            "status": "active",
        }

        self.interfaces[name] = interface_config

        return {
            "success": True,
            "interface": interface_config,
            "message": f"Interface '{name}' created for agent {agent_id}",
        }

    def add_component(
        self,
        interface_name: str,
        component_type: str,
        config: Dict,
    ) -> Dict[str, Any]:
        """
        Add component to interface

        Args:
            interface_name: Interface name
            component_type: Component type (button/input/display/chart)
            config: Component configuration

        Returns:
            Add result
        """
        if interface_name not in self.interfaces:
            return {
                "success": False,
                "error": f"Interface '{interface_name}' not found",
            }

        interface = self.interfaces[interface_name]

        component = {
            "id": len(interface["components"]) + 1,
            "type": component_type,
            "config": config,
        }

        interface["components"].append(component)

        logger.info(f"➕ Added {component_type} to {interface_name}")

        return {
            "success": True,
            "component": component,
            "interface": interface_name,
        }

    def render_interface(self, interface_name: str) -> Dict[str, Any]:
        """
        Render interface

        Args:
            interface_name: Interface name

        Returns:
            Rendered interface HTML/JSON
        """
        if interface_name not in self.interfaces:
            return {
                "success": False,
                "error": f"Interface '{interface_name}' not found",
            }

        interface = self.interfaces[interface_name]

        html = self._generate_html(interface)

        logger.info(f"🎨 Rendered interface: {interface_name}")

        return {
            "success": True,
            "interface": interface_name,
            "html": html,
            "components": len(interface["components"]),
        }

    def handle_interaction(
        self,
        interface_name: str,
        component_id: int,
        action: str,
        data: Any,
    ) -> Dict[str, Any]:
        """
        Handle user interaction

        Args:
            interface_name: Interface name
            component_id: Component ID
            action: Action type (click/input/submit)
            data: Interaction data

        Returns:
            Interaction result
        """
        if interface_name not in self.interfaces:
            return {
                "success": False,
                "error": f"Interface '{interface_name}' not found",
            }

        logger.info(f"👆 Interaction on {interface_name}: {action}")

        return {
            "success": True,
            "interface": interface_name,
            "component_id": component_id,
            "action": action,
            "response": f"Processed {action} with data: {data}",
        }

    def _get_default_components(self, layout: str) -> List[Dict]:
        """Get default components for layout"""
        if layout == "chat":
            return [
                {"id": 1, "type": "chat_display", "config": {"height": 400}},
                {
                    "id": 2,
                    "type": "text_input",
                    "config": {"placeholder": "Type a message..."},
                },
                {"id": 3, "type": "send_button", "config": {"label": "Send"}},
            ]
        elif layout == "dashboard":
            return [
                {"id": 1, "type": "metrics_panel", "config": {}},
                {"id": 2, "type": "chart", "config": {"type": "line"}},
                {"id": 3, "type": "data_table", "config": {}},
            ]
        elif layout == "form":
            return [
                {"id": 1, "type": "text_input", "config": {"label": "Input"}},
                {"id": 2, "type": "textarea", "config": {"label": "Description"}},
                {"id": 3, "type": "submit_button", "config": {"label": "Submit"}},
            ]
        else:
            return []

    def _generate_html(self, interface: Dict) -> str:
        """Generate HTML for interface"""
        theme_class = f"theme-{interface['theme']}"
        layout_class = f"layout-{interface['layout']}"

        html = f"""
        <div class="agui-interface {theme_class} {layout_class}">
            <div class="agui-header">
                <h2>{interface['name']}</h2>
                <span class="agent-id">Agent: {interface['agent_id']}</span>
            </div>
            <div class="agui-body">
        """

        for component in interface["components"]:
            html += self._render_component(component)

        html += """
            </div>
        </div>
        """

        return html

    def _render_component(self, component: Dict) -> str:
        """Render individual component"""
        comp_type = component["type"]
        comp_id = component["id"]

        if comp_type == "chat_display":
            return f'<div id="comp-{comp_id}" class="chat-display"></div>'
        elif comp_type == "text_input":
            placeholder = component["config"].get("placeholder", "")
            return (
                f'<input id="comp-{comp_id}" type="text" placeholder="{placeholder}" />'
            )
        elif comp_type == "send_button":
            label = component["config"].get("label", "Send")
            return f'<button id="comp-{comp_id}">{label}</button>'
        else:
            return f'<div id="comp-{comp_id}" class="{comp_type}"></div>'

    def list_interfaces(self) -> Dict[str, Any]:
        """
        List all interfaces

        Returns:
            List of interfaces
        """
        return {
            "success": True,
            "count": len(self.interfaces),
            "interfaces": list(self.interfaces.values()),
        }
