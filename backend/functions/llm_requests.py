import whisper
import ollama

from functions.database import get_recent_messages

# Convert Audio to Text
def convert_audio_to_text(audio_file):
    try:
        model = whisper.load_model("base")
        transcript = model.transcribe(audio_file)

        return transcript["text"]
    except Exception as e:
        print(f"Exception has occured: {e}")
        return

# llama3.2b model - Get response from the model
def get_chat_response(message_input):
    messages = get_recent_messages()
    user_message = {"role": "user", "content": message_input}

    messages.append(user_message)

    try:
        response = ollama.chat(
            model="llama3.2:latest",
            messages=messages,
        )
        message_text = response.message.content
        return message_text
    except Exception as e:
        print(f"Exception has occured: {e}")
        return