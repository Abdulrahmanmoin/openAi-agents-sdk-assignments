from connection import config
from agents import Agent, function_tool, RunContextWrapper, trace, Runner
from pydantic import BaseModel

class UserInfo(BaseModel):
    user_id: str | int
    name: str


user_1 = UserInfo(name="Abdul Rahman Moin", user_id=2)

@function_tool
def get_user_info(wrapper: RunContextWrapper[UserInfo]):
    return f"The user info is {wrapper.context}"

agent = Agent(
    name="Context Agent",
    instructions="You are assistant agent, always call the tool to get the user context.",
    tools=[get_user_info]
)

def main():
    with trace("Context Agent"):
        res = Runner.run_sync(
            agent,
            "Tell me my name and what is my age.",
            context=user_1,
            run_config=config
        )

        print("output: ", res.final_output)


main()