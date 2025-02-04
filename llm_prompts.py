
"""
Prompt templates for the pipeline steps:
1. (small) LM extracts the client name from the message
2. Reasoner divide the message in steps for possible mail to send or calendar event to add
3. A Tool caller LLM selects which tool to call based on the reasoned steps
4. A creative multilingual LLM writes a MarkDown note to save on a Notion page
"""

"""
Variables you can use in the templates: 
extraction prompt:  ${user_message}
action reasoning: ${user_message} ${client_name}
tool caller: ${user_message} ${reasoned_steps} ${client_name}
note writer: ${user_message} ${reasoned_steps} ${client_name}
"""


TEXT_EXTRACTION_PROMPT = """

"""

ACTION_REASONING_PROMPT = """

"""

TOOL_CALLER_PROMPT = """


"""

NOTE_WRITER_PROMPT = """


"""