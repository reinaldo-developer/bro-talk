import ollama

def get_response_ollama(user_text, history, model_name="llama3:8b"):
    """Generate response based on model"""
    history.append({"role":"user","content":user_text})
    try:
        response = ollama.chat(model=model_name, messages=history)
        ai_message = response["message"]["content"]
        history.append({"role":"assistant", "content":ai_message})
        return ai_message, history
    
    except Exception as e:
        print(f"❌ Erro ao comunicar com o Ollama: {e}")
        history.append({"role": "assistant", "content": "I'm having trouble thinking right now."})
        return "I'm having trouble thinking right now.", history
    






