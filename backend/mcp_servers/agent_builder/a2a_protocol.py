"""
A2A Protocol - Agent-to-Agent communication
"""

import json
from typing import Any, Dict, List, Optional

from loguru import logger


class A2AProtocol:
    """Agent-to-Agent communication protocol"""

    def __init__(self):
        """Initialize A2A protocol"""
        self.agents = {}
        self.message_queue = []
        logger.info("🔗 A2A protocol initialized")

    def register_agent(self, agent_id: str, agent_config: Dict) -> Dict[str, Any]:
        """
        Register agent for A2A communication

        Args:
            agent_id: Unique agent identifier
            agent_config: Agent configuration

        Returns:
            Registration result
        """
        logger.info(f"📝 Registering agent: {agent_id}")

        self.agents[agent_id] = {
            "id": agent_id,
            "name": agent_config.get("name", agent_id),
            "capabilities": agent_config.get("capabilities", []),
            "status": "active",
            "message_count": 0,
        }

        return {
            "success": True,
            "agent_id": agent_id,
            "message": f"Agent {agent_id} registered successfully",
        }

    def send_message(
        self,
        from_agent: str,
        to_agent: str,
        message: str,
        message_type: str = "request",
    ) -> Dict[str, Any]:
        """
        Send message between agents

        Args:
            from_agent: Sender agent ID
            to_agent: Recipient agent ID
            message: Message content
            message_type: Type of message (request/response/notification)

        Returns:
            Message delivery result
        """
        logger.info(f"📨 Message: {from_agent} → {to_agent}")

        if to_agent not in self.agents:
            return {
                "success": False,
                "error": f"Agent {to_agent} not registered",
            }

        message_obj = {
            "id": len(self.message_queue) + 1,
            "from": from_agent,
            "to": to_agent,
            "type": message_type,
            "content": message,
            "status": "delivered",
        }

        self.message_queue.append(message_obj)
        self.agents[from_agent]["message_count"] += 1
        self.agents[to_agent]["message_count"] += 1

        return {
            "success": True,
            "message_id": message_obj["id"],
            "status": "delivered",
        }

    def broadcast_message(
        self, from_agent: str, message: str, exclude: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Broadcast message to all agents

        Args:
            from_agent: Sender agent ID
            message: Message content
            exclude: Optional list of agent IDs to exclude

        Returns:
            Broadcast result
        """
        exclude = exclude or []
        recipients = [
            agent_id
            for agent_id in self.agents.keys()
            if agent_id != from_agent and agent_id not in exclude
        ]

        logger.info(f"📢 Broadcasting from {from_agent} to {len(recipients)} agents")

        results = []
        for recipient in recipients:
            result = self.send_message(from_agent, recipient, message, "broadcast")
            results.append(result)

        return {
            "success": True,
            "recipients": len(recipients),
            "results": results,
        }

    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """
        Get agent status and statistics

        Args:
            agent_id: Agent identifier

        Returns:
            Agent status
        """
        if agent_id not in self.agents:
            return {"success": False, "error": f"Agent {agent_id} not found"}

        return {
            "success": True,
            "agent": self.agents[agent_id],
        }

    def list_agents(self) -> Dict[str, Any]:
        """
        List all registered agents

        Returns:
            List of agents
        """
        return {
            "success": True,
            "count": len(self.agents),
            "agents": list(self.agents.values()),
        }

    def create_agent_group(
        self, group_name: str, agent_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Create group of agents for coordinated tasks

        Args:
            group_name: Group name
            agent_ids: List of agent IDs

        Returns:
            Group creation result
        """
        logger.info(f"👥 Creating agent group: {group_name}")

        # Validate all agents exist
        invalid_agents = [aid for aid in agent_ids if aid not in self.agents]
        if invalid_agents:
            return {
                "success": False,
                "error": f"Invalid agents: {invalid_agents}",
            }

        group = {
            "name": group_name,
            "agents": agent_ids,
            "created": True,
        }

        return {
            "success": True,
            "group": group,
            "message": f"Group '{group_name}' created with {len(agent_ids)} agents",
        }

    def coordinate_task(self, task: str, agent_ids: List[str]) -> Dict[str, Any]:
        """
        Coordinate multi-agent task

        Args:
            task: Task description
            agent_ids: Agents to coordinate

        Returns:
            Coordination result
        """
        logger.info(f"🎯 Coordinating task across {len(agent_ids)} agents")

        results = []
        for agent_id in agent_ids:
            if agent_id in self.agents:
                result = {
                    "agent_id": agent_id,
                    "task": task,
                    "status": "assigned",
                }
                results.append(result)

        return {
            "success": True,
            "task": task,
            "agents": len(results),
            "results": results,
        }
