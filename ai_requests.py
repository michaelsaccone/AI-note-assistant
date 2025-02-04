from langchain.chains import LLMChain
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate

client_extraction_model_name = 'llama3.2:1b'
action_reasoner_model_name = 'deepseek-r1:14b'



# Initialize the Ollama LLM
llm = Ollama(model=model_name, temperature=temperature)


def call_ollama_llm(prompt_text, model_name="llama2", temperature=0.7):
    """
    Calls an LLM hosted with Ollama using LangChain.

    :param prompt_text: The input text prompt for the LLM.
    :param model_name: The name of the model to use (default is 'llama2').
    :param temperature: The temperature for sampling (default is 0.7).
    :return: The generated text from the LLM.
    """


    # Define a simple prompt template
    prompt_template = PromptTemplate(
        input_variables=["input_text"],
        template="{input_text}"
    )

    # Create an LLMChain with the prompt template and the LLM
    llm_chain = LLMChain(llm=llm, prompt=prompt_template)

    # Call the LLM with the provided prompt text
    response = llm_chain.run(input_text=prompt_text)

    return response