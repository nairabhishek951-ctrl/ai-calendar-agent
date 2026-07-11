from datetime import datetime, timedelta

from ai.parser import parse_event


def create_event(service, user_input):
    print("\n========================================")
    print("        CREATE A CALENDAR EVENT")
    print("========================================\n")

    parsed = parse_event(user_input)

    title = parsed["title"]
    date = parsed["date"]
    time = f"{parsed['hour']:02d}:{parsed['minute']:02d}"
    duration = parsed["duration"]

    print("\nAI understood:")
    print(f"Title    : {title}")
    print(f"Date     : {date}")
    print(f"Time     : {time}")
    print(f"Duration : {duration} minutes")

    start_datetime = datetime.strptime(
        f"{date} {time}",
        "%Y-%m-%d %H:%M"
    )

    end_datetime = start_datetime + timedelta(minutes=duration)

    event = {
        "summary": title,
        "start": {
            "dateTime": start_datetime.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": end_datetime.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
    }

    created_event = service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    print("\nSUCCESS! Event created in Google Calendar.")
    print(f"Event: {created_event.get('summary')}")
    print(f"Start: {created_event['start'].get('dateTime')}")
