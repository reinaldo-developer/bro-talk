import ollama
import re

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
    
def stream_response_ollama(user_text, history, model_name="llama3:8b"):
    """
    Generate response but with a fluid streaming yielding conversation.
    """
    history.append({"role":"user", "content": user_text})
    stream = ollama.chat(model=model_name, messages=history, stream=True)

    buffer = ""
    full_response = ""

    for chunk in stream:
        token = chunk['message']['content']
        buffer += token
        full_response += token

    if re.search(r'[.!?]\s', buffer):
        sentences = re.split(r'(?<=[.!?])\s+', buffer)

        for i in range(len(sentences) - 1):
            if sentences[i].strip():
                yield sentences[i].strip()
        
        buffer = sentences[-1]
    if buffer.strip():
        yield buffer.strip()

