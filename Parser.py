from models import PlayerAdvice

def parse_ai_response(ai_text: str):
    players_list = []
    advice_list = []

    # -----------------------------
    # PARSE PLAYERS SECTION
    # -----------------------------
    start = ai_text.find("PLAYERS:")
    end = ai_text.find("ANALYSIS SUMMARY")

    if start == -1 or end == -1:
        return [], []

    players_chunk = ai_text[start + len("PLAYERS:"): end]

    for line in players_chunk.split("\n"):
        line = line.strip()
        if line.startswith("-"):
            raw = line[1:].strip()

            # FIX: support both em dash and hyphen
            name = raw.split("—")[0].split("-")[0].strip()

            players_list.append(name)

    # -----------------------------
    # PARSE ADVICE SECTION
    # -----------------------------
    starx = ai_text.find("ADVICE:")
    if starx == -1:
        return players_list, []

    advice_section = ai_text[starx + len("ADVICE:"):]

    # Split into each player block
    blocks = advice_section.split("\n-")
    use_blocks = blocks[1:]  # skip text before first dash

    for inside in use_blocks:
        lines = [l.strip() for l in inside.splitlines() if l.strip()]

        if not lines:
            continue

        # First line contains: "PlayerName: <something>"
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

        # Now matches your updated PlayerAdvice model (player is a string)
        advice_list.append(
            PlayerAdvice(
                player=name,
                recommendation=recommendation,
                explanation=explanation,
                confidence=confidence
            )
        )

    return players_list, advice_list
