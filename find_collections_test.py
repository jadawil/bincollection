import unittest
from icalendar import Calendar, Event
from datetime import date
from find_collections import DTSTART_KEY, SUMMARY_KEY, find_next_collections

class TestFindCollections(unittest.TestCase):
    
    def test_find_next_collections(self):
        cal = Calendar()
        
        third_event = Event()
        third_from_date = date(2018, 10, 10)
        third_summary = 'Third Collection'
        third_event.add(DTSTART_KEY, third_from_date)
        third_event.add(SUMMARY_KEY, third_summary)

        second_event = Event()
        second_from_date = date(2018, 10, 10)
        second_summary = 'Second Collection'
        second_event.add(DTSTART_KEY, second_from_date)
        second_event.add(SUMMARY_KEY, second_summary)
        cal.add_component(second_event)

        first_event = Event()
        first_from_date = date(2018, 2, 7)
        first_summary = 'First Collection'
        first_event.add(DTSTART_KEY, first_from_date)
        first_event.add(SUMMARY_KEY, first_summary)
        cal.add_component(first_event)

        collections = find_next_collections(date(2018, 10, 11), cal)
        self.assertEqual(len(collections), 0)
        collections = find_next_collections(date(2018, 8, 10), cal)
        self.assertEqual(len(collections), 1)
        self.assertEqual(collections[0].get(DTSTART_KEY).dt, second_from_date)
        self.assertEqual(collections[0].get(SUMMARY_KEY), second_summary)
        collections = find_next_collections(first_from_date, cal)
        self.assertEqual(len(collections), 1)
        self.assertEqual(collections[0].get(DTSTART_KEY).dt, first_from_date)
        self.assertEqual(collections[0].get(SUMMARY_KEY), first_summary)

        cal.add_component(third_event)

        collections = find_next_collections(third_from_date, cal)
        self.assertTrue(len(collections) == 2)


if __name__ == '__main__':
    unittest.main()
