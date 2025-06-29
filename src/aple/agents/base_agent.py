from abc import ABC, abstractmethod
from ..services.llm_service import LLMService

class BaseAgent(ABC):
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        self.config = {}

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    def _get_system_prompt(self) -> str:
        return f"""
        You are the {self.config['role']}.
        Your goal is to {self.config['goal']}.
        Background: {self.config['backstory']}
        """