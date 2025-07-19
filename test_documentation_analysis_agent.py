import asyncio
import unittest
from unittest.mock import MagicMock

from data_creator_agent import CentralMessageBus, ArchitectureEventType
from documentation_analysis_agent import DocumentationAnalysisAgent

class TestDocumentationAnalysisAgent(unittest.TestCase):

    def setUp(self):
        self.bus = CentralMessageBus()
        self.agent = DocumentationAnalysisAgent(message_bus=self.bus)

    def test_markdown_analysis(self):
        # Mock a subscriber to the ANALYZED_DOCUMENTATION event
        subscriber = MagicMock()
        subscriber.inbox = []
        self.bus.subscribe(ArchitectureEventType.ANALYZED_DOCUMENTATION, subscriber)

        # A sample markdown file
        markdown_content = """
# My Project

This is a project.
"""

        # The message to be handled by the agent
        msg = {
            "type": ArchitectureEventType.REPO_DATA_EXTRACTED,
            "source_repo": "test_repo",
            "data": [
                {"file_path": "README.md", "content": markdown_content}
            ]
        }

        # Run the agent's handler
        async def run_test():
            await self.agent.handle_message(msg)

        asyncio.run(run_test())

        # Check if the subscriber received a message
        self.assertEqual(len(subscriber.inbox), 1)
        analysis = subscriber.inbox[0]['analysis']
        self.assertTrue("My Project" in analysis['full_text'])
        self.assertTrue(analysis['summary'].endswith('...'))

if __name__ == '__main__':
    unittest.main()
