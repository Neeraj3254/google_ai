import os
import google.generativeai as genai
from dotenv import load_dotenv
import time

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def chat_stream(user_message, conversation_history):
    """Chat but show words appearing one by one!"""
    
    conversation_history.append({
        "role": "user",
        "parts": [user_message]
    })
    
    model = genai.GenerativeModel('gemini-2.5-pro')
    chat_session = model.start_chat(history=conversation_history[:-1])
    
    # Stream = words appear gradually!
    print("\n🤖 AI: ", end="", flush=True)
    full_response = ""
    
    response = chat_session.send_message(user_message, stream=True)
    
    for chunk in response:
        if chunk.text:
            print(chunk.text, end="", flush=True)
            full_response += chunk.text
            time.sleep(0.01)  # Tiny pause so you can see it!
    
    print()  # New line when done
    
    conversation_history.append({
        "role": "model",
        "parts": [full_response]
    })
    
    return conversation_history

def main():
    """Chatbot with cool streaming!"""
    print("🤖 AI Chatbot with Streaming")
    print("="*60)
    print("Watch responses appear word-by-word!")
    print("Type 'quit' to exit")
    print("="*60)
    
    conversation_history = []
    
    while True:
        user_input = input("\n👤 You: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!\n")
            break
        
        try:
            conversation_history = chat_stream(user_input, conversation_history)
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()