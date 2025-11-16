from models import FantasyResponse, FantasyRequest, PlayerAdvice, ImageAnalysisResponse
import os
import tempfile
from google import genai

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
from Parser import parse_ai_response


# ------------------------------------
# LOAD API KEY FROM .env
# ------------------------------------
load_dotenv()

# Create FastAPI app
app = FastAPI()

# Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Allow all origins (React dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


# ---------------------------------------------------------
# MANUAL TEXT INPUT ENDPOINT
# ---------------------------------------------------------
@app.post("/manual_input", response_model=FantasyResponse)
async def manual_input(request: FantasyRequest):

    prompt = f"""
    You are an expert fantasy football analyst.
    The user manually entered the following players:

    {", ".join(request.players)}

    Week: {request.week}
    League format: {request.league or "standard"}

    Provide start/sit recommendations WITH:
    - Recommendation: Start/Sit
    - Explanation: 1–2 sentences
    - Confidence: 0.00 to 1.00

    Use this exact structure:

    PLAYERS:
    - Player Name — Position

    ANALYSIS SUMMARY:
    <text>

    ADVICE:
    - Player Name:
        Recommendation: <Start/Sit>
        Explanation: <why>
        Confidence: <0.00>
    """

    # Call Gemini
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=prompt
    )

    ai_text = response.text
    players_list, advice_list = parse_ai_response(ai_text)

    return FantasyResponse(
        week=request.week,
        advice=advice_list
    )



# ---------------------------------------------------------
# SCREENSHOT UPLOAD ENDPOINT
# ---------------------------------------------------------
@app.post("/fantasy_team_screenshot", response_model=ImageAnalysisResponse)
async def upload_image(file: UploadFile = File(...)):

    # STEP 1 — Read uploaded file bytes
    image_bytes = await file.read()

    # STEP 2 — Save to temp file for Gemini
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(image_bytes)
        temp_path = tmp.name

    gemini_uploaded_file = client.files.upload(file=temp_path)

    # STEP 3 — Load vision prompt
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROMPT_PATH = os.path.join(BASE_DIR, "AIprompt.txt")

    with open(PROMPT_PATH, "r") as f:
        prompt = f.read()

    # STEP 4 — Call Gemini Vision model
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt, gemini_uploaded_file]
    )

    ai_text = response.text

    # STEP 5 — Parse AI text into structured data
    players_list, advice_list = parse_ai_response(ai_text)

    # STEP 6 — Return JSON
    return ImageAnalysisResponse(
        players=players_list,
        analysis=ai_text,
        advice=advice_list
    )
