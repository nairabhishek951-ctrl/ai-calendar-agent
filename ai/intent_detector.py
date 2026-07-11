def detect_intent(user_input):

    text = user_input.lower()

    SHOW_SCHEDULE = [
        "today",
        "today's schedule",
        "show schedule",
        "show my schedule",
        "calendar",
        "agenda",
        "what do i have",
        "what's on my calendar",
        "what is on my calendar",
        "what's on my schedule",
        "meetings today",
        "am i busy",
        "busy today",
        "today's agenda"
    ]

    CREATE_EVENT = [
        "create",
        "add",
        "schedule",
        "book",
        "meeting",
        "appointment",
        "call",
        "event",
        "remind me"
    ]

    DELETE_EVENT = [
        "delete",
        "remove",
        "cancel",
        "erase"
    ]

    UPDATE_EVENT = [
        "update",
        "change",
        "move",
        "reschedule"
    ]

    for phrase in SHOW_SCHEDULE:
        if phrase in text:
            return "SHOW_SCHEDULE"

    for phrase in DELETE_EVENT:
        if phrase in text:
            return "DELETE_EVENT"

    for phrase in UPDATE_EVENT:
        if phrase in text:
            return "UPDATE_EVENT"

    for phrase in CREATE_EVENT:
        if phrase in text:
            return "CREATE_EVENT"

    return "UNKNOWN"