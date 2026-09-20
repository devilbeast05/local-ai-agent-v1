from ollama import chat
from tools import calculator

MODEL = "qwen3:4b"

SYSTEM_PROMPT = """
You are a helpful AI assistant.

You have access to a calculator tool.
Use the calculator whenever the user asks you to perform arithmetic.

Do not manually calculate when the calculator tool can be used.
"""

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

tools = [
    calculator
]

print("================================")
print("       LOCAL AI AGENT V3")
print("================================")
print(f"Model: {MODEL}")
print("Tools: calculator")
print("Type 'exit' to quit.\n")


while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    try:

        response = chat(
            model=MODEL,
            messages=messages,
            tools=tools
        )

        # Check whether the model requested a tool
        if response.message.tool_calls:

            for tool_call in response.message.tool_calls:

                print("\n[Tool requested]")
                print("Tool:", tool_call.function.name)
                print("Arguments:", tool_call.function.arguments)

                if tool_call.function.name == "calculator":

                    result = calculator(
                        **tool_call.function.arguments
                    )

                    print("Tool result:", result)

                    messages.append(response.message)

                    messages.append({
                        "role": "tool",
                        "tool_name": "calculator",
                        "content": str(result)
                    })

            # Ask the model to produce the final answer
            final_response = chat(
                model=MODEL,
                messages=messages
            )

            print("\nAI:", final_response.message.content)

            messages.append({
                "role": "assistant",
                "content": final_response.message.content
            })

        else:

            print("\nAI:", response.message.content)

            messages.append({
                "role": "assistant",
                "content": response.message.content
            })

    except Exception as e:

        print("\nError:", e)