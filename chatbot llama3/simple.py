from langchain_ollama import OllamaLLM

model = OllamaLLM(model="llama3")

print("Welcome! Type 'exit' to quit.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    
    print("Bot:", end=" ", flush=True)

    for chunk in model.stream(user_input):
        print(chunk, end="", flush=True)
    print()
