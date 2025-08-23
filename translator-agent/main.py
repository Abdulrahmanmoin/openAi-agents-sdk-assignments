from connection import config
from agents import Agent, Runner

# Create a language-specific agent for translation
translator_agent = Agent(
    name="Translator Agent",
    instructions=(
        "You are a translation assistant. Translate the user's input"
        "if user input is in English then translate into Roman Urdu or if in Roman Urdu then translate into English."
    ),
)

user_input = "How are you today?"

result = Runner.run_sync(translator_agent, 
                         input=user_input,
                         run_config=config
                         )

print("Translation:", result.final_output)