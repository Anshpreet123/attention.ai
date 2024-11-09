# # backend/main.py
# from fastapi import FastAPI,Request,Response
# from .agents.conversation_agent import ConversationAgent
# from .agents.user_interaction_agent import UserInteractionAgent
# from .agents.itinerary_agent import ItineraryAgent
# from pydantic import BaseModel

# session_data = {}
# conversation_agent = ConversationAgent()
# app = FastAPI()

# class ChatRequest(BaseModel):
#     user_input: str

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the One-Day Tour Planning API"}

# user_agent = UserInteractionAgent()
# itinerary_agent = ItineraryAgent()

# # @app.post("/preferences")
# # async def set_preferences(request: Request):
# #     data = await request.json()
# #     # Assuming 'user_agent.gather_preferences' processes and returns the input
# #     preferences = user_agent.gather_preferences(data)
    
# #     return preferences
# @app.post("/preferences")
# async def set_preferences(request: Request, response: Response):
#     # Parse incoming JSON data
#     data = await request.json()
#     city = data.get("city")
#     budget = data.get("budget")
#     interests = data.get("interests", [])

#     # Validate that necessary fields are present
#     if not city or budget is None:
#         return {"error": "City and budget are required"}, 400

#     # Store the preferences in session_data
#     session_data["preferences"] = {
#         "city": city,
#         "budget": budget,
#         "interests": interests
#     }
#     return {"status": "Preferences set"}

# @app.post("/itinerary")
# async def generate_itinerary(preferences: dict):
#     # Use preferences to create a dynamic itinerary, here’s a mock example for illustration
#     # Replace this mock with real logic if available
#     city = preferences.get("city", "Unknown City")
#     budget = preferences.get("budget", 0)
#     interests = preferences.get("interests", [])

#     itinerary = [
#         {"stop": f"Popular Spot in {city}", "time": "10:00 AM", "cost": 20 if budget > 500 else 10},
#         {"stop": f"Famous Park in {city}", "time": "12:00 PM", "cost": 0},
#         {"stop": f"Historic Site in {city}", "time": "2:00 PM", "cost": 15 if "culture" in interests else 5}
#     ]

#     return itinerary

# @app.post("/chat")
# async def chat(request: Request):
#     # Parse incoming JSON data
#     data = await request.json()
#     user_input = data.get("user_input")

#     # Ensure user preferences are set before chatting
#     if "preferences" not in session_data:
#         return {"response": "Please set your preferences first."}

#     # Generate a response based on the session's conversation history
#     response_text = conversation_agent.get_response("default_session", user_input)
#     return {"response": response_text}

# backend/main.py
from fastapi import FastAPI, Request, Response
from .agents.conversation_agent import ConversationAgent
from .agents.user_interaction_agent import UserInteractionAgent
from .agents.itinerary_agent import ItineraryAgent

app = FastAPI()

# Initialize session data and agents
session_data = {"chat_history": []}  # Store chat history without user ID
conversation_agent = ConversationAgent()
user_agent = UserInteractionAgent()
itinerary_agent = ItineraryAgent()

@app.get("/")
def read_root():
    return {"message": "Welcome to the One-Day Tour Planning API"}

@app.post("/preferences")
async def set_preferences(request: Request, response: Response):
    # Parse incoming JSON data
    data = await request.json()
    city = data.get("city")
    budget = data.get("budget")
    interests = data.get("interests", [])

    # Validate that necessary fields are present
    if not city or budget is None:
        return {"error": "City and budget are required"}, 400

    # Store the preferences in session_data
    session_data["preferences"] = {
        "city": city,
        "budget": budget,
        "interests": interests
    }
    return {"status": "Preferences set"}

@app.post("/itinerary")
async def generate_itinerary(request: Request):
    # Use session preferences to create a dynamic itinerary
    preferences = session_data.get("preferences", {})
    city = preferences.get("city", "Unknown City")
    budget = preferences.get("budget", 0)
    interests = preferences.get("interests", [])

    itinerary = [
        {"stop": f"Popular Spot in {city}", "time": "10:00 AM", "cost": 20 if budget > 500 else 10},
        {"stop": f"Famous Park in {city}", "time": "12:00 PM", "cost": 0},
        {"stop": f"Historic Site in {city}", "time": "2:00 PM", "cost": 15 if "culture" in interests else 5}
    ]

    return itinerary

@app.post("/chat")
async def chat(request: Request):
    # Parse incoming JSON data
    data = await request.json()
    user_input = data.get("user_input")

    # Ensure user preferences are set before chatting
    if "preferences" not in session_data:
        return {"response": "Please set your preferences first."}

    # Generate a response from the conversation agent
    response_text = conversation_agent.get_response("default_session", user_input)

    # Append to chat history
    session_data["chat_history"].append(("User", user_input))
    session_data["chat_history"].append(("Assistant", response_text))

    return {"response": response_text, "chat_history": session_data["chat_history"]}
