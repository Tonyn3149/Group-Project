from models import PlayerAdvice

def parse_ai_response(ai_text: str):
    """
    Extracts:
      - players list
      - advice list (PlayerAdvice objects)
    from Gemini output following the required format.

    Returns:
        (players_list, advice_list)
    """

    players_list = []
    advice_list = []

    # Normalize text to avoid casing issues
    text = ai_text.replace("\r", "")

    # ---------------------------------------------------------
    # PARSE PLAYERS SECTION
    # ---------------------------------------------------------
    start = text.find("PLAYERS:")
    end = text.find("ANALYSIS SUMMARY")

    if start == -1 or end == -1:
        # If sections missing → return empty but safe
        return [], []

    players_chunk = text[start + len("PLAYERS:"): end]

    for line in players_chunk.split("\n"):
        line = line.strip()
        if line.startswith("-"):
            raw = line[1:].strip()

            # Handle both “—” and "-" separating player from attributes
            if "—" in raw:
                name = raw.split("—")[0].strip()
            elif "-" in raw:
                name = raw.split("-")[0].strip()
            else:
                name = raw.strip()

            if name:
                players_list.append(name)

    # ---------------------------------------------------------
    # PARSE ADVICE SECTION
    # ---------------------------------------------------------
    advice_start = text.find("ADVICE:")
    if advice_start == -1:
        return players_list, []

    advice_section = text[advice_start + len("ADVICE:"):]

    # Blocks begin with "- PlayerName:"
    blocks = advice_section.split("\n-")

    # Skip anything before the first "-"
    for block in blocks[1:]:
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        if not lines:
            continue

        # First line example: "Puka Nacua:"
        name_line = lines[0]
        name = name_line.split(":", 1)[0].strip()

        recommendation = ""
        explanation = ""
        confidence = 0.0

        for line in lines[1:]:
            if line.startswith("Recommendation"):
                recommendation = line.split(":", 1)[1].strip()

            elif line.startswith("Explanation"):
                explanation = line.split(":", 1)[1].strip()

            elif line.startswith("Confidence"):
                try:
                    confidence = float(line.split(":", 1)[1].strip())
                except:
                    confidence = 0.0

        # Append parsed advice object
        advice_list.append(
            PlayerAdvice(
                player=name,
                recommendation=recommendation,
                explanation=explanation,
                confidence=confidence
            )
        )

    return players_list, advice_list
