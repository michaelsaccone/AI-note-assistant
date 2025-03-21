
"""
Prompt templates for the pipeline steps:
1. (small) LM extracts the client name from the message
2. Reasoner divide the message in steps for possible mail to send or calendar event to add
3. A Tool caller LLM selects which tool to call based on the reasoned steps
4. A creative multilingual LLM writes a MarkDown note to save on a Notion page
"""

"""
Variables you can use in the templates: 
extraction prompt:  {user_message}
action reasoning: {user_message} {client_name}
tool caller: {user_message} {reasoned_steps} {client_name}
note writer: {user_message} {reasoned_steps} {client_name}
"""

user_message = "{user_message}"
TEXT_EXTRACTION_PROMPT = f"""
I want you to extract the subject from the sentence I write here below. You have to write only the business name, without any additional explanations or comments.
Do not add any word to complete the name, extract only the words used in the text I give you as input.
"""

client_name = "{client_name}"
ACTION_REASONING_PROMPT = f"""

"""

reasoned_steps = "{reasoned_steps}"
TOOL_CALLER_PROMPT = """


"""

NOTE_ORGANISER_PROMPT = """
You are a text clarification expert. Please rewrite the following text to make it clearer and more organized,
since it has been recorded and your output will be used as a written note. Consider that the note will be added to
the client's Notion page, under a h3 section (###) like other notes are formatted, so the page will already contain the
client business name the date, and the h3 section (therefore, you must not write them in the note). 
You should also use Markdown syntax for the text formatting.
Remove any redundant parts while ensuring all important information is retained. Write the note in italian.
"""
