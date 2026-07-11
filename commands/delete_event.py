from datetime import datetime, timedelta


ACTION_WORDS = {"delete", "remove", "cancel"}
FILLER_WORDS = {"my", "the", "a", "an", "event"}


def _clean_search_query(user_input):
    words = [
        word for word in user_input.split()
        if word.lower() not in ACTION_WORDS and word.lower() not in FILLER_WORDS
    ]
    return " ".join(words).strip()


def _get_upcoming_events(service):
    now = datetime.now()

    start = datetime(now.year, now.month, now.day)
    end = start + timedelta(days=30)

    events_result = service.events().list(
        calendarId="primary",
        timeMin=start.isoformat() + "Z",
        timeMax=end.isoformat() + "Z",
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    return events_result.get("items", [])


def delete_event(service, user_input):
    search_query = _clean_search_query(user_input)

    if not search_query:
        print("No matching event found.")
        return

    events = _get_upcoming_events(service)
    matching_events = []

    for event in events:
        summary = event.get("summary", "")
        if search_query.lower() in summary.lower():
            matching_events.append(event)

    if not matching_events:
        print("No matching event found.")
        return

    if len(matching_events) == 1:
        event = matching_events[0]
        event_id = event.get("id")

        if event_id:
            service.events().delete(
                calendarId="primary",
                eventId=event_id
            ).execute()

            print(f"Deleted event: {event.get('summary', 'Untitled event')}")
        else:
            print("No matching event found.")
        return

    print("Multiple matching events found:")

    for index, event in enumerate(matching_events, start=1):
        summary = event.get("summary", "Untitled event")
        print(f"{index}. {summary}")

    selection = input("Which event would you like to delete? ")

    try:
        choice = int(selection) - 1
    except ValueError:
        print("Invalid selection.")
        return

    if 0 <= choice < len(matching_events):
        event = matching_events[choice]
        event_id = event.get("id")

        if event_id:
            service.events().delete(
                calendarId="primary",
                eventId=event_id
            ).execute()
            print(f"Deleted event: {event.get('summary', 'Untitled event')}")
        else:
            print("No matching event found.")
    else:
        print("Invalid selection.")
