import os
from ..services.llm_service import LLMService
from ..agents.knowledge_manager import KnowledgeManager
from ..agents.test_taker import TestTaker
from ..agents.examiner import Examiner
from ..chatbot import Chatbot
from ..utils import write_json_file, write_markdown_file
from ..models import EvaluationReport

class ApleSession:
    def __init__(self, topic: str, ui):
        self.topic = topic
        self.ui = ui
        self.llm_service = LLMService()
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)

        self.knowledge_manager = KnowledgeManager(self.llm_service)
        self.test_taker = TestTaker(self.llm_service)
        self.examiner = Examiner(self.llm_service)

        self.benchmark = None
        self.conversation = []
        self.knowledge_base = ""
        self.assessment_results = []
        self.evaluation_report = None

    def run(self):
        self._generate_benchmark()
        self._run_tutoring_chat()
        self._synthesize_knowledge_base()
        self._run_assessment()
        self._evaluate_answers()

    def _generate_benchmark(self):
        self.ui.show_progress("Step 1/5: Generating benchmark and learning objectives...")
        self.benchmark = self.llm_service.create_benchmark(self.topic)
        write_json_file(
            os.path.join(self.output_dir, "benchmark.json"),
            self.benchmark.model_dump()
        )
        self.ui.show_progress("Benchmark created successfully.")

    def _run_tutoring_chat(self):
        self.ui.show_progress("\nStep 2/5: Initializing Socratic chat session...")
        self.ui.display_chat_prompt()
        chatbot = Chatbot(self.topic, self.benchmark.learning_objectives, self.llm_service, self.ui)
        self.conversation = chatbot.run()

    def _synthesize_knowledge_base(self):
        self.ui.show_progress("\nStep 3/5: Synthesizing conversation into a knowledge base...")
        self.knowledge_base = self.knowledge_manager.execute(
            topic=self.topic,
            conversation=self.conversation
        )
        write_markdown_file(
            os.path.join(self.output_dir, "knowledge_base.md"),
            self.knowledge_base
        )
        self.ui.show_progress("Knowledge base created.")

    def _run_assessment(self):
        self.ui.show_progress("\nStep 4/5: Starting assessment...")
        for question in self.benchmark.questionnaire:
            self.ui.show_progress(f"  - Answering question {question.question_id}: '{question.question[:50]}...'")
            answer = self.test_taker.execute(
                knowledge_base=self.knowledge_base,
                question_text=question.question
            )
            write_markdown_file(
                os.path.join(self.output_dir, f"answer_{question.question_id}.md"),
                answer
            )
            self.assessment_results.append({
                "question_id": question.question_id,
                "question": question.question,
                "answer": answer
            })

    def _evaluate_answers(self):
        self.ui.show_progress("\nStep 5/5: Evaluating answers and generating report...")
        self.evaluation_report = self.examiner.execute(
            questionnaire=self.benchmark.questionnaire,
            assessment_results=self.assessment_results
        )
        if isinstance(self.evaluation_report, EvaluationReport):
            write_json_file(
                os.path.join(self.output_dir, "evaluation_report.json"),
                self.evaluation_report.model_dump()
            )
            self.ui.show_progress("Evaluation complete.")
        else:
            self.ui.display_error("Failed to generate a valid evaluation report.")