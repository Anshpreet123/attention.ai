# backend/agents/user_interaction_agent.py
from typing import Dict

class UserInteractionAgent:
    def gather_preferences(self, data: Dict):
        # Gather data like city, budget, interests, etc.
        return {
            "city": data.get("city", ""),
            "budget": data.get("budget", ""),
            "interests": data.get("interests", [])
        }
