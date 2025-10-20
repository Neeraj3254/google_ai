import os
import google.generativeai as genai
from dotenv import load_dotenv
import time

load_dotenv()

# Check if API key exists
if not os.getenv("GOOGLE_API_KEY"):
    print("❌ ERROR: No API key found!")
    print("Fix: Check your .env file has GOOGLE_API_KEY=your-key")
    exit()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def chat_with_retry(user_message, conversation_history, max_retries=3):
    """Chat with retry if it fails"""
    
    conversation_history.append({
        "role": "user",
        "parts": [user_message]
    })
    
    model = genai.GenerativeModel('gemini-2.5-pro')
    
    for attempt in range(max_retries):
        try:
            chat_session = model.start_chat(history=conversation_history[:-1])
            
            # Stream response
            print("\n🤖 AI: ", end="", flush=True)
            full_response = ""
            
            response = chat_session.send_message(user_message, stream=True)
            
            for chunk in response:
                if chunk.text:
                    print(chunk.text, end="", flush=True)
                    full_response += chunk.text
            
            print()
            
            conversation_history.append({
                "role": "model",
                "parts": [full_response]
            })
            
            return conversation_history, None
            
        except Exception as e:
            if attempt == max_retries - 1:
                return conversation_history, f"Failed after {max_retries} tries: {str(e)}"
            print(f"\n⚠️ Attempt {attempt + 1} failed, retrying...")
            time.sleep(1)
    
    return conversation_history, "Unknown error"

def save_conversation(conversation_history, filename="conversation.txt"):
    """Save your chat to a file"""
    try:
        with open(filename, 'w') as f:
            f.write("My AI Conversation\n")
            f.write("="*60 + "\n\n")
            
            for msg in conversation_history:
                role = "You" if msg["role"] == "user" else "AI"
                content = msg["parts"][0]
                f.write(f"{role}: {content}\n\n")
        
        print(f"💾 Saved to {filename}")
        return True
    except Exception as e:
        print(f"❌ Couldn't save: {str(e)}")
        return False

def main():
    """Production-ready chatbot!"""
    print("🤖 AI Chatbot (Production Ready)")
    print("="*60)
    print("Features: Memory, Streaming, Error Handling, Save")
    print("Commands: 'quit', 'save'")
    print("="*60)
    
    conversation_history = []
    message_count = 0
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                print("⚠️ Please type something")
                continue
            
            # Commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                if conversation_history:
                    save_choice = input("\n💾 Save conversation? (y/n): ")
                    if save_choice.lower() == 'y':
                        save_conversation(conversation_history)
                print(f"\n📊 Total messages: {message_count}")
                print("👋 Goodbye!\n")
                break
            
            if user_input.lower() == 'save':
                save_conversation(conversation_history)
                continue
            
            # Get AI response
            conversation_history, error = chat_with_retry(
                user_input, 
                conversation_history
            )
            
            if error:
                print(f"\n❌ {error}")
                print("Try again or type 'quit'")
            else:
                message_count += 1
                
        except KeyboardInterrupt:
            print("\n\n⚠️ Interrupted! Type 'quit' to exit properly")
            continue
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()