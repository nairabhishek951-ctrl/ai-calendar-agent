from datetime import datetime, timedelta

from ai.intent_detector import detect_intent
from commands.create_event import create_event
from commands.delete_event import delete_event
from commands.show_schedule import show_today_schedule

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


def main():
    print("\nConnecting to Google Calendar...")

    service = connect_to_calendar()

    print("SUCCESS! Connected to Google Calendar.")

    print("\n🤖 ASTRA")
    print("\nHow can I help you today?")

    while True:
        user_input = input("\n> ").strip()

        if user_input.lower() in {"exit", "quit", "bye"}:
            print("\n👋 Goodbye Abhishek!")
            print("Have a productive day.")
            break

        intent = detect_intent(user_input)

        if intent == "CREATE_EVENT":
            create_event(service, user_input)
        elif intent == "SHOW_SCHEDULE":
            show_today_schedule(service, user_input)
        elif intent == "DELETE_EVENT":
            delete_event(service, user_input)
        else:
            print("Sorry, I didn't understand that request.")

        print("\n────────────────────────────────────")
        print("\n🤖 Anything else?")