from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = '''
Answer the question below.
Here is the conversation history: {context}
Question: {question}
Answer:
'''

model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

print("Welcome to the AI ChatBot! Type 'exit' to quit.")

context = ""

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    
    print("Bot:", end=" ", flush=True)

    for chunk in chain.stream({"context": context, "question": user_input}):
        print(chunk, end="", flush=True)
    
    print()
    context += f"\nUser: {user_input}\nAI: {''.join(chunk for chunk in chain.stream({'context': context, 'question': user_input}))}"
