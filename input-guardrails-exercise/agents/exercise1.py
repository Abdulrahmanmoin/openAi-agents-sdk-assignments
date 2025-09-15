import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from connection import config


from agents import Agent, input_guardrail, RunContextWrapper, Runner, GuardrailFunctionOutput, trace
from pydantic import BaseModel

class GuardrailAgentOutput(BaseModel):
    is_greeting: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail Agent",
    instructions="Check if in the user input there is any question other than hi, hello and greeting, then raise the exception.",
    output_type=GuardrailAgentOutput
)

@input_guardrail
async def assistant_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str
):
    result = await Runner.run(
        guardrail_agent,
        input,
        run_config=config
    )
    
    return GuardrailFunctionOutput(
        tripwire_triggered= not result.final_output.is_greeting,
        output_info= result.final_output.reasoning
    )
        

agent = Agent(
    name="Assistant Agent",
    instructions="You are a assitant agent, you can only do hello, hi!",
    input_guardrails=[assistant_guardrail]
)

def main():
    with trace("Input Guardrail exercise 1"):
        try:
            res = Runner.run_sync(
                agent,
                input="I want to change my class timings 😭😭",
                run_config=config
            )
            
            print("OUTPUT: ", res.final_output)
            
        except:
            print("OUTPUT: You can only do greeting with this agent.")
            
main()