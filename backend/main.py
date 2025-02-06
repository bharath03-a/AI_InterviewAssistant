# uvicorn main:app
# uvicorn main:app --reload

# Importing necessary libraries
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

# Importing our fuctions
from functions.llm_requests import convert_audio_to_text, get_chat_response
from functions.database import reset_messages, store_messages
from functions.text_to_speech import convert_text_to_speech

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

# restting the db
@app.get("/reset/")
async def reset_db():
    reset_messages()
    return {"message": "DB has been reset"}

# Get audio
@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):
    
    # Get the saved audio file
    # audio_input = "./files/audio/test_audio.mp3"

    # save file from frontend
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())

    audio_input = open(file.filename, "rb")

    # Dcoding the audio
    decoded_message = convert_audio_to_text(file.filename)

    if not decoded_message:
        raise HTTPException(status_code=400, detail="Failed to decode the audio")
    
    # get our llama response
    chat_response = get_chat_response(decoded_message)

    if not chat_response:
        raise HTTPException(status_code=400, detail="Failed to get chat response")
    print(chat_response)

    store_messages(decoded_message, chat_response)

    # convert the response to audio
    audio_output = convert_text_to_speech(chat_response)

    if not audio_output:
        raise HTTPException(status_code=400, detail="Failed to get Eleven labs audio response")
    
    # create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    return StreamingResponse(iterfile(), media_type="application/octet-stream")


# API endpoint to sending data
# Note: Not playing in the browser using post request
# @app.post("/post-audio/")
# async def post_audio(file: UploadFile = File(...)):
#     pass