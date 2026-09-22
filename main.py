from ollama import chat

from tools import calculator, get_current_time, AVAILABLE_TOOLS


MODEL = "qwen3:4b"


SYSTEM_PROMPT = """
You are a helpful local AI assistant.

You have access to tools that you can use when necessary.

Available tools:

1. calculator
   Use this for mathematical calculations.

2. get_current_time
   Use this when the user asks for the current date or time.

Use tools when they are appropriate.
Do not use tools unnecessarily.

After receiving a tool result, provide a clear final answer.
"""


# Conversation memory
messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


# Tools exposed to the model
tools = [
    calculator,
    get_current_time
]


print("======================================")
print("        LOCAL AI AGENT - V3.1")
print("======================================")
print(f"Model: {MODEL}")
print("Tools: calculator, get_current_time")
print("Type 'exit' to quit.")
print()


while True:

    user_input = input("You: ")

    # Exit
    if user_input.lower() == "exit":
        print("\nGoodbye!")
        break

    # Add user message to memory
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    try:

        # Ask the model what to do
        response = chat(
            model=MODEL,
            messages=messages,
            tools=tools
        )

        # ------------------------------------------------
        # TOOL CALL
        # ------------------------------------------------

        if response.message.tool_calls:

            # Store the assistant's tool-call message
            messages.append(response.message)

            for tool_call in response.message.tool_calls:

                tool_name = tool_call.function.name
                tool_arguments = tool_call.function.arguments

                print("\n[Agent requested tool]")
                print("Tool:", tool_name)
                print("Arguments:", tool_arguments)

                # Find tool from registry
                tool_function = AVAILABLE_TOOLS.get(tool_name)

                if tool_function is None:

                    result = f"Error: Tool '{tool_name}' not found."

                else:

                    try:

                        result = tool_function(
                            **tool_arguments
                        )

                    except Exception as e:

                        result = f"Tool error: {str(e)}"

                print("Result:", result)

                # Send tool result back to model
                messages.append(
                    {
                        "role": "tool",
                        "tool_name": tool_name,
                        "content": str(result)
                    }
                )

            # Ask model to generate final answer
            final_response = chat(
                model=MODEL,
                messages=messages,
                tools=tools
            )

            print(
                "\nAI:",
                final_response.message.content
            )

            # Store final response
            messages.append(
                {
                    "role": "assistant",
                    "content": final_response.message.content
                }
            )

        # ------------------------------------------------
        # NORMAL RESPONSE
        # ------------------------------------------------

        else:

            print(
                "\nAI:",
                response.message.content
            )

            messages.append(
                {
                    "role": "assistant",
                    "content": response.message.content
                }
            )

    except Exception as e:

        print("\nERROR:", e)