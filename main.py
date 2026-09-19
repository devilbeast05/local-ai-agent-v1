from ollama import chat

print("================================")
print("       LOCAL AI ASSISTANT")
print("================================")
print("Model: qwen3:4b")
print("Type 'exit' to quit.\n")

while True:

    user_input= input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    response = chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    print("\nAI:", response.message.content)
    print()