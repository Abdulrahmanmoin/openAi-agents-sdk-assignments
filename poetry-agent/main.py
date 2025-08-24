from agents import Agent, Runner, function_tool
from connection import config

# --- Poet Agent ---
poet_agent = Agent(
    name="Poet Agent",
    instructions=(
        "You are a poet. Write a 2 stanza poem about feelings, story, or performance."
    )
)

@function_tool
async def generate_poem() -> str:
    """
    Generate a fresh poem using poet agent.
    """
    result = await Runner.run(poet_agent, input="Write a 2 stanza poem.", run_config=config)
    print("Poem: ", result.final_output)
    return result.final_output

# --- Analyst Agents ---
lyric_analyst = Agent(
    name="Lyric Analyst",
    instructions="Analyze if the poem is lyric (personal feelings and emotions). Respond Yes or No with reason also tell type of poem like (Lyric, Narrative, or Dramatic)."
)

narrative_analyst = Agent(
    name="Narrative Analyst",
    instructions="Analyze if the poem is narrative (story with characters/events). Respond Yes or No with reason also tell type of poem like (Lyric, Narrative, or Dramatic)."
)

dramatic_analyst = Agent(
    name="Dramatic Analyst",
    instructions="Analyze if the poem is dramatic (meant to be spoken by a character/like in a play). Respond Yes or No with reason also tell type of poem like (Lyric, Narrative, or Dramatic)."
)

# --- Orchestrator Agent ---
orchestrator = Agent(
    name="Poetry Orchestrator",
    instructions=(
        "First, call the Poet Agent to generate a poem. "
        "Then decide which type of poem it is: lyric, narrative, or dramatic. "
        "Finally, hand the poem to the correct analyst agent for confirmation."
    ),
    tools=[generate_poem],
    handoffs=[lyric_analyst, narrative_analyst, dramatic_analyst]
)

# --- Run the workflow ---
result = Runner.run_sync(
    orchestrator,
    input="Start by calling the Poet Agent. After that, analyze the poem.",
    run_config=config
)

print("\nFinal Output:\n", result.final_output)