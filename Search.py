import json
import re

def extract_cards_section(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        json_content = file.read()

    # Regular expression to find the "Cards": [ section that follows a closing square bracket
    pattern = re.compile(r'\],\s*"Cards":\s*\[([^]]*)\]', re.DOTALL)
    match = pattern.search(json_content)

    if match:
        cards_section = match.group(1)
        try:
            cards_data = json.loads(f"[{cards_section.strip()}]")
            return cards_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        print("No matching section found")
        return None

# Load JSON data from CollectionState.JSON
file_path = 'CollectionState.JSON'
try:
    data = extract_cards_section(file_path)
    if data is None:
        exit(1)
except FileNotFoundError:
    print("Error: FileNotFoundError - CollectionState.JSON file not found.")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Error: JSONDecodeError - {e}")
    exit(1)

# Extract relevant information and filter out entries with "Custom": true
cards_info = []
for card in data:
    if "Custom" in card and card["Custom"] == True:
        continue  # Skip entries where Custom is true

    card_def_id = card.get('CardDefId', '')
    surface_effect_def_id = card.get('SurfaceEffectDefId', '')
    reveal_effect_def_id = card.get('CardRevealEffectDefId', '')

    if card_def_id and surface_effect_def_id:
        if reveal_effect_def_id:
            # Check if the reveal effect is one of the known colors
            if any(color in reveal_effect_def_id for color in ["Black", "Gold", "Green", "Blue", "Red", "White", "Purple"]):
                cards_info.append(f"{card_def_id} {surface_effect_def_id} {reveal_effect_def_id}")
            else:
                # Append "Rainbow" to specific card types
                if reveal_effect_def_id in ["Comic", "Glimmer", "Kirby", "Sparkle"]:
                    cards_info.append(f"{card_def_id} {surface_effect_def_id} {reveal_effect_def_id}Rainbow")
                else:
                    cards_info.append(f"{card_def_id} {surface_effect_def_id} Rainbow")
        else:
            cards_info.append(f"{card_def_id} {surface_effect_def_id}")

# Sort the cards alphabetically by CardDefId
cards_info.sort()

# Write sorted information to a text file
try:
    with open('output.txt', 'w', encoding='utf-8') as outfile:
        for card_info in cards_info:
            outfile.write(f"{card_info}\n")

    print("Output written to output.txt")
except IOError as e:
    print(f"Error: IOError - {e}")
    exit(1)
