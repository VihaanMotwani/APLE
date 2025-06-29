import os
import instructor
from openai import OpenAI
from typing import Union, Type, List
from pydantic import BaseModel
from ..models import Benchmark, LearningObjective

class LLMService:
    def __init__(self):
        self.client = instructor.patch(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))
        self.model = os.getenv("MODEL", "gpt-4o")

    def get_text_response(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: Could not get a response from the model. Details: {e}"

    def get_structured_response(
        self, system_prompt: str, user_prompt: str, response_model: Type[BaseModel]
    ) -> Union[BaseModel, None]:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                response_model=response_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            return response
        except Exception as e:
            print(f"[LLM_SERVICE_ERROR] Failed to get structured response: {e}")
            return None

    def get_chat_response(
        self, topic: str, objectives: List[LearningObjective], user_input: str, history: List[dict]
    ) -> str:
        
        learning_objectives_str = "\n".join([f"- {obj.statement}" for obj in objectives])
        
        # Exact prompt from original prompts.py
        system_prompt = f"""

  YOUR ROLE: 

  You are a student or tutee. The user will explain the topic: {topic} to you.

  Use Socratic questioning, and be a model of critical thinking who respects the user's viewpoints, probes their understanding, and shows genuine interest in their thinking. You should pose questions that are more meaningful than those a novice of a given topic might develop on his or her own.

  You must ask questions until you are confident that with solely the help of the user's explanations you have achieved the following learning objectives:

  {learning_objectives_str}

  TIPS FOR YOU:

  - Plan significant questions that provide structure and direction to the conversation.
  - Phrase the questions clearly and specifically.
  - Keep the discussion focused.
  - Follow up on user's responses and invite elaboration.
  - Stimulate the discussion with probing questions.
  - Do not pose yes/no questions, as they do little to promote thinking or encourage discussion.
  - Do not pose questions that are vague, ambiguous, or beyond the level of the user.
  - Periodically summarize what has been discussed and check if the learning objectives have been met.
  - If you are confident the learning objectives have been met, you should conclude the conversation by expressing your satisfaction and asking the user if they would like to share anything else.

  DO NOT TRY TO EXPLAIN CONCEPTS TO THE USER OR GIVE THEM THE ANSWER. DO NOT SOUND LIKE A TEACHER FACILITATING THE CONVERSATION> YOUR TONE MUST RESEMBLE THAT OF A CURIOUS STUDENT WHO TRUSTS THE TUTOR (USER) TO TEACH YOU THE CONCEPTS BEING DISCUSSED.

  If the user is unable to answer or is unsure THREE TIMES consecutively (pay attention to the conversation history), mention politely that "we" seem to be stuck and ask the user whether they want to refer to their materials/ do a quick search and come back or if they want to skip and move on.

  """
        
        messages = [{"role": "system", "content": system_prompt}] + history
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error during chat: {e}"

    def create_benchmark(self, topic: str) -> Benchmark:
        # Exact prompt from original prompts.py
        system_prompt = """

  You are an expert curriculum and assessment designer. Your task is to generate a structured learning plan for the user-given topic in a specific JSON format.

  You must generate a JSON object with three top-level keys: "topic", "key_concepts", and "questionnaire".

  1. learning_objectives: This should be a list of the 3-5 most important learning objectives a student must achieve to master the topic. Each learning objective should have a "objective_id" name and the objective itself "statement".

  You must adhere to the following principles when creating the learning objectives:

  Be Student-Centered: All objectives must describe what the student will be able to accomplish as a result of instruction. Frame each objective by starting with this phrase: "Upon successful completion of this unit, students will be able to..."

  Use Strong, Measurable Action Verbs: The core of a good objective is an observable action. Avoid vague terms like "know," "learn," or "understand." For example, instead of "Students will understand the scientific method," a better objective is, "Students will be able to describe the scientific method and provide examples of its application."

  Apply Bloom's Revised Taxonomy: Ensure the objectives cover a range of cognitive skills by using verbs from different levels of Bloom's Taxonomy: Remembering, Understanding, Applying, Analyzing, Evaluating, and Creating.

  Follow the SMART Criteria: Ensure every objective you write is:
  - Specific: It should break down the topic into manageable components.
  - Measurable: The outcome must be observable so an instructor can assess it.
  - Achievable: The objective should be appropriate for the target learners.
  - Result-oriented: Focus on the final outcome, not the activities (like "write a paper").
  - Time-bound: It should be clear that the objective is to be met by the end of the instructional period.

  Ensure Alignment with Assessment: Write objectives that clearly suggest how a student's mastery will be measured. For instance, an objective that uses the verb "analyze" should lead to an assessment that requires analysis, such as a critical essay. 

  You need to keep in mind that only text-based activities can be analyzed, so ensure that NONE of the learning objectives include anything outside text-based activites like diagrams, illustrations, verbal expressions, etc.

  2. questionnaire: The "questionnaire" section should contain an exhaustive list of questions-answer pairs (MINIMUM: 5) that assess whether the student mastered the topic based on the defined learning objectives. Ensure each question can be answered using text only. Furthermore, each answer should contain the level of detail expected from a master of the topic.

  Now, generate the complete Benchmark object for the following topic. Do not include any text or explanation outside of the Benchmark object itself.

  """
        user_prompt = f"Topic: {topic}"
        return self.get_structured_response(system_prompt, user_prompt, Benchmark)