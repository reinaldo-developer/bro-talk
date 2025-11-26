from audio_recorder import AudioRecorder
import ai_chat_ollama
import speech_to_text
import text_to_speech
import os

def main():
    system_prompt = """
    You are BroTalk, a friendly and patient AI English conversation partner. 
    Your goal is to help me practice my English speaking skills.
    Keep your responses short and natural, like a real conversation.
    Ask questions to keep the conversation flowing.
    If I make a simple grammatical mistake, gently correct it.
    Start the conversation by introducing yourself and asking me about my day.
    """

    conversation_history = [{"role":"system", "content":system_prompt}]

    introduction_response, conversation_history = ai_chat_ollama.get_response_ollama(
        "Introduce yourself and start the conversation.",
        conversation_history
    )
    text_to_speech.speak(introduction_response)

    while True:
        #record audio from user
        recorder = AudioRecorder()
        user_audio_file = recorder.record_audio()
        #transcribe user audio to intermediary text
        user_text = speech_to_text.transcribe(user_audio_file)
        #remove intermediary audio file
        os.remove(user_audio_file)
        if not user_text.strip():
            text_to_speech.speak("Sorry, I didn't catch that. Could you say it again?")
            continue
        
        print(f"You said: {user_text}")

        if user_text.lower() == "goodbye":
            text_to_speech.speak("Great to talk to you. See ya!")
            break
        full_ai_response = ""
        #ai_text, conversation_history = ai_chat_ollama.get_response_ollama(user_text=user_text,
        #                                                                   history=conversation_history)
        for sentence in ai_chat_ollama.stream_response_ollama(user_text, conversation_history):
            print(f"Bot (chunk): {sentence}")

            text_to_speech.speak(sentence)
            #text_to_speech.speak(ai_text)
            full_ai_response += sentence + " "
        conversation_history.append({"role": "user", "content": user_text})
        conversation_history.append({"role": "assistant", "content": full_ai_response.strip()})

if __name__ == '__main__':
    main()