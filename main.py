from agent import LocalAIAgent, MODEL


# ==================================================
# DISPLAY
# ==================================================

print("==========================================")
print("          LOCAL AI AGENT - V3.3")
print("==========================================")
print(f"Model: {MODEL}")
print()
print("Features:")
print("  - Local LLM")
print("  - Conversation Memory")
print("  - Tool Calling")
print("  - Multiple Tools")
print("  - Agent Loop")
print("  - Tool Safety")
print("  - Iteration Limit")
print()
print("Type 'exit' to quit.")
print()


# ==================================================
# CREATE AGENT
# ==================================================

agent = LocalAIAgent()


# ==================================================
# MAIN LOOP
# ==================================================

while True:

    user_input = input("You: ")


    # ----------------------------------------------
    # EXIT
    # ----------------------------------------------

    if user_input.lower() == "exit":

        print("\nGoodbye!")

        break


    # ----------------------------------------------
    # ADD USER MESSAGE
    # ----------------------------------------------

    agent.add_user_message(
        user_input
    )


    # ----------------------------------------------
    # RUN AGENT
    # ----------------------------------------------

    try:

        answer = agent.run()

        print("\nAI:", answer)
        print()

    except Exception as error:

        print(
            "\nAgent Error:",
            error
        )

        print()