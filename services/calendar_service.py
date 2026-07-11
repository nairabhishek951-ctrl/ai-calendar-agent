from datetime import datetime, timedelta

from ai.parser import parse_event
from ai.intent_detector import detect_intent
from commands.delete_event import delete_event

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


def show_today_schedule(service):
    print()
    print("══════════════════════════════════")
    print("📅 Today's Schedule")
    print("══════════════════════════════════")
    print()

    now = datetime.now()

    start = datetime(now.year, now.month, now.day)
    end = start + timedelta(days=1)

    events_result = service.events().list(
        calendarId="primary",
        timeMin=start.isoformat() + "Z",
        timeMax=end.isoformat() + "Z",
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    if not events:
        print("No events scheduled today.")
        return

    count = 0

    for event in events:
        start_time = event["start"].get(
            "dateTime",
            event["start"].get("date")
        )

        start_datetime = datetime.fromisoformat(
            start_time.replace("Z", "+00:00")
        )

        formatted_time = start_datetime.strftime("%I:%M %p")

        print(f"⏰ {formatted_time}")
        print(f"   {event['summary']}")
        print()

        count += 1

    print("──────────────────────────────────")
    print(f"Total Events: {count}")


def main():
    print("\nConnecting to Google Calendar...")

    service = connect_to_calendar()

    print("SUCCESS! Connected to Google Calendar.")

    print("\n🤖 ASTRA")
    print("\nHow can I help you today?")

    user_input = input("\n> ")

    intent = detect_intent(user_input)

    if intent == "CREATE_EVENT":
        create_event(service)
    elif intent == "SHOW_SCHEDULE":
        show_today_schedule(service)
    elif intent == "DELETE_EVENT":
        delete_event(service, user_input)
    else:
        print("Sorry, I didn't understand that request.")