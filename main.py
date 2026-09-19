from ollama import chat

MODEL = "qwen3:4b"

SYSTEM_PROMPT = """
You are an AI engineering tutor.

Explain technical concepts in simple language.
Use practical examples whenever useful.
If the user asks something complicated, break it into
smaller steps.
"""

# Conversation memory
messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

print("================================")
print("      LOCAL AI ASSISTANT V2")
print("================================")
print(f"Model: {MODEL}")
print("Memory: Enabled")
print("Type 'exit' to quit.\n")


while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    # Add user's message to memory
    messages.append({
        "role": "user",
        "content": user_input
    })

    try:

        stream = chat(
            model=MODEL,
            messages=messages,
            stream=True
        )

        print("\nAI: ", end="")

        assistant_response = ""

        for chunk in stream:

            content = chunk.message.content

            print(content, end="", flush=True)

            assistant_response += content

        print("\n")

        # Add AI response to memory
        messages.append({
            "role": "assistant",
            "content": assistant_response
        })

    except Exception as e:

        print("\nError:", e)