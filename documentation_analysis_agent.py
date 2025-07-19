import markdown
from bs4 import BeautifulSoup
from data_creator_agent import Agent, ArchitectureEventType

class DocumentationAnalysisAgent(Agent):
    def __init__(self, name="DocumentationAnalysisAgent", message_bus=None, config=None):
        super().__init__(name=name, message_bus=message_bus, config=config)
        self.doc_file_extensions = self.config.get("doc_extensions", ['.md', '.txt', '.rst'])
        if self.message_bus:
            self.message_bus.subscribe(ArchitectureEventType.REPO_DATA_EXTRACTED, self)

    async def handle_message(self, msg):
        if msg.get("type") == ArchitectureEventType.REPO_DATA_EXTRACTED:
            print(f"{self.name}: Received repository data for '{msg.get('source_repo')}'. Analyzing documentation files...")

            repo_name = msg.get('source_repo')
            files_data = msg.get('data', [])

            for file_info in files_data:
                file_path = file_info.get("file_path")

                if any(file_path.endswith(ext) for ext in self.doc_file_extensions):
                    try:
                        analysis_result = self.analyze_documentation(file_info['content'])

                        self.send({
                            "type": ArchitectureEventType.ANALYZED_DOCUMENTATION,
                            "source_file": file_path,
                            "repo": repo_name,
                            "analysis": analysis_result
                        })
                    except Exception as e:
                        print(f"Error analyzing {file_path}: {e}")

    def analyze_documentation(self, content):
        """Converts markdown to plain text and extracts a summary."""
        # A more sophisticated implementation would parse sections, etc.
        html = markdown.markdown(content)
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text()
        summary = ' '.join(text.split()[:50]) + '...' # Simple summary

        return {"summary": summary, "full_text": text}
