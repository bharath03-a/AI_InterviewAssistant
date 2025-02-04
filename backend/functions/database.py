import os
import json
import random

# Get recent messages
def get_recent_messages():

    # defining parameters
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_name = os.path.join(base_dir, 'files', 'db', 'stored_data.json')
    learn_instructions = {
        "role": "system",
        "content": "You are interviewing the user for a job as a retail assistant. Ask short questions that are relevant to the junior position. Your name is Rachel and the use is called Lada. Keep your answers to under 30 words."
    }

    # Initialize messages
    messages = []

    # add randomness
    x = random.uniform(0, 1)
    if x < 0.5:
        learn_instructions["content"] = learn_instructions["content"] + " Your response will include some dry humour."
    else:
        learn_instructions["content"] = learn_instructions["content"] + " Your response will include a rather challenging question."

    # Append instructions to message
    messages.append(learn_instructions)

    # getting history of messages
    try:
        if os.path.getsize(file_name) > 0:
            with open(file_name, "r") as file:
                data = json.load(file)
                # appending last 5 messages
                if data:
                    if len(data) < 5:
                        for item in data:
                            messages.append(item)
                    else:
                        for item in data[-5:]:
                            messages.append(item)
    except Exception as e:
        print(f"Exception has occured: {e}")
        pass

    return messages

def store_messages(request_message, response_message):
    
    # defining parameters
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_name = os.path.join(base_dir, 'files', 'db', 'stored_data.json')

    # recent messages
    messages = get_recent_messages()[1:]

    # adding messages 
    user_message =  {"role": "user", "content": request_message}
    assistant_message = {"role": "assistant", "content": response_message}

    messages.append(user_message)
    messages.append(assistant_message)

    with open(file_name, "w") as file:
        json.dump(messages, file, indent=4)