import re


def extract_sos(message: str):
    text = message.strip()
    lower = text.lower()

    result = {
        "source_type": "INDIVIDUAL_SOS",

        "location": {
            "text": None,
            "latitude": None,
            "longitude": None
        },

        "people": {
            "total": None,
            "children": None,
            "elderly": None,
            "pregnant": None,
            "injured": None,
            "missing": None,
            "mobility_impaired": None
        },

        "situation": None,

        "request": {
            "type": None,
            "resources": []
        },

        "needs": {
            "food": False,
            "water": False,
            "medicine": False,
            "shelter": False,
            "rescue": False,
            "medical_transfer": False
        },

        "contact_info": [],
        "original_message": text
    }

    # -------------------------
    # PEOPLE COUNT
    # -------------------------
    people_match = re.search(
        r'\b(\d+)\s+(?:people|persons|members|adults|individuals)\b',
        lower
    )

    if people_match:
        result["people"]["total"] = people_match.group(1)

    # -------------------------
    # CHILDREN
    # -------------------------
    child_match = re.search(
        r'\b(\d+)\s+(?:children|kids|child|infants|babies)\b',
        lower
    )

    if child_match:
        result["people"]["children"] = child_match.group(1)
    elif re.search(r'\b(child|children|kid|kids|baby|babies|infant)\b', lower):
        result["people"]["children"] = "mentioned"

    # -------------------------
    # PREGNANT
    # -------------------------
    if re.search(r'\b(pregnant|pregnancy)\b', lower):
        result["people"]["pregnant"] = "mentioned"

    # -------------------------
    # ELDERLY
    # -------------------------
    if re.search(
        r'\b(elderly|grandmother|grandfather|grandma|grandpa|senior citizens?)\b',
        lower
    ):
        result["people"]["elderly"] = "mentioned"

    # -------------------------
    # INJURED
    # -------------------------
    injured_match = re.search(
        r'\b(\d+)\s+(?:injured|wounded|hurt)\b',
        lower
    )

    if injured_match:
        result["people"]["injured"] = injured_match.group(1)
    elif re.search(r'\b(injured|wounded|bleeding|hurt)\b', lower):
        result["people"]["injured"] = "mentioned"

    # -------------------------
    # MISSING
    # -------------------------
    missing_match = re.search(
        r'\b(\d+)\s+(?:missing|lost)\b',
        lower
    )

    if missing_match:
        result["people"]["missing"] = missing_match.group(1)
    elif re.search(r'\b(missing|lost person|cannot find)\b', lower):
        result["people"]["missing"] = "mentioned"

    # -------------------------
    # MOBILITY IMPAIRED
    # -------------------------
    if re.search(
        r'\b(cannot walk|can\'t walk|wheelchair|disabled|mobility impaired|'
        r'unable to walk|unable to move)\b',
        lower
    ):
        result["people"]["mobility_impaired"] = "mentioned"

    # -------------------------
    # NEEDS
    # -------------------------
    if re.search(r'\b(food|meal|meals|ration|hungry)\b', lower):
        result["needs"]["food"] = True
        result["request"]["resources"].append("FOOD")

    if re.search(r'\b(water|drinking water|clean water)\b', lower):
        result["needs"]["water"] = True
        result["request"]["resources"].append("WATER")

    if re.search(
        r'\b(medicine|medicines|medication|medical supplies|pharmacy)\b',
        lower
    ):
        result["needs"]["medicine"] = True
        result["request"]["resources"].append("MEDICINE")

    if re.search(r'\b(shelter|tent|temporary housing)\b', lower):
        result["needs"]["shelter"] = True
        result["request"]["resources"].append("SHELTER")

    if re.search(
        r'\b(rescue|trapped|stranded|stuck|boat|evacuate|evacuation)\b',
        lower
    ):
        result["needs"]["rescue"] = True

    # -------------------------
    # MEDICAL TRANSFER
    # -------------------------
    if re.search(
        r'\b(shifted to hospital|transfer to hospital|'
        r'take.*hospital|hospital transfer|airlift)\b',
        lower
    ):
        result["needs"]["medical_transfer"] = True

    # -------------------------
    # REQUEST TYPE
    # -------------------------
    if result["needs"]["medical_transfer"]:
        result["request"]["type"] = "MEDICAL"

    elif result["needs"]["rescue"]:
        result["request"]["type"] = "RESCUE"

    elif result["needs"]["food"]:
        result["request"]["type"] = "FOOD"

    elif result["needs"]["water"]:
        result["request"]["type"] = "WATER"

    elif result["needs"]["shelter"]:
        result["request"]["type"] = "SHELTER"

    # -------------------------
    # PHONE NUMBERS
    # -------------------------
    phones = re.findall(r'\b\d{10}\b', text)

    result["contact_info"] = phones

    # -------------------------
    # SITUATION
    # -------------------------
    situation_patterns = [
        r'[^.]*\btrapped\b[^.]*',
        r'[^.]*\bstranded\b[^.]*',
        r'[^.]*\bsurrounded by water\b[^.]*',
        r'[^.]*\bflood(?:ed|ing)?\b[^.]*'
    ]

    for pattern in situation_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result["situation"] = match.group(0).strip()
            break

    return result