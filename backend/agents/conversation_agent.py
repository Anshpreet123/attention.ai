# backend/agents/conversation_agent.py
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class ConversationAgent:
    def __init__(self, model_name="distilgpt2"):
        # Load the lightweight distilgpt2 model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.user_histories = {}  # Dictionary to store conversation history per user

    def get_response(self, user_id, user_input):
        # Initialize or retrieve the user's chat history
        if user_id not in self.user_histories:
            self.user_histories[user_id] = None  # Start with no history for a new user

        # Encode the new user input and append to conversation history
        new_input_ids = self.tokenizer.encode(user_input + self.tokenizer.eos_token, return_tensors="pt")

        # Append new input to existing history, or start fresh if no history
        bot_input_ids = torch.cat([self.user_histories[user_id], new_input_ids], dim=-1) if self.user_histories[user_id] is not None else new_input_ids

        # Generate response with a specified max_new_tokens limit
        self.user_histories[user_id] = self.model.generate(
            bot_input_ids,
            max_new_tokens=100,  # Set the max number of tokens to generate for the response
            pad_token_id=self.tokenizer.eos_token_id
        )

        # Decode only the new part of the response
        response = self.tokenizer.decode(self.user_histories[user_id][:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        return response
