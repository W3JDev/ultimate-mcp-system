"""
End-to-end tests for complete workflows
"""

import time

import pytest
import requests


def check_server(port):
    """Check if a server is running on the given port"""
    try:
        response = requests.get(f"http://localhost:{port}/", timeout=2)
        return True
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return False


def all_servers_running():
    """Check if all required servers are running"""
    ports = [7860, 7862, 7863, 7864]
    return all(check_server(port) for port in ports)


skip_if_servers_not_running = pytest.mark.skipif(
    not all_servers_running(),
    reason="Requires all servers running (ports 7860, 7862, 7863, 7864)"
)


@pytest.mark.e2e
@skip_if_servers_not_running
class TestCompleteWorkflow:
    """Test complete end-to-end workflows"""

    BASE_URL = "http://localhost:7860"

    def test_workflow_creation_flow(self):
        """Test complete workflow creation from request to response"""
        # 1. Send request to orchestrator
        response = requests.post(
            f"{self.BASE_URL}/api/process",
            json={
                "message": "Create a workflow that sends email notifications",
                "context": {},
            },
        )

        assert response.status_code == 200
        data = response.json()

        # 2. Verify routing to N8N MCP
        assert (
            "workflow" in data.get("response", "").lower()
            or "n8n" in data.get("server", "").lower()
        )

    def test_agent_creation_flow(self):
        """Test complete agent creation flow"""
        # 1. Send request to orchestrator
        response = requests.post(
            f"{self.BASE_URL}/api/process",
            json={"message": "Create an AI agent for research tasks", "context": {}},
        )

        assert response.status_code == 200
        data = response.json()

        # 2. Verify routing to Agent Builder
        assert (
            "agent" in data.get("response", "").lower()
            or "agent_builder" in data.get("server", "").lower()
        )

    def test_system_control_flow(self):
        """Test system control command flow"""
        # 1. Send request to orchestrator
        response = requests.post(
            f"{self.BASE_URL}/api/process",
            json={"message": "Get system information", "context": {}},
        )

        assert response.status_code == 200
        data = response.json()

        # 2. Verify routing to Local Control
        assert (
            "system" in data.get("response", "").lower()
            or "local_control" in data.get("server", "").lower()
        )

    def test_multi_turn_conversation(self):
        """Test multi-turn conversation with context"""
        # Turn 1
        response1 = requests.post(
            f"{self.BASE_URL}/api/process",
            json={"message": "Create a workflow", "context": {}},
        )
        assert response1.status_code == 200

        # Turn 2 - Follow-up
        response2 = requests.post(
            f"{self.BASE_URL}/api/process",
            json={
                "message": "Now deploy it",
                "context": response1.json().get("context", {}),
            },
        )
        assert response2.status_code == 200


@pytest.mark.e2e
@skip_if_servers_not_running
class TestServerAvailability:
    """Test that all servers are available"""

    SERVERS = {
        "orchestrator": 7860,
        "n8n_mcp": 7862,
        "agent_builder": 7863,
        "local_control": 7864,
    }

    @pytest.mark.parametrize("server_name,port", SERVERS.items())
    def test_server_reachable(self, server_name, port):
        """Test that server is reachable"""
        try:
            response = requests.get(f"http://localhost:{port}/", timeout=5)
            assert response.status_code in [200, 404]  # 404 ok, server is running
        except requests.exceptions.ConnectionError:
            pytest.fail(f"{server_name} on port {port} is not reachable")

    @pytest.mark.parametrize("server_name,port", SERVERS.items())
    def test_server_health(self, server_name, port):
        """Test server health endpoint"""
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                assert "status" in data
        except requests.exceptions.ConnectionError:
            pytest.skip(f"{server_name} health endpoint not available")


@pytest.mark.e2e
@pytest.mark.skip(reason="Performance testing - run separately")
class TestPerformance:
    """Performance and load tests"""

    def test_response_time(self):
        """Test that response time is acceptable"""
        start = time.time()

        response = requests.post(
            "http://localhost:7860/api/process",
            json={"message": "test", "context": {}},
            timeout=10,
        )

        elapsed = time.time() - start

        assert response.status_code == 200
        assert elapsed < 5.0  # Should respond within 5 seconds

    def test_concurrent_requests(self):
        """Test handling concurrent requests"""
        import concurrent.futures

        def make_request():
            return requests.post(
                "http://localhost:7860/api/process",
                json={"message": "test", "context": {}},
                timeout=10,
            )

        # Send 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        # All requests should succeed
        assert all(r.status_code == 200 for r in results)
