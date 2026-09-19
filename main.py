from ollama import chat

response = chat(
model="qwen3:4b",
messages=[
    {
        "role": "user",
        "content": "Explain what artificial intelligence is."
    }
]
)
print (response.message.content)