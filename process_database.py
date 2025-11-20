import json
import os

def calculate_crescendo_score(alliance_data, opponent_data):
    """
    Calculates the total score for an alliance in a Crescendo match.
    """
    # Convert string values to integers, defaulting to 0 if empty or invalid.
    try:
        leaves = int(alliance_data.get("Leaves", 0))
    except (ValueError, TypeError):
        leaves = 0

    auto_amp_notes = alliance_data.get("AutoAmpNotes", 0)
    auto_speaker_notes = alliance_data.get("AutoSpeakerNotes", 0)
    amp_notes = alliance_data.get("AmpNotes", 0)
    speaker_notes = alliance_data.get("SpeakerNotes", 0)
    amped_speaker_notes = alliance_data.get("AmpedSpeakerNotes", 0)
    stage_points = sum(alliance_data.get("Stage", []))
    
    # Points from opponent's fouls
    fouls = opponent_data.get("Fouls", 0)
    tech_fouls = opponent_data.get("TechFouls", 0)

    # Based on your formula: Leaves * 3 + AmpNotes * 2 + SpeakerNotes * 4 + AutoSpeakerNotes * 6 + Amped SpeakerNotes * 6 + Fouls
    # I have interpreted Fouls as points gained from opponent fouls.
    # Regular Foul = 2 pts, Tech Foul = 5 pts.
    score = (
        leaves * 2 +
        auto_amp_notes * 2 +
        auto_speaker_notes * 5 +
        amp_notes * 1 +
        speaker_notes * 2 +
        amped_speaker_notes * 5 +
        fouls_pts * 2 +
        tech_fouls_pts * 5 +
        stage_points
    )
    return score

def get_score_calculator(game_title):
    """
    Returns the appropriate score calculation function based on the game title.
    """
    if game_title.lower() == "crescendo":
        return calculate_crescendo_score
    # Add other games here in the future
    # elif game_title.lower() == "some_other_game":
    #     return calculate_some_other_game_score
    else:
        # Return a default calculator that returns 0 if game is not found
        return lambda alliance, opponent: 0

def process_database(input_path, output_path, game_title):
    """
    Reads match data from database.json, calculates scores, and writes to a new file.
    """
    try:
        with open(input_path, 'r') as f:
            db_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {input_path}")
        return

    score_calculator = get_score_calculator(game_title)
    
    processed_matches = []
    for match in db_data.get("matches", []):
        match_prefix = ""
        if match.get("type") == "Qualification":
            match_prefix = "Q"
        elif match.get("type") == "Playoff":
            match_prefix = "P"
        elif match.get("type") == "Final":
            match_prefix = "F"
        
        match_id = f"{match_prefix}{match.get('number', '')}"

        # Create simplified data dicts for the calculator
        red_data = {
            "Leaves": match.get("redLeaves"),
            "AutoSpeakerNotes": match.get("redAutoSpeakerNotes"),
            "AmpNotes": match.get("redAmpNotes"),
            "SpeakerNotes": match.get("redSpeakerNotes"),
            "AmpedSpeakerNotes": match.get("redAmpedSpeakerNotes"),
            "Stage": match.get("redStage", []),
        }
        blue_data = {
            "Leaves": match.get("blueLeaves"),
            "AutoSpeakerNotes": match.get("blueAutoSpeakerNotes"),
            "AutoAmpNotes": match.get("blueAutoAmpNotes"),
            "AmpNotes": match.get("blueAmpNotes"),
            "SpeakerNotes": match.get("blueSpeakerNotes"),
            "AmpedSpeakerNotes": match.get("blueAmpedSpeakerNotes"),
            "Stage": match.get("blueStage", []),
        }
        
        # Data about opponent fouls
        red_opponent_fouls = {"Fouls": match.get("blueFouls", 0), "TechFouls": match.get("blueTechFouls", 0)}
        blue_opponent_fouls = {"Fouls": match.get("redFouls", 0), "TechFouls": match.get("redTechFouls", 0)}

        red_score = score_calculator(red_data, red_opponent_fouls)
        blue_score = score_calculator(blue_data, blue_opponent_fouls)

        processed_match = {
            "match_id": match_id,
            "red_alliance": match.get("redTeams", []),
            "blue_alliance": match.get("blueTeams", []),
            "score_red": red_score,
            "score_blue": blue_score
        }
        processed_matches.append(processed_match)

    output_data = {"matches": processed_matches}

    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Successfully processed data and saved to {output_path}")

if __name__ == "__main__":
    # Assuming the script is in the BORC directory.
    # The game title can be dynamically determined or passed as an argument.
    EVENT_FOLDER = os.path.join("events", "minifrc10")
    INPUT_FILE = os.path.join(EVENT_FOLDER, "database.json")
    OUTPUT_FILE = os.path.join(EVENT_FOLDER, "processed_matches.json")
    GAME_TITLE = "Crescendo" # This could come from event_data.json in a more advanced script

    process_database(INPUT_FILE, OUTPUT_FILE, GAME_TITLE)
