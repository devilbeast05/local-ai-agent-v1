from ollama import chat

from tools import (
    AVAILABLE_TOOLS,
    calculator,
    get_current_time
)


# ==================================================
# CONFIGURATION
# ==================================================

MODEL = "qwen3:4b"

MAX_TOOL_ITERATIONS = 5


# ==================================================
# SYSTEM PROMPT
# ==================================================

SYSTEM_PROMPT = """
You are a helpful general-purpose local AI assistant.

You are powered by a local Qwen language model.

You can:
- Answer general questions.
- Explain concepts.
- Help with programming.
- Help with mathematics.
- Reason about problems.
- Have normal conversations.
- Explain technical topics.
- Use tools when tools are useful.

You have access to these tools:

1. calculator
   Use this for mathematical calculations.

2. get_current_time
   Use this when the user asks for the current date or time.

IMPORTANT:

The tools are additional capabilities.
They are NOT your only capabilities.

If the user asks a normal question that does not require a tool,
answer the question directly using your language-model knowledge.

Do NOT say that you are unable to answer a question merely because
there is no tool for it.

Use a tool only when the user's request actually requires that tool.

For example:

User: "What is an AI agent?"
Answer normally.

User: "What is Python?"
Answer normally.

User: "Explain machine learning."
Answer normally.

User: "What is 25 multiplied by 8?"
Use the calculator tool.

User: "What time is it?"
Use the get_current_time tool.

After receiving a tool result:
- Analyze the result.
- Use it to answer the user.
- Do not expose unnecessary internal tool details.

Always provide a useful final answer.
"""

# ==================================================
# TOOLS AVAILABLE TO OLLAMA
# ==================================================

TOOLS = [
    calculator,
    get_current_time
]


# ==================================================
# AGENT CLASS
# ==================================================

class LocalAIAgent:

    def __init__(self):

        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        self.tool_iterations = 0


    # ==================================================
    # ADD USER MESSAGE
    # ==================================================

    def add_user_message(self, user_input):

        self.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )


    # ==================================================
    # EXECUTE TOOL
    # ==================================================

    def execute_tool(self, tool_name, arguments):

        print("\n[Tool Execution]")
        print("Tool:", tool_name)
        print("Arguments:", arguments)

        # ----------------------------------------------
        # Find tool
        # ----------------------------------------------

        tool_function = AVAILABLE_TOOLS.get(tool_name)

        if tool_function is None:

            result = (
                f"Error: Tool '{tool_name}' "
                f"does not exist."
            )

            print("Result:", result)

            return result


        # ----------------------------------------------
        # Execute tool safely
        # ----------------------------------------------

        try:

            result = tool_function(
                **arguments
            )

            print("Result:", result)

            return result

        except TypeError as error:

            result = (
                f"Invalid arguments for tool "
                f"'{tool_name}': {error}"
            )

            print("Result:", result)

            return result

        except Exception as error:

            result = (
                f"Tool execution failed: {error}"
            )

            print("Result:", result)

            return result


    # ==================================================
    # RUN AGENT
    # ==================================================

    def run(self):

        self.tool_iterations = 0


        # ==================================================
        # AGENT LOOP
        # ==================================================

        while self.tool_iterations < MAX_TOOL_ITERATIONS:

            self.tool_iterations += 1

            print(
                f"\n[Agent iteration "
                f"{self.tool_iterations}/"
                f"{MAX_TOOL_ITERATIONS}]"
            )


            # ------------------------------------------
            # Ask LLM
            # ------------------------------------------

            response = chat(
                model=MODEL,
                messages=self.messages,
                tools=TOOLS
            )


            # ------------------------------------------
            # Check tool calls
            # ------------------------------------------

            tool_calls = response.message.tool_calls


            # ==================================================
            # FINAL ANSWER
            # ==================================================

            if not tool_calls:

                final_answer = response.message.content

                self.messages.append(
                    {
                        "role": "assistant",
                        "content": final_answer
                    }
                )

                return final_answer


            # ==================================================
            # TOOL CALL
            # ==================================================

            print(
                f"[Agent requested "
                f"{len(tool_calls)} tool(s)]"
            )


            # ------------------------------------------
            # Store assistant tool request
            # ------------------------------------------

            self.messages.append(
                response.message
            )


            # ------------------------------------------
            # Execute tools
            # ------------------------------------------

            for tool_call in tool_calls:

                tool_name = tool_call.function.name

                arguments = tool_call.function.arguments

                result = self.execute_tool(
                    tool_name,
                    arguments
                )


                # --------------------------------------
                # Send result back to LLM
                # --------------------------------------

                self.messages.append(
                    {
                        "role": "tool",
                        "tool_name": tool_name,
                        "content": str(result)
                    }
                )


            print(
                "\n[Tool results sent back to model]"
            )


        # ==================================================
        # MAX ITERATION REACHED
        # ==================================================

        return (
            "I stopped because the maximum number "
            "of tool iterations was reached."
        )