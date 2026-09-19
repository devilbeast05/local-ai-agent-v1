from ollama import chat

MODEL = "qwen3:4b"

SYSTEM_PROMPT = """
You are an AI engineering tutor.

Explain technical concepts in simple language.
Use practical examples whenever useful.
If the user asks something complicated, break it into
smaller steps.
"""

print("================================")
print("       LOCAL AI ASSISTANT")
print("================================")
print(f"Model: {MODEL}")
print("Type 'exit' to quit.\n")


while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    try:

        stream = chat(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            stream=True
        )

        print("\nAI: ", end="")

        for chunk in stream:
            print(chunk.message.content, end="", flush=True)

        print("\n")

    except Exception as e:
        print("\nError:", e)