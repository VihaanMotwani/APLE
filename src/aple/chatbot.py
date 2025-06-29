from typing import List
from .models import LearningObjective
from .services.llm_service import LLMService
from .ui.console import ConsoleUI

class Chatbot:
    def __init__(self, topic: str, objectives: List[LearningObjective], llm_service: LLMService, ui: ConsoleUI):
        self.topic = topic
        self.learning_objectives = objectives
        self.llm_service = llm_service
        self.ui = ui
        self.conversation_history = []

    def run(self) -> list:
        while True:
            user_input = self.ui.get_chat_input()
            if user_input.lower() in ['exit', 'bye', 'quit']:
                self.ui.display_goodbye()
                break

            self.conversation_history.append({'role': 'user', 'content': user_input})
            
            aple_response = self.llm_service.get_chat_response(
                topic=self.topic,
                objectives=self.learning_objectives,
                user_input=user_input,
                history=self.conversation_history
            )
            
            self.conversation_history.append({'role': 'assistant', 'content': aple_response})
            self.ui.display_chatbot_response(aple_response)

        return self.conversation_history