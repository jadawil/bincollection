from icalendar import Calendar, Event
from datetime import date
from urllib import request

BIN_FEED_URL = 'https://s3-eu-west-1.amazonaws.com/fs-downloads/GM/binfeed.ical'

UID_KEY = 'uid'
DTSTAMP_KEY = 'dtstamp'
DTSTART_KEY = 'dtstart'
SUMMARY_KEY = 'summary'

def find_next_collections(from_date, calendar):
    """Find the first collections on or after the given date.

    Keyword arguments:
    from_date -- the date to find collections on or after
    calendar -- the calendar to find collections in.
    """

    collections = []
    next_date = None
    for event in calendar.walk():
        dtstart = event.get(DTSTART_KEY)
        if dtstart and dtstart.dt >= from_date:
            if not next_date or dtstart.dt < next_date:
                next_date = dtstart.dt
                collections = []
            if dtstart.dt == next_date:
                collections.append(event)
    return collections

if __name__ == '__main__':
    bin_data = request.urlopen(BIN_FEED_URL).read()
    bin_calendar = Calendar.from_ical(bin_data)

    while True:
        read = input("Enter a date to find the next collection (YYYY-MM-DD):")
        parsed_date = None

        try:
            parsed_date = date.fromisoformat(read)
        except ValueError:
            print("Invalid date format.")
            continue

        collections = find_next_collections(parsed_date, bin_calendar)
        for collection in collections:
            print(f'Date: {collection.get(DTSTART_KEY).dt}, Bin: {collection.get(SUMMARY_KEY)}')

