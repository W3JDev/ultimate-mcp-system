"""
GitHub MCP Integration
Provides GitHub repository operations
"""

from typing import Any, Dict

from .base_integration import BaseMCPIntegration


class GitHubMCPIntegration(BaseMCPIntegration):
    """Integration with GitHub MCP for repository operations"""

    def __init__(self, github_token: str = ""):
        """
        Initialize GitHub MCP integration

        Args:
            github_token: GitHub personal access token
        """
        # GitHub MCP server command
        server_command = ["npx", "-y", "@modelcontextprotocol/server-github"]
        super().__init__(server_command, "GitHub MCP")
        self.github_token = github_token

    def get_integration_name(self) -> str:
        """Get the integration name"""
        return "github"

    def create_repository(
        self, name: str, description: str = "", private: bool = False
    ) -> Dict[str, Any]:
        """
        Create a new GitHub repository

        Args:
            name: Repository name
            description: Repository description
            private: Whether repository should be private

        Returns:
            Repository creation result
        """
        return self.call_tool(
            "create_repository",
            {"name": name, "description": description, "private": private},
        )

    def create_issue(
        self, repo: str, title: str, body: str = "", labels: list = None
    ) -> Dict[str, Any]:
        """
        Create an issue in a repository

        Args:
            repo: Repository (owner/repo)
            title: Issue title
            body: Issue body
            labels: Issue labels

        Returns:
            Issue creation result
        """
        return self.call_tool(
            "create_issue",
            {"repo": repo, "title": title, "body": body, "labels": labels or []},
        )

    def create_pull_request(
        self, repo: str, title: str, head: str, base: str, body: str = ""
    ) -> Dict[str, Any]:
        """
        Create a pull request

        Args:
            repo: Repository (owner/repo)
            title: PR title
            head: Head branch
            base: Base branch
            body: PR body

        Returns:
            PR creation result
        """
        return self.call_tool(
            "create_pull_request",
            {"repo": repo, "title": title, "head": head, "base": base, "body": body},
        )

    def search_repositories(self, query: str) -> Dict[str, Any]:
        """
        Search for repositories

        Args:
            query: Search query

        Returns:
            Search results
        """
        return self.call_tool("search_repositories", {"query": query})

    def get_file_contents(self, repo: str, path: str, ref: str = "main") -> Dict[str, Any]:
        """
        Get file contents from a repository

        Args:
            repo: Repository (owner/repo)
            path: File path
            ref: Git reference (branch, tag, commit)

        Returns:
            File contents
        """
        return self.call_tool("get_file_contents", {"repo": repo, "path": path, "ref": ref})
