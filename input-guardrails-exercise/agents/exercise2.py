# from connection import config
from agents import Agent, Runner, input_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, trace
from pydantic import BaseModel

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from connection import config

class father_guardrail_output(BaseModel):
    response: str
    isWeatherExceed: bool

father_input_guardrail_agent = Agent(
    "Father Guardrail",
    instructions="""
    Your task is to check if the temperature is below 26°C based on the input. 
    The input may contain a temperature like '27C' or 'it is 27C'. 
    Extract the temperature (a number followed by 'C') and compare it to 26°C.
    If the temperature is below 26°C, set isWeatherExceed to True and provide a response indicating running is not allowed.
    If the temperature is 26°C or higher, set isWeatherExceed to False and allow running.
    Example outputs:
    - For input 'it is 25C': {"response": "Too cold to run.", "isWeatherExceed": True}
    - For input 'it is 27C': {"response": "Temperature is fine to run.", "isWeatherExceed": False}
    """,   
    output_type=father_guardrail_output   
)

@input_guardrail
async def father_guadrail(ctx, agent, input):
    result = await Runner.run(
        father_input_guardrail_agent,
        input,
        run_config=config
    )
    
    return GuardrailFunctionOutput(
        output_info= result.final_output.response,
        tripwire_triggered=result.final_output.isWeatherExceed
    )
    

# Main Agent
father_agent = Agent(
    "Father Agent",
    instructions="""
    You are a strict father agent. Kids ask you for permission to run. 
    Don't allow running if the temperature is below 26°C, as determined by the guardrail.
    If the guardrail allows the input, respond with permission to run.
    """,
    input_guardrails=[father_guadrail]
)


def main():
    try:
        with trace("Strict Father Agent"):
            result = Runner.run_sync(
                father_agent,
                input="I want to run. it is 25C",
                run_config=config
                )
            print("OUTPUT: ", result.final_output)
        
    except InputGuardrailTripwireTriggered as e:
       print("OUTPUT: It is too cold to run. You are not allowed to run.")
        

main()