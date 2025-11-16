from typing import List, Optional
from pydantic import BaseModel

# ---------------------------------------------------------
# USER MANUAL INPUT MODEL
# ---------------------------------------------------------
class FantasyRequest(BaseModel):
    players: List[str]                  # List of manually typed players
    week: int                           # NFL week number
    league: Optional[str] = None        # PPR, Half-PPR, Standard, etc.


# ---------------------------------------------------------
# STRUCTURED PLAYER ADVICE FROM AI
# ---------------------------------------------------------
class PlayerAdvice(BaseModel):
    player: str                         # One player per advice entry
    recommendation: str                 # "Start", "Sit", "Flex", etc.
    explanation: str                    # Short reasoning
    confidence: float                   # 0.0 to 1.0 confidence score


# ---------------------------------------------------------
# RESPONSE FOR MANUAL PLAYER INPUT
# ---------------------------------------------------------
class FantasyResponse(BaseModel):
    week: int                           # Echo week back to frontend
    advice: List[PlayerAdvice]          # List of recommendations


# ---------------------------------------------------------
# RESPONSE FOR SCREENSHOT-BASED INPUT
# ---------------------------------------------------------
class ImageAnalysisResponse(BaseModel):
    players: List[str]                  # Extracted names from screenshot
    analysis: str                       # Raw AI text (debug / display)
    advice: List[PlayerAdvice]          # Structured recommendations
