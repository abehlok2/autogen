import os
from typing import Tuple
import autogen
from autogen import AssistantAgent, ConversableAgent, GroupChat, GroupChatManager, UserProxyAgent, Completion, ChatCompletion, Agent
from autogen import config_list_gpt4_gpt35, config_list_from_json

# Configurations for agents/llms

gpt35_config = \
  {
    "model": "gpt-3.5-turbo-16k",
    "api_key": "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",
    "temperature": 0.25,
    "frequency_penalty": 0.5
}

gpt4_config = \
  {
    "model": "gpt-4-0613",
    "api_key": "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",
    "temperature": 0.25,
    "frequency_penalty": 0.5,
    "request_timeout": 180,
}

user_proxy_admin_agent = autogen.UserProxyAgent(
    name="Assistant Task Administrator",
    llm_config=gpt4_config,
    max_consecutive_auto_reply=5,
    human_input_mode="NEVER",
)

lesson_planning_agent = autogen.ConversableAgent(
    name="Lesson Planning Agent",
    llm_config=gpt4_config,
    max_consecutive_auto_reply=5,
    human_input_mode="ALWAYS",
    system_message = 
  """
  You will now function as a component of a whole that makes up a larger system called the "Teacher Assistant Program".
    The "Teacher Assistant Program" is a system that is designed to help teachers with their daily tasks by utilizing the power of
    machine learning and commercially available AI. Your function within this system is to generate lesson plans for teachers.
    You will be given a prompt and you will generate a lesson plan based on that prompt.
   
    Be *very* considerate of the age appropriateness and overall content of the lesson plan you generate. Your lesson plans
    are all to be generated for general-education level children in 4th grade, in New York State at a good public school.
    If the user provides formatting along with their lesson plan generation query, attempt to preserve or utilize it in
    your response.

    Attempt to preserve formatting unless specifically instructed otherwise. Respond to user prompts with *ONLY* the modified lesson plan.
  
  """
)


def _get_lp_input() -> Tuple[str, str]:
    """Prompt the user for a lesson plan input.
     Args:
      prompt: The prompt to send as the initial message to the agent.
    """
    lp_topic_input = input("What is the topic for the lesson plan you would like to build today?\n>")
    lp_detail_input = input("Please provide any additional context, detail, information, \
    or notes that you would like for me to take into consideration when generating the lesson plan.\n>")

    if lp_topic_input == "" or lp_topic_input == None:
        raise ValueError("Please provide a topic for the lesson plan.")
    elif len(lp_detail_input) > 5000:
        raise ValueError("Please provide a topic for the lesson plan that is less than 5000 characters.")
    output = (lp_topic_input, lp_detail_input)
    return output



def _complete_prompt(output: Tuple[str, str]) -> str:
  """Use the information provided by the user to generate an initial message for the agent
  Args:
  output: A tuple of the topic and detail input provided by the user.
  """
  topic, detail = output
  initial_message = f"""Please create a lesson plan based on the following relevant information 

  The topic of this lesson will be:
  {topic}.

  Use the following additional information and context to improve the quality \
  of your lesson plan: 
  {detail}."""
  return initial_message




def start_lesson_planning(lesson_planning_agent: ConversableAgent = lesson_planning_agent):
    output = _get_lp_input()
    initial_message = _complete_prompt(output)
    lp_chat = user_proxy_admin_agent.initiate_chat(lesson_planning_agent, True, message=initial_message)
    return lp_chat,

output = start_lesson_planning(lesson_planning_agent)
print(output)

if name == __main__():
    start_lesson_planning(lesson_planning_agent)
