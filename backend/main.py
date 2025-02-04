# uvicorn main:app
# uvicorn main:app --reload

# Importing necessary libraries
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import ollama

# Importing our fuctions
from functions.llm_requests import convert_audio_to_text, get_chat_response
from functions.database import store_messages

# Defining the FastAPI app
app = FastAPI()


# CORS - Origins
origins = ["http://localhost:5173",
           "http://localhost:5174",
           "http://localhost:4173",
           "http://localhost:4174",
           "http://localhost:3000"]


# CORS - middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# check health of the API
@app.get("/health")
async def check_health():
    return {"message": "Heealthy API"} 

# Get audio
@app.get("/audio-get/")
async def get_audio():
    
    # Get the saved audio file
    audio_input = "./files/audio/test_audio.mp3"

    # Dcoding the audio
    decoded_message = convert_audio_to_text(audio_input)

    if not decoded_message:
        raise HTTPException(status_code=400, detail="Failed to decode the audio")
    

    # get our llama response
    chat_response = get_chat_response(decoded_message)

    store_messages(decoded_message, chat_response)
    print(chat_response)
    return "DONE"


# API endpoint to sending data
# Note: Not playing in the browser using post request
# @app.post("/post-audio/")
# async def post_audio(file: UploadFile = File(...)):
#     pass