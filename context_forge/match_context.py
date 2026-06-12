# context_forge/match_context.py
# DecisionLens Context Forge MCP stub
# Provides mock match metadata via the Model Context Protocol provider pattern.
# In production: replace mock data with a live football-data.org feed.

class MatchContextProvider:
    """Context Forge MCP-style provider for match metadata."""

    MOCK_CONTEXT = {
        "match": "Group Stage Match, FIFA World Cup 2026",
        "minute": 74,
        "score": "1-1",
        "yellow_cards": {"home": 2, "away": 1},
        "red_cards": {"home": 0, "away": 0},
        "venue": "MetLife Stadium, New Jersey"
    }

    def get_context(self) -> dict:
        return self.MOCK_CONTEXT

    def format_for_prompt(self) -> str:
        ctx = self.MOCK_CONTEXT
        return (f"Match context (for situational awareness only, "
                f"not used as rule evidence): {ctx['match']}, "
                f"minute {ctx['minute']}, score {ctx['score']}, "
                f"yellow cards: home {ctx['yellow_cards']['home']} "
                f"away {ctx['yellow_cards']['away']}.")
