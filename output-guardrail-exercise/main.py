from connection import config

from agents import Agent, output_guardrail, Runner, GuardrailFunctionOutput, trace
from pydantic import BaseModel


class FinancialAgentOutputGuardOutput(BaseModel):
    isAppropriateAdvice: bool
    isDisclaimer: bool
    reasoning: str

finance_output_guardrail_agent = Agent(
    name="Financial output guardrail agent",
    instructions=
    """
    You are the output guardrail agent checks the following thing in response:
    The response has the appropriate disclaimers
    The response should be general, educational not a specific advice to buy
    The response should include an advice to consult with the licensed financial advisor.
    """,
    output_type=FinancialAgentOutputGuardOutput
)

@output_guardrail
async def finance_output_guardrail_func(ctx, agent, output):
    response = await Runner.run(
        finance_output_guardrail_agent,
        f"Validating this financial advice response: {output}",
        run_config=config,
    )

    return GuardrailFunctionOutput(
        output_info=response.final_output.reasoning,
        tripwire_triggered= not (
            response.final_output.isDisclaimer and
            response.final_output.isAppropriateAdvice
        )
    )

finance_agent = Agent(
    name="Finance Agent",
    instructions=""" 
    You are helpful Finance advisory agent. 
    Always use the disclaimer that this is not professional. 
    Encourage user to contact the certified financial advisor for professional desicions.
    Never gurantee specific returns or outcomes.
    """
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="Your task is to delegate the finance related questions or queries to the Finance Agent",
    handoffs=[finance_agent]
)

def main():
    with trace("OUTPUT GUARDRAIL EXERCISE - FINANCIAL AGENT"):
        response = Runner.run_sync(
            triage_agent,
            "Tell me about BTC, should I buy that or not?",
            run_config=config,
        )

        print("OUTPUT: ", response.final_output)

main()