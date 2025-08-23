import requests
from agents import Agent, Runner, function_tool
from connection import config

API_URL = "https://template-03-api.vercel.app/api/products"

@function_tool
def get_products() -> list:
    """
    Fetch products from the shopping API.
    If category is given, filter products by category.
    """
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        products = data.get("data", [])
        
        return products[:5]  # return only top 5 for readability
    except Exception as e:
        print("Errors in get-products function tool:", e)
        return []

translator_agent = Agent(
    name="Shopping Agent",
    instructions=(
        "You are a helpful shopping assistant. Use tools to fetch product info."
    ),
    tools=[get_products]
)

user_input = "Show me product for Men's shoes."

result = Runner.run_sync(translator_agent, 
                         input=user_input,
                         run_config=config
                         )

print("Output:", result.final_output)