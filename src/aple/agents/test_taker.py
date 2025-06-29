from .base_agent import BaseAgent
from ..services.llm_service import LLMService
from ..utils import load_yaml

class TestTaker(BaseAgent):
    def __init__(self, llm_service: LLMService):
        super().__init__(llm_service)
        agent_configs = load_yaml('config/agents.yaml')
        self.config = agent_configs['test_taker']

    def execute(self, knowledge_base: str, question_text: str) -> str:
        system_prompt = f"""
You are the {self.config['role']}.
Your goal is to {self.config['goal']}.
Background: {self.config['backstory']}
You MUST follow the instructions with absolute precision. If the answer is not in the provided text, you MUST state 'I have not been taught the answer to this question.'
"""
        user_prompt = f"CONTEXT - KNOWLEDGE BASE:\n---\n{knowledge_base}\n---\n\nBased ONLY on the context provided above, answer the following question.\n\nQuestion: {question_text}"

        return self.llm_service.get_text_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )