import re


# ============================================================
# HELPER FUNCTIONS
# ============================================================

NUMBER_WORDS = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "ten": "10",
    "eleven": "11",
    "twelve": "12",
    "thirteen": "13",
    "fourteen": "14",
    "fifteen": "15",
    "sixteen": "16",
    "seventeen": "17",
    "eighteen": "18",
    "nineteen": "19",
    "twenty": "20"
}


def word_to_number(value):
    value = value.lower().strip()
    return NUMBER_WORDS.get(value, value)


def normalize_count(value):
    """Normalize counts such as 10,000 / 500,000 / 20,000+."""
    if value is None:
        return None
    return value.strip().replace(",", "").rstrip("+")


def clean_location_candidate(candidate):
    if not candidate:
        return None

    # Remove GPS coordinates and phone numbers.
    candidate = re.sub(
        r"\b-?\d{1,3}\.\d+\s*[,;/]\s*-?\d{1,3}\.\d+\b",
        "",
        candidate
    )
    candidate = re.sub(r"\b\d{10}\b", "", candidate)
    candidate = re.sub(r"\+?91[\s-]?\d{5}[\s-]?\d{5}\b", "", candidate)
    candidate = re.sub(r"#\w+", "", candidate)

    # Stop at words that clearly start a non-location part.
    candidate = re.split(
        r"\b(?:need|needs|please|urgent|help|send|contact|call|"
        r"phone|number|request|requests|asking|says|said|message|"
        r"tweet|tweets|now|immediately|there|here)\b",
        candidate,
        maxsplit=1,
        flags=re.IGNORECASE
    )[0]

    candidate = clean_text(candidate)

    if not candidate:
        return None

    # Reject obvious sentence fragments.
    if re.search(
        r"\b(?:has sent|sent this message|posted this|need help|needs help)\b",
        candidate,
        flags=re.IGNORECASE
    ):
        return None

    if re.fullmatch(
        r"(?:the )?(?:location|place|area|address|site|spot)",
        candidate,
        flags=re.IGNORECASE
    ):
        return None

    return candidate


def clean_text(value):
    if not value:
        return None

    value = re.sub(r"\s+", " ", value)
    value = value.strip(" \t\r\n.,;:-")

    return value if value else None


def add_resource(result, resource):
    if resource not in result["request"]["resources"]:
        result["request"]["resources"].append(resource)


# ============================================================
# MAIN EXTRACTOR
# ============================================================

def extract_sos_v2(message: str):

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
            "deceased": None,
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

    # ========================================================
    # 1. TOTAL PEOPLE
    # ========================================================

    # --------------------------------------------------------
    # "20-30 people"
    # "20 to 30 people"
    # "14-20ppl"
    # --------------------------------------------------------

    match = re.search(
        r"\b(\d{1,3}(?:,\d{3})+|\d+)\s*(?:-|to)\s*(\d{1,3}(?:,\d{3})+|\d+)\s*"
        r"(?:people|peoples|persons|individuals|members|adults|ppl)\b",
        lower
    )

    if match:
        result["people"]["total"] = (
            f"{normalize_count(match.group(1))}-{normalize_count(match.group(2))}"
        )

    # --------------------------------------------------------
    # "20ppl"
    # "50 people"
    # "4000 peoples"
    # --------------------------------------------------------

    if result["people"]["total"] is None:

        match = re.search(
            r"\b(\d{1,3}(?:,\d{3})+|\d+)\s*"
            r"(?:people|peoples|persons|individuals|members|adults|ppl)\b",
            lower
        )

        if match:
            result["people"]["total"] = normalize_count(match.group(1))

    # --------------------------------------------------------
    # "50 stranded people"
    # "4000 trapped people"
    # --------------------------------------------------------

    if result["people"]["total"] is None:

        match = re.search(
            r"\b(\d+)\s+"
            r"(?:stranded|trapped|stuck|marooned)\s+"
            r"(?:people|peoples|persons|individuals|ppl)\b",
            lower
        )

        if match:
            result["people"]["total"] = normalize_count(match.group(1))

    # --------------------------------------------------------
    # "20 people trapped"
    # --------------------------------------------------------

    if result["people"]["total"] is None:

        match = re.search(
            r"\b(\d+)\s+"
            r"(?:people|peoples|persons|individuals|ppl)\b",
            lower
        )

        if match:
            result["people"]["total"] = match.group(1)

    # --------------------------------------------------------
    # "family of five"
    # "family of 5"
    # --------------------------------------------------------

    if result["people"]["total"] is None:

        match = re.search(
            r"\b(?:family|families)\s+of\s+"
            r"(one|two|three|four|five|six|seven|eight|nine|ten|\d+)\b",
            lower
        )

        if match:
            result["people"]["total"] = word_to_number(
                match.group(1)
            )

    # --------------------------------------------------------
    # "group of 10"
    # --------------------------------------------------------

    if result["people"]["total"] is None:

        match = re.search(
            r"\bgroup\s+of\s+"
            r"(one|two|three|four|five|six|seven|eight|nine|ten|\d+)\b",
            lower
        )

        if match:
            result["people"]["total"] = word_to_number(
                match.group(1)
            )

    # ========================================================
    # 2. CHILDREN
    # ========================================================

    # --------------------------------------------------------
    # "29 children"
    # "5 kids"
    # "2 small children"
    # "3 young kids"
    # "4 little kids"
    # --------------------------------------------------------

    match = re.search(
        r"\b(\d+)\s+"
        r"(?:(?:small|young|little|minor)\s+)?"
        r"(?:children|kids|infants|babies)\b",
        lower
    )

    if match:
        result["people"]["children"] = match.group(1)

    # --------------------------------------------------------
    # "two children"
    # "three kids"
    # --------------------------------------------------------

    if result["people"]["children"] is None:

        match = re.search(
            r"\b(one|two|three|four|five|six|seven|eight|nine|ten)\s+"
            r"(?:(?:small|young|little|minor)\s+)?"
            r"(?:children|kids|infants|babies)\b",
            lower
        )

        if match:
            result["people"]["children"] = word_to_number(
                match.group(1)
            )

    # --------------------------------------------------------
    # "a child"
    # "one kid"
    # "a baby"
    # --------------------------------------------------------

    if result["people"]["children"] is None:

        if re.search(
            r"\b(?:a|an|one)\s+"
            r"(?:small|young|little)?\s*"
            r"(?:child|kid|baby|infant)\b",
            lower
        ):
            result["people"]["children"] = "1"

    # --------------------------------------------------------
    # "4 years old kid"
    # "4 year old child"
    # "4yr old kid"
    #
    # IMPORTANT:
    # 4 = age, NOT 4 children.
    # Therefore output = 1 child.
    # --------------------------------------------------------

    if result["people"]["children"] is None:

        if re.search(
            r"\b\d+\s*(?:year|years|yr|yrs)"
            r"\s*(?:old)?\s*"
            r"(?:child|kid|baby|infant)\b",
            lower
        ):
            result["people"]["children"] = "1"

    # "Most of them are children" means children are present,
    # but the message does not provide an exact count.
    if result["people"]["children"] is None:
        if re.search(
            r"\bmost of (?:them|the people) (?:are|is) children\b",
            lower
        ):
            result["people"]["children"] = "mentioned"

    # ========================================================
    # 3. ELDERLY
    # ========================================================

    # "2 elderly people"
    # "3 senior citizens"

    match = re.search(
        r"\b(\d+)\s+"
        r"(?:elderly|old people|senior citizens?)\b",
        lower
    )

    if match:
        result["people"]["elderly"] = match.group(1)

    # "two elderly people"

    if result["people"]["elderly"] is None:

        match = re.search(
            r"\b(one|two|three|four|five)\s+"
            r"(?:elderly|old people|senior citizens?)\b",
            lower
        )

        if match:
            result["people"]["elderly"] = word_to_number(
                match.group(1)
            )

    # Explicit elderly words

    if result["people"]["elderly"] is None:

        if re.search(
            r"\b("
            r"grandmother|grandfather|grandma|grandpa|"
            r"elderly|senior citizen|"
            r"old patient lady|old patient man"
            r")\b",
            lower
        ):
            result["people"]["elderly"] = "1"

    # "60 year old aunty"
    # "80 year old woman"
    # "70 yr old man"

    if result["people"]["elderly"] is None:

        if re.search(
            r"\b\d+\s*(?:year|years|yr|yrs)"
            r"\s*(?:old)?\s*"
            r"(?:aunty|aunt|uncle|man|woman|lady|person)\b",
            lower
        ):
            result["people"]["elderly"] = "1"

    # ========================================================
    # 4. PREGNANT
    # ========================================================

    # "2 pregnant women"

    match = re.search(
        r"\b(\d+)\s+"
        r"(?:pregnant women|pregnant woman|pregnant ladies|pregnant lady)\b",
        lower
    )

    if match:
        result["people"]["pregnant"] = match.group(1)

    # "two pregnant women"

    if result["people"]["pregnant"] is None:

        match = re.search(
            r"\b(one|two|three|four|five)\s+"
            r"(?:pregnant women|pregnant woman|pregnant ladies|pregnant lady)\b",
            lower
        )

        if match:
            result["people"]["pregnant"] = word_to_number(
                match.group(1)
            )

    # "pregnant woman"

    if result["people"]["pregnant"] is None:

        if re.search(
            r"\b(pregnant woman|pregnant lady|pregnant person)\b",
            lower
        ):
            result["people"]["pregnant"] = "1"

    # ========================================================
    # 5. INJURED
    # ========================================================

    match = re.search(
        r"\b(\d+)\s+"
        r"(?:people|persons|children|kids)?\s*"
        r"(?:are\s+)?"
        r"(?:injured|wounded|hurt)\b",
        lower
    )

    if match:
        result["people"]["injured"] = match.group(1)

    elif re.search(
        r"\b(injured|wounded|bleeding|badly hurt)\b",
        lower
    ):
        result["people"]["injured"] = "1"

    # ========================================================
    # 6. MISSING
    # ========================================================

    match = re.search(
        r"\b(\d+)\s+"
        r"(?:people|persons|children|kids|persons)?\s*"
        r"(?:are\s+)?missing\b",
        lower
    )

    if match:
        result["people"]["missing"] = match.group(1)

    else:

        match = re.search(
            r"\b(one|two|three|four|five)\s+"
            r"(?:people|persons|children|kids)?\s*"
            r"(?:are\s+)?missing\b",
            lower
        )

        if match:
            result["people"]["missing"] = word_to_number(
                match.group(1)
            )

    if result["people"]["missing"] is None:

        if re.search(
            r"\b("
            r"missing person|missing people|"
            r"cannot find|can't find|"
            r"not found"
            r")\b",
            lower
        ):
            result["people"]["missing"] = "1"

    # ========================================================
    # 7. DECEASED
    # ========================================================

    match = re.search(
        r"\b(\d+)\s+"
        r"(?:people|persons|children|kids)?\s*"
        r"(?:died|dead|deceased|killed|passed away)\b",
        lower
    )

    if match:
        result["people"]["deceased"] = match.group(1)

    else:

        match = re.search(
            r"\b(one|two|three|four|five)\s+"
            r"(?:people|persons|children|kids)?\s*"
            r"(?:died|dead|deceased|killed|passed away)\b",
            lower
        )

        if match:
            result["people"]["deceased"] = word_to_number(
                match.group(1)
            )

    if result["people"]["deceased"] is None:

        # Only explicit past/current death statements.
        # Do NOT count predictions such as "will lose their life".
        if re.search(
            r"\b(?:"
            r"passed away|"
            r"has died|have died|"
            r"died|are dead|is dead|was dead|were dead|"
            r"deceased|were killed|was killed|"
            r"killed in the (?:flood|disaster|accident)|"
            r"death toll"
            r")\b",
            lower
        ):
            result["people"]["deceased"] = "1"

    # ========================================================
    # 8. MOBILITY IMPAIRED
    # ========================================================

    if re.search(
        r"\b("
        r"cannot walk|can't walk|unable to walk|"
        r"unable to move|wheelchair|disabled|"
        r"mobility impaired|paralyzed|paralysed|"
        r"bedridden"
        r")\b",
        lower
    ):
        result["people"]["mobility_impaired"] = "1"

    # ========================================================
    # 9. GPS COORDINATES
    # ========================================================

    # --------------------------------------------------------
    # Format:
    # 9.356785,76.576964
    # 9.356785, 76.576964
    # --------------------------------------------------------

    gps = re.search(
        r"\b(-?\d{1,3}\.\d+)\s*[,;/]\s*"
        r"(-?\d{1,3}\.\d+)\b",
        text
    )

    if gps:

        lat = float(gps.group(1))
        lon = float(gps.group(2))

        if -90 <= lat <= 90 and -180 <= lon <= 180:

            result["location"]["latitude"] = lat
            result["location"]["longitude"] = lon

    # --------------------------------------------------------
    # Format:
    # 10.1797°N 76.2097°E
    # --------------------------------------------------------

    if result["location"]["latitude"] is None:

        gps = re.search(
            r"(-?\d+(?:\.\d+)?)\s*°?\s*([NS])"
            r"[\s,;/]+"
            r"(-?\d+(?:\.\d+)?)\s*°?\s*([EW])",
            text,
            re.IGNORECASE
        )

        if gps:

            lat = float(gps.group(1))
            lon = float(gps.group(3))

            if gps.group(2).upper() == "S":
                lat = -lat

            if gps.group(4).upper() == "W":
                lon = -lon

            if -90 <= lat <= 90 and -180 <= lon <= 180:

                result["location"]["latitude"] = lat
                result["location"]["longitude"] = lon

    # ========================================================
    # 10. LOCATION TEXT
    # ========================================================

    location_candidates = []

    # If GPS is present, look for a nearby geographic phrase.
    gps_patterns = [
        r"(?P<loc>[A-Z][A-Za-z0-9'./-]*(?:\s+[A-Z][A-Za-z0-9'./-]*){0,5}),?\s*"
        r"(?:Google\s+map\s+coordinates?|coordinates?|GPS)\b",
        r"(?:coordinates?|GPS)\s*(?:for|at|of)?\s*"
        r"(?P<loc>[A-Z][A-Za-z0-9'./-]*(?:\s+[A-Z][A-Za-z0-9'./-]*){0,5})"
    ]

    for pattern in gps_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            candidate = clean_location_candidate(match.group("loc"))
            if candidate:
                location_candidates.append(candidate)

    # Explicit labels.
    explicit_patterns = [
        r"(?:location|place|address|locality)\s*[:\-]\s*(?P<loc>[^#\n]+)",
        r"(?:stranded|stuck|trapped|marooned)\s+(?:at|in|near)\s+(?P<loc>[^.,#\n]+)",
        r"\bat\s+(?P<loc>[A-Z][A-Za-z0-9'./-]*(?:\s+[A-Z][A-Za-z0-9'./-]*){0,5})(?=\.|,|;|$)",
        r"\bin\s+(?P<loc>[A-Z][A-Za-z0-9'./-]*(?:\s+[A-Z][A-Za-z0-9'./-]*){0,5})(?=\.|,|;|$)"
    ]

    for pattern in explicit_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            candidate = clean_location_candidate(match.group("loc"))
            if candidate:
                location_candidates.append(candidate)

    # Prefer candidates that look geographic, but allow short proper names.
    filtered = []
    for candidate in location_candidates:
        if re.search(
            r"\b(road|street|rd|st|nagar|town|city|village|district|"
            r"kerala|india|church|school|hospital|municipality|camp|"
            r"junction|colony|lane|beach|paravoor|chengannur|"
            r"edathwa|thiruvalla)\b",
            candidate,
            flags=re.IGNORECASE
        ):
            filtered.append(candidate)
        elif len(candidate.split()) <= 4:
            filtered.append(candidate)

    if filtered:
        result["location"]["text"] = filtered[0]

    # ========================================================
    # 11. FOOD
    # ========================================================

    if re.search(
        r"\b("
        r"food|foods|meal|meals|ration|rations|"
        r"hungry|starving|"
        r"packed food|food packets|food items|"
        r"food packet"
        r")\b",
        lower
    ):

        result["needs"]["food"] = True
        add_resource(result, "FOOD")

    # ========================================================
    # 12. WATER
    # ========================================================

    if re.search(
        r"\b("
        r"water|"
        r"drinking water|"
        r"clean water|"
        r"water bottles?|"
        r"potable water"
        r")\b",
        lower
    ):

        result["needs"]["water"] = True
        add_resource(result, "WATER")

    # ========================================================
    # 13. MEDICINE
    # ========================================================

    if re.search(
        r"\b("
        r"medicine|medicines|medication|"
        r"medical supplies?|medical kit|"
        r"first aid|pharmacy|"
        r"pediatric medicines?|"
        r"tablets?|injections?"
        r")\b",
        lower
    ):

        result["needs"]["medicine"] = True
        add_resource(result, "MEDICINE")

    # ========================================================
    # 14. OXYGEN
    # ========================================================

    if re.search(
        r"\boxygen\b",
        lower
    ):

        result["needs"]["medicine"] = True
        add_resource(result, "OXYGEN")

    # ========================================================
    # 15. AMBULANCE
    # ========================================================

    if re.search(
        r"\bambulance\b",
        lower
    ):

        result["needs"]["medical_transfer"] = True
        add_resource(result, "AMBULANCE")

    # ========================================================
    # 16. SHELTER
    # ========================================================

    if re.search(
        r"\b("
        r"shelter|tent|temporary housing|"
        r"relief camp|camp|"
        r"accommodation"
        r")\b",
        lower
    ):

        result["needs"]["shelter"] = True
        add_resource(result, "SHELTER")

    # ========================================================
    # 17. RESCUE
    # ========================================================

    if re.search(
        r"\b("
        r"rescue|trapped|stranded|stuck|"
        r"marooned|boat|"
        r"evacuate|evacuation|"
        r"airlift|helicopter|"
        r"save us|help us"
        r")\b",
        lower
    ):

        result["needs"]["rescue"] = True

    # ========================================================
    # 18. MEDICAL TRANSFER
    # ========================================================

    # Strong direct indicators

    if re.search(
        r"\b("
        r"shifted|transfer|transferred|"
        r"take|taken|move|moved|"
        r"transport|transported|"
        r"airlift"
        r")\b"
        r".{0,120}"
        r"\b("
        r"hospital|medical|clinic|"
        r"health centre|health center"
        r")\b",
        lower
    ):

        result["needs"]["medical_transfer"] = True

    # Direct hospital request

    if re.search(
        r"\b("
        r"need.*hospital|"
        r"hospital.*needed|"
        r"hospital.*urgent|"
        r"urgent.*hospital|"
        r"medical emergency"
        r")\b",
        lower
    ):

        result["needs"]["medical_transfer"] = True

    # ========================================================
    # 19. REQUEST TYPE
    # ========================================================

    if result["needs"]["medical_transfer"]:

        result["request"]["type"] = "MEDICAL"

    elif result["needs"]["rescue"]:

        result["request"]["type"] = "RESCUE"

    elif result["needs"]["medicine"]:

        result["request"]["type"] = "MEDICAL"

    elif result["needs"]["food"]:

        result["request"]["type"] = "FOOD"

    elif result["needs"]["water"]:

        result["request"]["type"] = "WATER"

    elif result["needs"]["shelter"]:

        result["request"]["type"] = "SHELTER"

    # ========================================================
    # 20. PHONE NUMBERS
    # ========================================================

    phone_patterns = [

        # +91 98765 43210
        r"\+91[\s\-]?\d{5}[\s\-]?\d{5}",

        # 91 98765 43210
        r"\b91[\s\-]\d{5}[\s\-]\d{5}\b",

        # 98765-43210
        r"\b\d{5}[\s\-]\d{5}\b",

        # 9876543210
        r"\b\d{10}\b"
    ]

    phones = []

    for pattern in phone_patterns:

        matches = re.findall(
            pattern,
            text
        )

        for phone in matches:

            normalized = re.sub(
                r"\D",
                "",
                phone
            )

            # Remove country code
            if (
                normalized.startswith("91")
                and len(normalized) == 12
            ):
                normalized = normalized[2:]

            if len(normalized) == 10:

                if normalized not in phones:
                    phones.append(normalized)

    result["contact_info"] = phones

    # ========================================================
    # 21. SOURCE TYPE
    # ========================================================

    if re.search(
        r"\b("
        r"relief camp|camp|"
        r"collection centre|collection center|"
        r"relief centre|relief center"
        r")\b",
        lower
    ):

        result["source_type"] = "RELIEF_REQUEST"

    elif (
        result["needs"]["medical_transfer"]
        or result["needs"]["medicine"]
        or re.search(
            r"\b(?:oxygen|ambulance|medical emergency)\b",
            lower
        )
    ):

        result["source_type"] = "MEDICAL_SOS"

    elif result["people"]["total"]:

        total = result["people"]["total"]

        # If range or >1 → group
        if "-" in str(total):
            result["source_type"] = "GROUP_SOS"

        else:

            try:

                if int(total) > 1:
                    result["source_type"] = "GROUP_SOS"

            except ValueError:
                result["source_type"] = "GROUP_SOS"

    # ========================================================
    # 22. SITUATION
    # ========================================================

    situation_patterns = [

        # trapped
        r"[^.?!]*\btrapped\b[^.?!]*",

        # stranded
        r"[^.?!]*\bstranded\b[^.?!]*",

        # stuck
        r"[^.?!]*\bstuck\b[^.?!]*",

        # surrounded by water
        r"[^.?!]*\bsurrounded by water\b[^.?!]*",

        # water level
        r"[^.?!]*\bwater level\b[^.?!]*",

        # flooded / flooding
        r"[^.?!]*\bflood(?:ed|ing)?\b[^.?!]*",

        # emergency
        r"[^.?!]*\bemergency\b[^.?!]*"
    ]

    for pattern in situation_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            situation = match.group(0).strip()

            # Remove hashtags
            situation = re.sub(
                r"#\w+",
                "",
                situation
            )

            # Remove phone numbers
            situation = re.sub(
                r"\b\d{10}\b",
                "",
                situation
            )

            # Remove GPS coordinates
            situation = re.sub(
                r"\b-?\d{1,3}\.\d+\s*[,;/]\s*"
                r"-?\d{1,3}\.\d+\b",
                "",
                situation
            )

            # Remove excessive whitespace
            situation = re.sub(
                r"\s+",
                " ",
                situation
            ).strip()

            if len(situation) <= 300:
                result["situation"] = situation
                break

    return result