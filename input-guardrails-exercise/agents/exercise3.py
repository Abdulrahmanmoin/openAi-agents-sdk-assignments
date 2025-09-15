import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from connection import config

from agents import Agent, input_guardrail, RunContextWrapper, Runner, GuardrailFunctionOutput, trace
from pydantic import BaseModel

class GateKeeperGuardrailOutput(BaseModel):
    is_student_this_school: bool
    reasoning: str

gate_keeper_guardrail_agent = Agent(
    name="Gate Keeper Guardrail Agent",
    instructions="You don't allow student of other school to enter this 'Massachusetts Institute of Technology (MIT)' school.",
    output_type=GateKeeperGuardrailOutput
)

@input_guardrail
async def gate_keeper_guardrail(ctx: RunContextWrapper[None], agent: Agent, input: str):
        result = await Runner.run(
            gate_keeper_guardrail_agent,
            input,
            run_config=config
        )
        
        return GuardrailFunctionOutput(
            output_info= result.final_output.reasoning,
            tripwire_triggered= not result.final_output.is_student_this_school
        )

agent = Agent(
    name="Gate Keeper Agent",   
    instructions="You a gate keeper agent, you open gate for school students.",
    input_guardrails=[gate_keeper_guardrail]
)

def main():
    with trace("Input guardrail - Gate keeper guardrail"):
        try:
            res = Runner.run_sync(
                agent,
                input="I want to go inside and my school name is Oxford.",
                run_config=config,
            )
            
            print("OUTPUT: ", res.final_output)
        
        except:
            print("OUTPUT: You are not allowed to go inside!")
            
main()