import argparse
import json
from collections import Counter
from datetime import datetime

import pendulum
import requests
from github import Github

from .config import (
    FOREST_CLAENDAR_URL,
    FOREST_ISSUE_NUMBER,
    FOREST_LOGIN_URL,
    FOREST_SUMMARY_HEAD,
    FOREST_SUMMARY_STAT_TEMPLATE,
    FOREST_TAG_URL,
    FOREST_URL_HEAD,
)


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
        self._make_forest_dict()

    def _get_my_tags(self):
        r = self.s.get(FOREST_TAG_URL.format(user_id=self.user_id))
        if not r.ok:
            raise Exception("Can not get tags")
        tag_list = r.json().get("tags", [])
        tag_dict = {}
        for t in tag_list:
            tag_dict[t["tag_id"]] = t["title"]
        return tag_dict

    def make_year_stats(self):
        if not self.is_login:
            raise Exception("Please login first")
        self.make_plants_data()

    def _make_forest_dict(self):
        if not self.plants:
            self.make_plants_data()
        tags_dict = self._get_my_tags()
        d = Counter()
        for p in self.plants:
            d[tags_dict[p.get("tag")]] += 1
        return d

    @staticmethod
    def _make_tag_summary_str(tag_summary_dict, unit):
        s = FOREST_SUMMARY_HEAD
        for k, v in tag_summary_dict.most_common():
            s += FOREST_SUMMARY_STAT_TEMPLATE.format(tag=k, times=str(v) + f" {unit}")
        return s

    def make_new_table(self, token, repo_name, issue_number=FOREST_ISSUE_NUMBER):
        u = Github(token)
        issue = u.get_repo(repo_name).get_issue(FOREST_ISSUE_NUMBER)
        unit = "个"
        body = ""
        tag_summary_dict = self._make_forest_dict()
        for b in issue.body.splitlines():
            if b.startswith("|"):
                break
            body += b
        body = body + "\r\n" + self._make_tag_summary_str(tag_summary_dict, unit)
        issue.edit(body=body)

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


def get_forst_daily(email, password, github_token, repo_name):
    f = Forst(email, password)
    f.login()
    # also edit the issue body
    f.make_new_table(github_token, repo_name)
    return f.make_forst_daily()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("email", help="email")
    parser.add_argument("password", help="password")
    parser.add_argument("github_token", help="github_token")
    parser.add_argument("repo_name", help="repo_name")
    options = parser.parse_args()
    f = Forst(options.email, options.password)
    f.login()
    f._make_forest_dict()
    print(f.make_new_table(options.github_token, options.repo_name))
