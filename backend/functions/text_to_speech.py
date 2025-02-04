import requests
from decouple import config

ELEVEN_LABS_API = config("ELEVEN_LABS_API_KEY")

def convert_text_to_speech(message):
    """
    Function that converts text to speech
    """

    body = {
        "text": message,
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0,
        }
    }

    voice_rachel = "LcfcDJNUP1GQjkzn1xUU"
    
    headers = { "xi-api-key": ELEVEN_LABS_API, 
               "Content-Type": "application/json",
               "accept": "audio/mpeg"}
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_rachel}"

    try:
        response = requests.post(endpoint, headers=headers, json=body)
    except Exception as e:
        print(f"Exception has occured: {e}")
        return
    
    if response.status_code == 200:
        return response.content
    else:
        return
