import argparse
import json
from datetime import datetime

import pendulum
import requests

from .config import (FOREST_CLAENDAR_URL, FOREST_LOGIN_URL, FOREST_TAG_URL,
                     FOREST_URL_HEAD)


class Forst:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.s = requests.Session()
        self.year = datetime.now().year
        self.user_id = None
        self.plants = []
        self.log_days = []
        self.success_plants_count = 0
        self.is_login = False

    def login(self):
        data = {"session": {"email": self.email, "password": self.password}}
        headers = {"Content-Type": "application/json"}
        r = self.s.post(FOREST_LOGIN_URL, headers=headers, data=json.dumps(data))
        if not r.ok:
            raise Exception(f"Someting is wrong to login -- {r.text}")
        self.user_id = r.json()["user_id"]
        self.is_login = True

    def make_plants_data(self):
        date = str(self.year) + "-01-01"
        r = self.s.get(FOREST_CLAENDAR_URL.format(date=date, user_id=self.user_id))
        if not r.ok:
            raise LoadError(f"Someting is wrong to get data-- {r.text}")
        self.plants = r.json()["plants"]
        # only count success trees
        self.plants = [i for i in self.plants if i["is_success"]]

    def _get_my_tags(self):
        r = self.s.get(FOREST_TAG_URL.format(user_id=self.user_id))
        if not r.ok:
            raise Exception("Can not get tags")
        return r.json().get("tags", [])

    def make_year_stats(self):
        if not self.is_login:
            raise Exception("Please login first")
        self.make_plants_data()

    def _get_forst_steak(self):
        pass

    def make_forst_daily(self):
        end_date = pendulum.now("Asia/Shanghai")
        start_date = end_date.start_of("year")
        self.make_year_stats()
        log_days = set(
            [
                pendulum.parse(i["created_at"], tz="Asia/Shanghai").to_date_string()
                for i in self.plants
            ]
        )
        self.log_days = sorted(list(log_days))
        total_plants = len(self.plants)
        is_today_check = False
        if end_date.to_date_string() in self.log_days:
            is_today_check = True
        periods = list(pendulum.period(start_date, end_date.subtract(days=1)))
        periods.sort(reverse=True)

        # if today id done
        streak = 0
        if end_date.to_date_string() in self.log_days:
            streak += 1

        # for else if not break not else
        for p in periods:
            if p.to_date_string() not in self.log_days:
                break
            streak += 1
        # total plants, streak, is_today_check
        return len(self.plants), streak, is_today_check


def get_forst_daily(email, password):
    f = Forst(email, password)
    f.login()
    return f.make_forst_daily()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("email", help="email")
    parser.add_argument("password", help="password")
    options = parser.parse_args()
    f = Forst(options.email, options.password)
    f.login()
    print(f.make_forst_daily())
