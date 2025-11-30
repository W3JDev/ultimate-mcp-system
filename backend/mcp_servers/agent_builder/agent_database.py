"""
SQLite Agent Persistence - Store agents permanently
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger


class AgentDatabase:
    """Persistent storage for agents using SQLite"""

    def __init__(self, db_path: str = "backend/agents.db"):
        """Initialize database connection"""
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
        logger.success(f"✅ Agent Database initialized: {db_path}")

    def _create_tables(self):
        """Create database schema"""
        cursor = self.conn.cursor()
        
        # Agents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                agent_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                framework TEXT NOT NULL,
                config TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                deployed BOOLEAN DEFAULT 0,
                deployment_url TEXT,
                status TEXT DEFAULT 'active'
            )
        """)
        
        # Execution history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                user_message TEXT NOT NULL,
                response TEXT NOT NULL,
                success BOOLEAN NOT NULL,
                timestamp TEXT NOT NULL,
                execution_time_ms INTEGER,
                FOREIGN KEY (agent_id) REFERENCES agents(agent_id)
            )
        """)
        
        # Deployments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deployments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                deployment_type TEXT NOT NULL,
                deployment_url TEXT,
                workflow_id TEXT,
                deployed_at TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                FOREIGN KEY (agent_id) REFERENCES agents(agent_id)
            )
        """)
        
        self.conn.commit()
        logger.info("✅ Database tables created")

    def save_agent(self, agent_config: Dict[str, Any]) -> bool:
        """Save or update agent"""
        try:
            cursor = self.conn.cursor()
            
            now = datetime.utcnow().isoformat()
            agent_id = agent_config["agent_id"]
            
            # Check if exists
            cursor.execute("SELECT agent_id FROM agents WHERE agent_id = ?", (agent_id,))
            exists = cursor.fetchone()
            
            if exists:
                # Update
                cursor.execute("""
                    UPDATE agents
                    SET name = ?, framework = ?, config = ?, updated_at = ?
                    WHERE agent_id = ?
                """, (
                    agent_config["name"],
                    agent_config["framework"],
                    json.dumps(agent_config),
                    now,
                    agent_id
                ))
                logger.info(f"📝 Updated agent: {agent_id}")
            else:
                # Insert
                cursor.execute("""
                    INSERT INTO agents (agent_id, name, framework, config, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    agent_id,
                    agent_config["name"],
                    agent_config["framework"],
                    json.dumps(agent_config),
                    now,
                    now
                ))
                logger.success(f"💾 Saved new agent: {agent_id}")
            
            self.conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to save agent: {e}")
            self.conn.rollback()
            return False

    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent by ID"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM agents WHERE agent_id = ?", (agent_id,))
            row = cursor.fetchone()
            
            if row:
                agent_data = dict(row)
                agent_data["config"] = json.loads(agent_data["config"])
                return agent_data
            return None
            
        except Exception as e:
            logger.error(f"❌ Failed to get agent: {e}")
            return None

    def list_agents(self, framework: Optional[str] = None, status: str = "active") -> List[Dict[str, Any]]:
        """List all agents with optional filtering"""
        try:
            cursor = self.conn.cursor()
            
            if framework:
                cursor.execute(
                    "SELECT * FROM agents WHERE framework = ? AND status = ? ORDER BY created_at DESC",
                    (framework, status)
                )
            else:
                cursor.execute(
                    "SELECT * FROM agents WHERE status = ? ORDER BY created_at DESC",
                    (status,)
                )
            
            agents = []
            for row in cursor.fetchall():
                agent_data = dict(row)
                agent_data["config"] = json.loads(agent_data["config"])
                agents.append(agent_data)
            
            return agents
            
        except Exception as e:
            logger.error(f"❌ Failed to list agents: {e}")
            return []

    def delete_agent(self, agent_id: str) -> bool:
        """Delete agent (soft delete by marking inactive)"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE agents SET status = 'deleted', updated_at = ? WHERE agent_id = ?",
                (datetime.utcnow().isoformat(), agent_id)
            )
            self.conn.commit()
            logger.info(f"🗑️ Deleted agent: {agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to delete agent: {e}")
            return False

    def log_execution(
        self,
        agent_id: str,
        user_message: str,
        response: str,
        success: bool,
        execution_time_ms: int = 0
    ) -> bool:
        """Log agent execution"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO executions (agent_id, user_message, response, success, timestamp, execution_time_ms)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                agent_id,
                user_message,
                response,
                success,
                datetime.utcnow().isoformat(),
                execution_time_ms
            ))
            self.conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to log execution: {e}")
            return False

    def save_deployment(
        self,
        agent_id: str,
        deployment_type: str,
        deployment_url: str,
        workflow_id: Optional[str] = None
    ) -> bool:
        """Save deployment record"""
        try:
            cursor = self.conn.cursor()
            
            # Update agent
            cursor.execute("""
                UPDATE agents
                SET deployed = 1, deployment_url = ?, updated_at = ?
                WHERE agent_id = ?
            """, (deployment_url, datetime.utcnow().isoformat(), agent_id))
            
            # Insert deployment record
            cursor.execute("""
                INSERT INTO deployments (agent_id, deployment_type, deployment_url, workflow_id, deployed_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                agent_id,
                deployment_type,
                deployment_url,
                workflow_id,
                datetime.utcnow().isoformat()
            ))
            
            self.conn.commit()
            logger.success(f"🚀 Saved deployment for: {agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to save deployment: {e}")
            self.conn.rollback()
            return False

    def get_agent_stats(self, agent_id: str) -> Dict[str, Any]:
        """Get execution statistics for agent"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_executions,
                    SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_executions,
                    AVG(execution_time_ms) as avg_execution_time_ms,
                    MAX(timestamp) as last_execution
                FROM executions
                WHERE agent_id = ?
            """, (agent_id,))
            
            row = cursor.fetchone()
            return dict(row) if row else {}
            
        except Exception as e:
            logger.error(f"❌ Failed to get stats: {e}")
            return {}

    def close(self):
        """Close database connection"""
        self.conn.close()
        logger.info("🔌 Database connection closed")
