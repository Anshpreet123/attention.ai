# # frontend/app.py
# # import streamlit as st
# # import requests

# # st.title("One-Day Tour Planner")

# # city = st.text_input("Enter the city you'd like to visit")
# # budget = st.number_input("Enter your budget for the day", min_value=0)

# # if st.button("Plan My Tour"):
# #     response = requests.post("http://localhost:8000/preferences", json={
# #         "city": city, "budget": budget, "interests": ["culture", "food"]
# #     })
# #     st.write(response.json())

# # frontend/app.py
# import streamlit as st
# import requests

# st.title("One-Day Tour Planner")

# # Tour Planner Inputs
# st.header("Plan Your Tour")
# city = st.text_input("Enter the city you'd like to visit")
# budget = st.number_input("Enter your budget for the day", min_value=0)

# if st.button("Plan My Tour"):
#     response = requests.post("http://localhost:8000/preferences", json={
#         "city": city, "budget": budget, "interests": ["culture", "food"]
#     })
#     st.write(response.json())

# # Itinerary Generation Button
# if st.button("Generate Itinerary"):
#     itinerary_response = requests.post("http://localhost:8000/itinerary", json={
#         "city": city, "budget": budget, "interests": ["culture", "food"]
#     })
#     if itinerary_response.status_code == 200:
#         itinerary = itinerary_response.json()
#         st.header("Your Itinerary")
#         for stop in itinerary:
#             st.write(f"**Stop**: {stop['stop']}")
#             st.write(f"**Time**: {stop['time']}")
#             st.write(f"**Cost**: ${stop['cost']}")
#     else:
#         st.write("Failed to generate itinerary. Please try again.")

# # Chat Interface
# st.header("Chat with the Tour Assistant")

# # Initialize chat history in session state
# if "chat_history" not in st.session_state:
#     st.session_state["chat_history"] = []

# # Get user input
# user_input = st.text_input("Type your message:")

# if st.button("Send"):
#     try:
#         response = requests.post("http://localhost:8000/chat", json={"user_input": user_input})
#         if response.status_code == 200:
#             st.write("Assistant:", response.json().get("response"))
#         else:
#             st.write("Error:", response.status_code, response.text)
#     except Exception as e:
#         st.write("Connection error:", e)
        
# # Display chat history
# for speaker, message in st.session_state.chat_history:
#     if speaker == "User":
#         st.write(f"**{speaker}:** {message}")
#     else:
#         st.write(f"**{speaker}:** {message}")

import streamlit as st
import requests

st.title("One-Day Tour Planner")

# Tour Planner Inputs
st.header("Plan Your Tour")
city = st.text_input("Enter the city you'd like to visit")
budget = st.number_input("Enter your budget for the day", min_value=0)

if st.button("Plan My Tour"):
    # Make the API request to set preferences
    response = requests.post("http://localhost:8000/preferences", json={
        "city": city, "budget": budget, "interests": ["culture", "food"]
    })

    # Display the JSON response in a pretty format
    if response.status_code == 200:
        st.write("Tour Preferences Set:")
        st.json(response.json())  # Display JSON response in Streamlit
    else:
        st.write("Failed to set preferences. Please try again.")

# Itinerary Generation Button
if st.button("Generate Itinerary"):
    itinerary_response = requests.post("http://localhost:8000/itinerary", json={
        "city": city, "budget": budget, "interests": ["culture", "food"]
    })
    if itinerary_response.status_code == 200:
        itinerary = itinerary_response.json()
        st.header("Your Itinerary")
        for stop in itinerary:
            st.write(f"**Stop**: {stop['stop']}")
            st.write(f"**Time**: {stop['time']}")
            st.write(f"**Cost**: ${stop['cost']}")
        # Show the raw JSON response for the itinerary
        st.subheader("Itinerary JSON Response:")
        st.json(itinerary_response.json())
    else:
        st.write("Failed to generate itinerary. Please try again.")

# Chat Interface
st.header("Chat with the Tour Assistant")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Get user input
user_input = st.text_input("Type your message:")

if st.button("Send"):
    try:
        response = requests.post("http://localhost:8000/chat", json={"user_input": user_input})
        if response.status_code == 200:
            response_data = response.json()
            assistant_reply = response_data.get("response")

            # Update session chat history
            st.session_state.chat_history.append(("User", user_input))
            st.session_state.chat_history.append(("Assistant", assistant_reply))

            # Display the assistant's reply
            st.write("Assistant:", assistant_reply)
        else:
            st.write("Error:", response.status_code, response.text)
    except Exception as e:
        st.write("Connection error:", e)

# Display chat history
st.header("Chat History")
for speaker, message in st.session_state.chat_history:
    st.write(f"**{speaker}:** {message}")
