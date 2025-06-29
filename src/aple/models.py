from pydantic import BaseModel, Field
from typing import List, Literal

class LearningObjective(BaseModel):
    objective_id: str
    statement: str

class Question(BaseModel):
    question_id: str
    question: str
    answer: str

class Benchmark(BaseModel):
    topic: str
    learning_objectives: List[LearningObjective]
    questionnaire: List[Question]

class QuestionEvaluation(BaseModel):
    question_id: str
    evaluation: Literal["Correct", "Incorrect", "Partially Correct"]
    score: int
    justification: str = Field(description="Brief justification for the evaluation.")

class OverallRemarks(BaseModel):
    strengths: str = Field(description="What the tutee understood well.")
    areas_for_improvement: str = Field(description="What the tutee got wrong and topics to revisit.")
    suggested_next_steps: str = Field(description="What the tutee can explore next to deepen their knowledge.")

class EvaluationReport(BaseModel):
    overall_score_percentage: float = Field(description="The final score as a percentage.")
    overall_remarks: OverallRemarks
    question_evaluations: List[QuestionEvaluation]