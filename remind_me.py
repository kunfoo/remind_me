#!/usr/bin/env python3
import tomli
import logging
from datetime import date, timedelta

CONFIG = "remind_me.toml"
TODAY = date.today()

class Event:
    def __init__(self, title: str, raw_event: dict):
        self.date = raw_event["date"]
        self.message = raw_event.get("message", title)
        self.is_birthday = raw_event.get("birthday", False)
        self.age_unknown = raw_event.get("age_unknown", False)
        self.remind_before = raw_event.get("remind_before", [])

        self.reminders = [self.date]
        for r in self.remind_before:
            reminder = self.date - timedelta(days=r)
            self.reminders.append(reminder)

        if self.is_birthday:
            if not self.age_unknown:
                age = TODAY.year - self.date.year
                self.message = f"{self.message} ({age})"


    def __repr__(self):
        return f"{self.date}: {self.message}"


    def is_today(self):
        for reminder in self.reminders:
            if reminder.day == TODAY.day and reminder.month == TODAY.month:
                return True

        return False


def main():
    with open(CONFIG, "rb") as f:
        config = tomli.load(f)

    todays_events = []
    all_events = config["event"]
    for event_title in all_events:
        this_event = all_events[event_title]
        new_event = Event(event_title, this_event)
        if new_event.is_today():
            todays_events.append(new_event)

    print(todays_events)

    exit(0)

if __name__ == "__main__":
    main()
