import asyncio
import os
import shutil
import unittest
import subprocess
from unittest.mock import MagicMock, AsyncMock, patch

# Import the classes from the script
from data_creator_agent import Agent, CentralMessageBus, ArchitectureEventType, DataCreatorAgent, extract_repo_data

class TestDataCreatorAgent(unittest.TestCase):

    def setUp(self):
        self.bus = CentralMessageBus()
        self.agent = DataCreatorAgent(message_bus=self.bus, config={"clone_dir": "./test_cloned_repos"})

    def tearDown(self):
        if os.path.exists("./test_cloned_repos"):
            shutil.rmtree("./test_cloned_repos")

    @patch('subprocess.run')
    def test_clone_and_extract_repo_success(self, mock_subprocess_run):
        # Mock the subprocess call to git clone
        mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        # Create a dummy repo with a file
        repo_path = "./test_cloned_repos/test_repo"
        os.makedirs(repo_path, exist_ok=True)
        with open(os.path.join(repo_path, "test_file.py"), "w") as f:
            f.write("print('hello')")

        # Mock the extract_repo_data function to return some data
        with patch('data_creator_agent.extract_repo_data') as mock_extract:
            mock_extract.return_value = [{"file": "test_file.py", "content": "print('hello')"}]

            # Run the agent's handler
            async def run_test():
                await self.agent.handle_message({
                    "type": "clone_and_extract_repo",
                    "repo_url": "https://github.com/user/test_repo.git"
                })

            # Mock a subscriber to the REPO_DATA_EXTRACTED event
            subscriber = Agent(name="Subscriber", message_bus=self.bus)
            self.bus.subscribe(ArchitectureEventType.REPO_DATA_EXTRACTED, subscriber)

            asyncio.run(run_test())

            # Check that the message was published and received
            self.assertEqual(len(subscriber.inbox), 1)
            self.assertEqual(subscriber.inbox[0]['type'], ArchitectureEventType.REPO_DATA_EXTRACTED)

    @patch('subprocess.run')
    def test_clone_and_extract_repo_failure(self, mock_subprocess_run):
        # Mock the subprocess call to git clone to fail
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, "git", stderr="fatal: repository not found")

        # Mock the orchestrator agent to receive the error message
        orchestrator = Agent(name="Orchestrator", message_bus=self.bus)
        self.bus.register_agent("Orchestrator", orchestrator.inbox)

        # Run the agent's handler
        async def run_test():
            await self.agent.handle_message({
                "type": "clone_and_extract_repo",
                "repo_url": "https://github.com/user/bad_repo.git"
            })

        asyncio.run(run_test())

        # Check that an error message was sent to the orchestrator
        self.assertEqual(len(orchestrator.inbox), 1)
        self.assertEqual(orchestrator.inbox[0]['type'], 'error')

if __name__ == '__main__':
    unittest.main()
