from ollama import chat

from tools import (
    calculator,
    get_current_time,
    AVAILABLE_TOOLS
)


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

MODEL = "qwen3:4b"

SYSTEM_PROMPT = """
You are a helpful local AI assistant.

You have access to tools.

Available tools:

1. calculator
   Use this for mathematical calculations.

2. get_current_time
   Use this when the user asks for the current date or time.

Rules:

- Use tools whenever they are appropriate.
- Do not use tools unnecessarily.
- After receiving tool results, analyze them.
- You may use multiple tools if necessary.
- Continue using tools until you have enough information
  to answer the user's request.
- Once you have enough information, provide a clear final answer.
"""


# --------------------------------------------------
# CONVERSATION MEMORY
# --------------------------------------------------

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


# --------------------------------------------------
# TOOLS AVAILABLE TO THE MODEL
# --------------------------------------------------

tools = [
    calculator,
    get_current_time
]


# --------------------------------------------------
# DISPLAY
# --------------------------------------------------

print("==========================================")
print("          LOCAL AI AGENT - V3.2")
print("==========================================")
print(f"Model: {MODEL}")
print("Tools:")
print("  - calculator")
print("  - get_current_time")
print()
print("Type 'exit' to quit.")
print()


# --------------------------------------------------
# MAIN APPLICATION LOOP
# --------------------------------------------------

while True:

    user_input = input("You: ")

    # ----------------------------------------------
    # EXIT
    # ----------------------------------------------

    if user_input.lower() == "exit":

        print("\nGoodbye!")

        break


    # ----------------------------------------------
    # ADD USER MESSAGE TO MEMORY
    # ----------------------------------------------

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    try:

        # ------------------------------------------
        # AGENT LOOP
        # ------------------------------------------

        while True:

            print("\n[Agent thinking...]")

            response = chat(
                model=MODEL,
                messages=messages,
                tools=tools
            )


            # --------------------------------------
            # CHECK FOR TOOL CALLS
            # --------------------------------------

            tool_calls = response.message.tool_calls


            # --------------------------------------
            # NO TOOL CALL
            # --------------------------------------

            if not tool_calls:

                final_answer = response.message.content

                print("\nAI:", final_answer)

                # Store final assistant response
                messages.append(
                    {
                        "role": "assistant",
                        "content": final_answer
                    }
                )

                # Exit agent loop
                break


            # --------------------------------------
            # TOOL CALLS FOUND
            # --------------------------------------

            print("\n[Tool calls detected]")


            # Store assistant's tool-call message
            messages.append(response.message)


            # --------------------------------------
            # EXECUTE EACH TOOL
            # --------------------------------------

            for tool_call in tool_calls:

                tool_name = tool_call.function.name

                arguments = tool_call.function.arguments


                print("\n------------------------------")
                print("Tool:", tool_name)
                print("Arguments:", arguments)


                # ----------------------------------
                # FIND TOOL
                # ----------------------------------

                tool_function = AVAILABLE_TOOLS.get(
                    tool_name
                )


                if tool_function is None:

                    result = (
                        f"Error: Tool '{tool_name}' "
                        f"does not exist."
                    )

                else:

                    try:

                        # --------------------------
                        # EXECUTE TOOL
                        # --------------------------

                        result = tool_function(
                            **arguments
                        )

                    except Exception as tool_error:

                        result = (
                            f"Tool execution error: "
                            f"{tool_error}"
                        )


                print("Result:", result)
                print("------------------------------")


                # ----------------------------------
                # SEND TOOL RESULT BACK TO MODEL
                # ----------------------------------

                messages.append(
                    {
                        "role": "tool",
                        "tool_name": tool_name,
                        "content": str(result)
                    }
                )


            # --------------------------------------
            # LOOP CONTINUES
            # --------------------------------------

            print(
                "\n[Sending tool results back to model...]"
            )


    except Exception as error:

        print(
            "\nERROR:",
            error
        )