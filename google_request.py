import datetime
import os.path
from datetime import timedelta

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]
FILE_PATH = 'credentials.json'
creds = service_account.Credentials.from_service_account_file(
    filename=FILE_PATH, scopes=SCOPES
)
service = build('calendar', 'v3', credentials=creds)
load_dotenv()


async def get_free_slot():
    try:

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        end_date = (datetime.datetime.utcnow() + datetime.timedelta(days=30)).isoformat() + "Z"

        events_result = (
            service.events()
            .list(
                calendarId=os.getenv('CALENDAR_ID'),
                timeMin=now,
                timeMax=end_date,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return []

        # Get the dates of the next 30 days
        next_30_days = [datetime.datetime.utcnow().date() + datetime.timedelta(days=i) for i in range(30)]

        # Iterate through events and remove dates where events occupy the entire time from 10:00 to 22:00
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            start_datetime = datetime.datetime.fromisoformat(start.replace("Z", "+00:00"))
            end = event["end"].get("dateTime", event["end"].get("date"))
            end_datetime = datetime.datetime.fromisoformat(end.replace("Z", "+00:00"))
            if start_datetime.time() <= datetime.time(10) and end_datetime.time() >= datetime.time(22):
                event_date = start_datetime.date()
                if event_date in next_30_days:
                    next_30_days.remove(event_date)

        # Convert dates to string format 'YYYY-MM-DD'
        next_30_days_str = [date.strftime('%Y-%m-%d') for date in next_30_days]

        return next_30_days_str

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []


async def get_free_slots(date):
    # Определение начала и конца дня для выбранной даты
    start_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    start_time = datetime.datetime.combine(start_date, datetime.datetime.min.time()) + timedelta(hours=10)
    end_time = datetime.datetime.combine(start_date, datetime.datetime.min.time()) + timedelta(hours=22)

    # Получение событий из календаря для выбранной даты
    events_result = service.events().list(calendarId=os.getenv('CALENDAR_ID'), timeMin=start_time.isoformat() + 'Z',
                                          timeMax=end_time.isoformat() + 'Z', singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    # Создание списка свободных слотов
    free_slots = []
    current_time = start_time
    for event in events:
        event_start = datetime.datetime.fromisoformat(event['start']['dateTime'][:-6])
        event_end = datetime.datetime.fromisoformat(event['end']['dateTime'][:-6])
        if current_time < event_start:
            free_slots.append((current_time, event_start))
        current_time = event_end

    if current_time < end_time:
        free_slots.append((current_time, end_time))

    return free_slots


async def insert_new(date, time, name, hair_length_name, hair_density_name, text, first_time, hair_coloring,
                     phone_number, services, price):
    try:

        event_date = date

        time_1 = time.split(':')[0]
        time_2 = time.split(':')[1]

        if time_1[:1] == '0':
            time_1 = time_1[:2].lstrip('0')
            if not time_1 == '00':
                time_1 = time_1.lstrip('0')

        if time_2[:1] == '0':
            time_2 = time_2[:2]
            if not time_2 == '00':
                time_2 = time_2.lstrip('0')

        time_1 = int(time_1) - 3
        last_time_1 = int(time_1) + 1

        start_time = datetime.datetime(event_date.year, event_date.month, event_date.day, int(time_1), int(time_2))
        end_time = datetime.datetime(event_date.year, event_date.month, event_date.day, last_time_1, int(time_2))

        # Формируем тело события

        event_body = {
                "summary": f"{name}",
                "description": f"Услуга: <b>{services}</b>\n"
                               f"Длина: <b>{hair_length_name}</b>\n"
                               f"Густота: <b>{hair_density_name}</b>\n"
                               f"{text}\n"
                               f"Впервый ли раз: <b>{first_time}</b>\n"
                               f"Окрашивание волос: <b>{hair_coloring}</b>\n"
                               f"Номер телефона: <b>{phone_number}</b>\n\n"
                               f"Цена: <b>{price}",
                "start": {"dateTime": start_time.isoformat(), "timeZone": "UTC"},
                "end": {"dateTime": end_time.isoformat(), "timeZone": "UTC"}
            }

        # Создаем событие
        event = service.events().insert(
            calendarId=os.getenv('CALENDAR_ID'),
            body=event_body
        ).execute()

        print(f"Event created: {event['id']}")

    except HttpError as error:
        print(f"This error: {error}")


def func(calendar_id):
    calendar_list_entry = {
        'id': calendar_id
    }

    return service.calendarList().insert(
        body=calendar_list_entry).execute()

