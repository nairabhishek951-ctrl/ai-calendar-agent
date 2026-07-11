from datetime import datetime, timedelta


def show_today_schedule(service, user_input):
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
