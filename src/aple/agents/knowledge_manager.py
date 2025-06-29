from .base_agent import BaseAgent
from ..services.llm_service import LLMService
from ..utils import load_yaml

class KnowledgeManager(BaseAgent):
    def __init__(self, llm_service: LLMService):
        super().__init__(llm_service)
        agent_configs = load_yaml('config/agents.yaml')
        self.config = agent_configs['knowledge_manager']
        self.task_configs = load_yaml('config/tasks.yaml')

    def execute(self, topic: str, conversation: list) -> str:
        # Rebuilding prompts exactly as in original main.py
        system_prompt = f"""
You are the {self.config['role']}.
Your goal is to {self.config['goal']}.
Background: {self.config['backstory']}
Your output MUST be a clean, well-structured Markdown document as described.
"""
        formatted_conversation = "\n".join(
            [f"{entry['role'].capitalize()}: {entry['content']}" for entry in conversation]
        )
        
        user_prompt = self.task_configs['knowledge_organization_task']['description'].format(
            topic=topic,
            conversation=formatted_conversation
        )
        
        return self.llm_service.get_text_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )