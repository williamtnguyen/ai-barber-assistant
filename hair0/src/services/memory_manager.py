"""
Memory Manager for Beverage Preferences using Self-Hosted Mem0

Handles user preference storage and retrieval using local ChromaDB vector database.
"""

import logging
from typing import List, Dict, Optional
from mem0 import Memory
from src.config.config import MEM0_CONFIG, DEFAULT_USER_ID

logger = logging.getLogger(__name__)


class BeverageMemoryManager:
    """Manages user beverage preferences using self-hosted mem0."""

    def __init__(self):
        """Initialize the memory manager with self-hosted configuration."""
        self.user_id = DEFAULT_USER_ID

        try:
            self.memory = Memory.from_config(MEM0_CONFIG)
            logger.info("Beverage memory manager initialized with mem0")
        except Exception as e:
            logger.error(f"Failed to initialize mem0: {e}")
            raise RuntimeError(f"Memory system initialization failed: {e}")

    def add_preference(self, preference_text: str) -> bool:
        """Add a user preference to memory."""
        try:
            result = self.memory.add(preference_text, user_id=self.user_id)
            logger.info(f"Added preference: {preference_text}")
            return True
        except Exception as e:
            logger.error(f"Error adding preference: {e}")
            raise

    def get_preferences(
        self, query: str = "beverage preferences", limit: int = 10
    ) -> List[Dict]:
        """Retrieve user preferences from memory."""
        try:
            response = self.memory.search(query, user_id=self.user_id, limit=limit)
            # Handle dict response from mem0
            if isinstance(response, dict) and "results" in response:
                return response["results"]
            elif isinstance(response, list):
                return response
            else:
                logger.warning(f"Unexpected response type: {type(response)}")
                return []
        except Exception as e:
            logger.error(f"Error retrieving preferences: {e}")
            raise

    def update_from_rating(
        self,
        drink_name: str,
        rating: int,
        notes: Optional[str] = "",
        flavor_profile: str = "",
    ) -> bool:
        """Update preferences based on drink rating."""
        try:
            if rating >= 4:
                # High rating - add as positive preference
                preference_text = f"User loves {drink_name} (rating: {rating}/5)"
                if flavor_profile:
                    preference_text += f" with flavors: {flavor_profile}"
                if notes:
                    preference_text += f". Notes: {notes}"

                self.memory.add(preference_text, user_id=self.user_id)
                logger.info(f"Added positive preference for {drink_name}")

            elif rating <= 2:
                # Low rating - add as negative preference
                preference_text = f"User dislikes {drink_name} (rating: {rating}/5)"
                if flavor_profile:
                    preference_text += f" with flavors: {flavor_profile}"
                if notes:
                    preference_text += f". Notes: {notes}"

                self.memory.add(preference_text, user_id=self.user_id)
                logger.info(f"Added negative preference for {drink_name}")

            return True

        except Exception as e:
            logger.error(f"Error updating preferences from rating: {e}")
            raise

    def get_flavor_preferences(self) -> Dict[str, List[str]]:
        """Get organized flavor preferences (liked vs disliked)."""
        try:
            # Search for positive and negative preferences with broader patterns
            liked_response = self.memory.search(
                "flavors", user_id=self.user_id, limit=50
            )

            liked_flavors = []
            disliked_flavors = []

            # Extract results from response
            results = []
            if isinstance(liked_response, dict) and "results" in liked_response:
                results = liked_response["results"]
            elif isinstance(liked_response, list):
                results = liked_response

            # Extract flavor information from results
            for result in results:
                if isinstance(result, dict) and "memory" in result:
                    text = result["memory"].lower()

                    # Look for positive patterns (loves, enjoys, appreciates, rating 4-5)
                    is_positive = any(
                        word in text
                        for word in [
                            "loves",
                            "enjoys",
                            "appreciates",
                            "rating: 4",
                            "rating: 5",
                            "5/5 rating",
                            "4/5 rating",
                        ]
                    )

                    # Look for negative patterns (dislikes, hates, rating 1-2)
                    is_negative = any(
                        word in text
                        for word in [
                            "dislikes",
                            "hates",
                            "rating: 1",
                            "rating: 2",
                            "1/5 rating",
                            "2/5 rating",
                        ]
                    )

                    # Extract flavors from the text
                    if "flavors:" in text:
                        flavors_part = text.split("flavors:")[1].split(".")[0].strip()
                        flavors = [f.strip() for f in flavors_part.split(",")]

                        if is_positive and not is_negative:
                            liked_flavors.extend(flavors)
                        elif is_negative and not is_positive:
                            disliked_flavors.extend(flavors)

            return {
                "liked_flavors": list(set(liked_flavors)),
                "disliked_flavors": list(set(disliked_flavors)),
            }

        except Exception as e:
            logger.error(f"Error getting flavor preferences: {e}")
            return {"liked_flavors": [], "disliked_flavors": []}

    def get_category_preferences(self) -> Dict[str, str]:
        """Get user preferences by beverage category."""
        try:
            categories = ["beer", "wine", "spirits", "cocktails"]
            preferences = {}

            for category in categories:
                response = self.memory.search(
                    f"{category} preferences", user_id=self.user_id, limit=5
                )

                # Extract results from response
                results = []
                if isinstance(response, dict) and "results" in response:
                    results = response["results"]
                elif isinstance(response, list):
                    results = response

                positive_count = 0
                negative_count = 0

                for result in results:
                    if isinstance(result, dict) and "memory" in result:
                        text = result["memory"].lower()
                        if (
                            "loves" in text
                            or "rating: 4" in text
                            or "rating: 5" in text
                        ):
                            positive_count += 1
                        elif (
                            "dislikes" in text
                            or "rating: 1" in text
                            or "rating: 2" in text
                        ):
                            negative_count += 1

                if positive_count > negative_count:
                    preferences[category] = "positive"
                elif negative_count > positive_count:
                    preferences[category] = "negative"
                else:
                    preferences[category] = "neutral"

            return preferences

        except Exception as e:
            logger.error(f"Error getting category preferences: {e}")
            raise

    def get_user_profile_summary(self) -> Dict:
        """Get a comprehensive summary of user preferences."""
        try:
            flavor_prefs = self.get_flavor_preferences()
            category_prefs = self.get_category_preferences()

            # Get recent preferences
            recent_response = self.memory.search(
                "user preferences", user_id=self.user_id, limit=10
            )
            recent_prefs = []
            if isinstance(recent_response, dict) and "results" in recent_response:
                recent_prefs = recent_response["results"]
            elif isinstance(recent_response, list):
                recent_prefs = recent_response

            return {
                "flavor_preferences": flavor_prefs,
                "category_preferences": category_prefs,
                "recent_activity_count": len(recent_prefs),
                "user_id": self.user_id,
            }

        except Exception as e:
            logger.error(f"Error getting user profile summary: {e}")
            raise


# Global instance
memory_manager = None


def get_memory_manager() -> BeverageMemoryManager:
    """Get or create the global memory manager instance."""
    global memory_manager
    if memory_manager is None:
        memory_manager = BeverageMemoryManager()
    return memory_manager
