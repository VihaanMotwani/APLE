from typing import List
from .base_agent import BaseAgent
from ..services.llm_service import LLMService
from ..utils import load_yaml
from ..models import EvaluationReport, Question

class Examiner(BaseAgent):
    def __init__(self, llm_service: LLMService):
        super().__init__(llm_service)
        agent_configs = load_yaml('config/agents.yaml')
        self.config = agent_configs['examiner']

    def execute(self, questionnaire: List[Question], assessment_results: list) -> EvaluationReport:
        system_prompt = f"""
You are the {self.config['role']}.
Your goal is to {self.config['goal']}.
Background: {self.config['backstory']}
You MUST output a single, valid JSON object and nothing else.
The JSON object must conform to the structure detailed in your goal.
"""
        evaluation_data_str = ""
        for i, question_data in enumerate(questionnaire):
            tutee_answer = assessment_results[i]['answer']
            evaluation_data_str += f"""
---
Question ID: {question_data.question_id}
Question: {question_data.question}
Correct Answer: {question_data.answer}
Tutee's Answer: {tutee_answer}
---
"""
        
        user_prompt = f"""
Please evaluate the following set of test data according to your instructions.
Use the scoring rubric (0=Incorrect, 1=Partial, 2=Correct) to calculate a final percentage score.
Provide concise justifications and overall remarks.

Here is the data to evaluate:
{evaluation_data_str}

Now, generate the complete JSON performance report.
"""
        
        report = self.llm_service.get_structured_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_model=EvaluationReport
        )
        return report