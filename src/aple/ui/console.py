from ..models import EvaluationReport

class ConsoleUI:
    def display_header(self):
        print('-'*75 + '\n\t\t\t\tA.T.L.A.S\n' + '-'*75)
        print("\nHey! I'm APLE, your protégé. What are we learning today?\n")

    def get_topic(self) -> str:
        topic = input("Enter topic: ")
        print("\nInteresting! Let's get right into it!")
        return topic

    def show_progress(self, message: str):
        print(message)

    def display_error(self, message: str):
        print(f"\n[ERROR] {message}")

    def display_chat_prompt(self):
        print('-'*75 + '\n\t\t\t\tChat with APLE\n' + '-'*75)
        print("I'm ready to learn. Teach me about the topic. Type 'exit' to end the session.")

    def get_chat_input(self) -> str:
        return input("\nYou: ")

    def display_chatbot_response(self, response: str):
        print(f"\nAPLE: {response}\n")

    def display_goodbye(self):
        print("\nGoodbye! Ending the learning session.")
    
    def display_summary(self, assessment_results: list):
        print("\nAssessment Complete. All artifacts have been saved to the 'output' directory.")
        print("\nSummary of Answers:")
        for result in assessment_results:
            print(f"\nQ: {result['question']}\nA: {result['answer']}")

    def display_report(self, report: EvaluationReport):
        print("\n--- Evaluation Report ---")
        if isinstance(report, EvaluationReport):
            remarks = report.overall_remarks
            print(f"\nOverall Score: {report.overall_score_percentage}%")
            print(f"\n--- Overall Remarks ---")
            print(f"  Strengths: {remarks.strengths}")
            print(f"  Areas for Improvement: {remarks.areas_for_improvement}")
            print(f"  Suggested Next Steps: {remarks.suggested_next_steps}")
            
            print("\n--- Detailed Evaluation ---")
            for eval_item in report.question_evaluations:
                print(f"\n  Question ID: {eval_item.question_id}")
                print(f"  Evaluation: {eval_item.evaluation} ({eval_item.score} points)")
                print(f"  Justification: {eval_item.justification}")
            print("\nA detailed report has been saved to 'output/evaluation_report.json'")
        else:
            print("\nError: The model failed to return a valid report object.")
            if report:
                print("Raw error output:", report)
    
    def display_footer(self):
        print("\n------------------------\nExecution finished.\n------------------------\n")