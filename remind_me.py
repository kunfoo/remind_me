#!/usr/bin/env python3
import tomllib
import logging
import typer
from datetime import date, timedelta
from smtplib import SMTP


class Event:
    def __init__(self, title: str, raw_event: dict):
        self.today = date.today()
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
                age = self.today.year - self.date.year
                self.message = f"{self.message} ({age})"


    def __repr__(self):
        return f"{self.date}: {self.message}"


    def is_today(self):
        for reminder in self.reminders:
            if reminder.day == self.today.day and reminder.month == self.today.month:
                return True

        return False


def main(config: str, email: str):
    with open(config, "rb") as f:
        config = tomllib.load(f)

    todays_events = []
    for event_title in config:
        this_event = config[event_title]
        new_event = Event(event_title, this_event)
        if new_event.is_today():
            todays_events.append(new_event)

    email_from = "Reminder"
    email_hdr = "From: Reminder\r\nSubject:"

    with SMTP("localhost") as server:
        for event in todays_events:
            msg = f"{email_hdr} {event}"
            server.sendmail(email_from, email, msg)

    exit(0)


if __name__ == "__main__":
    typer.run(main)
