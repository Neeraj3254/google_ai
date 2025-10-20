import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load your secret API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def chat(user_message, conversation_history):
    """Talk to the AI and remember what was said before"""
    
    # Add your message to the memory
    conversation_history.append({
        "role": "user",
        "parts": [user_message]
    })
    
    # Create the AI
    model = genai.GenerativeModel('gemini-2.5-pro')
    
    # Start a conversation with memory
    chat_session = model.start_chat(history=conversation_history[:-1])
    
    # Get AI's response
    response = chat_session.send_message(user_message)
    ai_reply = response.text
    
    # Remember what AI said
    conversation_history.append({
        "role": "model",
        "parts": [ai_reply]
    })
    
    return ai_reply, conversation_history

def main():
    """The main chat loop"""
    print("🤖 AI Chatbot with Memory")
    print("="*50)
    print("Type your messages below.")
    print("Type 'quit' to exit")
    print("="*50)
    print()
    
    # Empty memory to start
    conversation_history = []
    message_count = 0
    
    while True:
        # Get what you type
        user_input = input("\n👤 You: ").strip()
        
        # Did you type nothing?
        if not user_input:
            print("⚠️ Please type something!")
            continue
        
        # Want to exit?
        if user_input.lower() in ['quit', 'exit', 'q']:
            print(f"\n👋 Goodbye! You had {message_count} exchanges.")
            break
        
        # Get AI response
        try:
            ai_response, conversation_history = chat(user_input, conversation_history)
            message_count += 1
            
            # Show the response
            print(f"\n🤖 AI: {ai_response}")
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Try again or type 'quit' to exit")

if __name__ == "__main__":
    main()