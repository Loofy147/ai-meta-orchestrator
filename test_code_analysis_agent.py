import asyncio
import unittest
from unittest.mock import MagicMock

from data_creator_agent import CentralMessageBus, ArchitectureEventType
from code_analysis_agent import CodeAnalysisAgent

class TestCodeAnalysisAgent(unittest.TestCase):

    def setUp(self):
        self.bus = CentralMessageBus()
        self.agent = CodeAnalysisAgent(message_bus=self.bus)

    def test_python_code_analysis(self):
        # Mock a subscriber to the ANALYZED_CODE_STRUCTURE event
        subscriber = MagicMock()
        subscriber.inbox = []
        self.bus.subscribe(ArchitectureEventType.ANALYZED_CODE_STRUCTURE, subscriber)

        # A sample python code file
        python_code = """
def hello(name):
    \"\"\"A simple function.\"\"\"
    print(f"Hello, {name}")

class Greeter:
    \"\"\"A simple class.\"\"\"
    def __init__(self, greeting):
        self.greeting = greeting
"""

        # The message to be handled by the agent
        msg = {
            "type": ArchitectureEventType.REPO_DATA_EXTRACTED,
            "source_repo": "test_repo",
            "data": [
                {"file_path": "greeter.py", "content": python_code}
            ]
        }

        # Run the agent's handler
        async def run_test():
            await self.agent.handle_message(msg)

        asyncio.run(run_test())

        # Check if the subscriber received a message
        self.assertEqual(len(subscriber.inbox), 1)
        analysis = subscriber.inbox[0]['analysis']
        self.assertEqual(len(analysis['functions']), 1)
        self.assertEqual(analysis['functions'][0]['name'], 'hello')
        self.assertEqual(len(analysis['classes']), 1)
        self.assertEqual(analysis['classes'][0]['name'], 'Greeter')

if __name__ == '__main__':
    unittest.main()
