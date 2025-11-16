from models import FantasyResponse, FantasyRequest, PlayerAdvice, ImageAnalysisResponse
from Parser import parse_ai_response

import os
import tempfile

from google import genai
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv


# ---------------------------------------------------------
# LOAD ENV + INIT CLIENT
# ---------------------------------------------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY is not set in .env")

client = genai.Client(api_key=API_KEY)

# ---------------------------------------------------------
# FASTAPI APP + CORS
# ---------------------------------------------------------
app = FastAPI(
    title="Fantasy Winners Backend",
    description="AI-powered fantasy football assistant (manual input + screenshots).",
    version="1.0.0",
)

# Allow React dev server, etc. You can tighten this later.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # For dev: allow all. For prod: restrict this.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# HELPER: BUILD MANUAL INPUT PROMPT
# ---------------------------------------------------------
def build_manual_prompt(request: FantasyRequest) -> str:
    """
    Build a text-only prompt that matches the SAME output format
    as AIprompt.txt (PLAYERS / ANALYSIS SUMMARY / ADVICE).
    This keeps parse_ai_response() working for both flows.
    """
    players_str = ", ".join(request.players)
    league = request.league or "Standard"

    prompt = f"""
You are an elite fantasy football analyst.

The user has manually entered this list of players:
{players_str}

Context:
- Week: {request.week}
- League format: {league}

TASK:
Analyze these players for this specific week and return start/sit guidance.

You MUST follow this exact output structure:

PLAYERS:
- <Player Name> — starter/bench (certainty: X%)

ANALYSIS SUMMARY:
- <bullet point summary 1>
- <bullet point summary 2>
- <bullet point summary 3>

ADVICE:
- <Player Name>:
      Recommendation: <Start/Sit/Flex/High-Risk Start/Safe Floor/Boom-Bust>
      Explanation: <1–3 sentence expert fantasy reasoning>
      Confidence: <float between 0.0 and 1.0>

Make sure the headings 'PLAYERS:', 'ANALYSIS SUMMARY:', and 'ADVICE:' appear
exactly as written so the response can be parsed by another system.
"""
    return prompt


# ---------------------------------------------------------
# MANUAL TEXT INPUT ENDPOINT
# ---------------------------------------------------------
@app.post("/manual_input", response_model=FantasyResponse)
async def manual_input(request: FantasyRequest) -> FantasyResponse:
    """
    User types in players manually (e.g. ['Puka Nacua', 'De'Von Achane']).
    We send a text-only prompt to Gemini and parse the structured advice.
    """
    try:
        prompt = build_manual_prompt(request)

        # Call Gemini text model
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        ai_text = response.text or ""

        # Parse AI text into structured players + advice
        players_list, advice_list = parse_ai_response(ai_text)

        # If parsing failed, fail loudly so frontend knows
        if not advice_list:
            raise HTTPException(
                status_code=500,
                detail="AI response could not be parsed into advice. Try rephrasing or check backend prompt."
            )

        return FantasyResponse(
            week=request.week,
            advice=advice_list
        )

    except HTTPException:
        # Re-raise custom HTTP errors
        raise
    except Exception as e:
        # Generic safety net
        raise HTTPException(
            status_code=500,
            detail=f"Error processing manual input: {str(e)}"
        )


# ---------------------------------------------------------
# SCREENSHOT UPLOAD ENDPOINT
# ---------------------------------------------------------
@app.post("/upload_image", response_model=ImageAnalysisResponse)
async def upload_image(file: UploadFile = File(...)) -> ImageAnalysisResponse:
    """
    User uploads a screenshot of their fantasy team / draft / waivers.
    We send the image + AIprompt.txt to Gemini Vision, parse the text
    output into structured players + advice, and return it.
    """
    temp_path = None

    try:
        # STEP 1 — Read uploaded file
        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(status_code=400, detail="Empty file upload.")

        # STEP 2 — Save to temp file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(image_bytes)
            temp_path = tmp.name

        # STEP 3 — Upload file to Gemini
        gemini_uploaded_file = client.files.upload(file=temp_path)

        # STEP 4 — Load vision/system prompt from AIprompt.txt
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(base_dir, "AIprompt.txt")

        if not os.path.exists(prompt_path):
            raise HTTPException(
                status_code=500,
                detail="AIprompt.txt not found on server."
            )

        with open(prompt_path, "r", encoding="utf-8") as f:
            vision_prompt = f.read()

        # STEP 5 — Call Gemini with prompt + image file
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[vision_prompt, gemini_uploaded_file]
        )

        ai_text = response.text or ""

        # STEP 6 — Parse AI text into structured data
        players_list, advice_list = parse_ai_response(ai_text)

        if not players_list and not advice_list:
            # We got something weird back; surface the raw text for debugging
            raise HTTPException(
                status_code=500,
                detail="AI response could not be parsed. Check prompt formatting or model output."
            )

        # STEP 7 — Return JSON
        return ImageAnalysisResponse(
            players=players_list,
            analysis=ai_text,
            advice=advice_list
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing uploaded image: {str(e)}"
        )
    finally:
        # Clean up temp file
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                # If delete fails, don't crash the request
                pass
