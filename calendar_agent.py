from datetime import datetime, timedelta
from event_parser import parse_event

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def connect_to_calendar():
    credentials = Credentials.from_authorized_user_file(
        "token.json",
        SCOPES
    )

    service = build(
        "calendar",
        "v3",
        credentials=credentials
    )

    return service


def create_event(service):
    print("\n========================================")
    print("        CREATE A CALENDAR EVENT")
    print("========================================\n")

    user_input = input("Describe your event: ")

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


def main():
    print("\nConnecting to Google Calendar...")

    service = connect_to_calendar()

    print("SUCCESS! Connected to Google Calendar.")

    create_event(service)


if __name__ == "__main__":
    main()