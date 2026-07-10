from datetime import datetime, timedelta
import re


def parse_event(user_input):
    """
    Parses simple event descriptions.

    Example:
    Team Meeting tomorrow at 3 PM for 60 minutes
    """

    text = user_input.lower()

    # ------------------------
    # DATE
    # ------------------------

    if "tomorrow" in text:
        event_date = datetime.now() + timedelta(days=1)
    elif "today" in text:
        event_date = datetime.now()
    else:
        match = re.search(r"\d{4}-\d{2}-\d{2}", text)

        if match:
            event_date = datetime.strptime(match.group(), "%Y-%m-%d")
        else:
            event_date = datetime.now()

    # ------------------------
    # TIME
    # ------------------------

    time_match = re.search(r"(\d{1,2})\s?(am|pm)", text)

    if time_match:
        hour = int(time_match.group(1))

        if time_match.group(2) == "pm" and hour != 12:
            hour += 12

        if time_match.group(2) == "am" and hour == 12:
            hour = 0

        minute = 0

    else:
        hour = 9
        minute = 0

    # ------------------------
    # DURATION
    # ------------------------

    duration_match = re.search(r"(\d+)\s?(minute|minutes|min)", text)

    if duration_match:
        duration = int(duration_match.group(1))
    else:
        duration = 60

    # ------------------------
    # TITLE
    # ------------------------

    title = user_input

    remove_words = [
        "tomorrow",
        "today",
        "at",
        "for"
    ]

    for word in remove_words:
        title = title.replace(word, "")

    title = re.sub(r"\d+\s?(am|pm)", "", title, flags=re.IGNORECASE)
    title = re.sub(r"\d+\s?(minutes|minute|min)", "", title, flags=re.IGNORECASE)

    title = " ".join(title.split())

    return {
        "title": title.title(),
        "date": event_date.strftime("%Y-%m-%d"),
        "hour": hour,
        "minute": minute,
        "duration": duration,
    }