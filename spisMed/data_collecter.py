import pandas as pd
from spisMed.chefs import Chef, day_to_num 
from datetime import datetime, timedelta

from typing import List, Dict


DATE_FORMAT: str = "%d-%m-%Y"
dan_to_eng = {
    "mandag": "monday",
    "tirsdag": "tuesday",
    "onsdag": "wednesday",
    "torsdag": "thursday",
    "fredag": "friday",
    "lørdag": "saturday",
    "søndag": "sunday"
}

def to_bool(x):
    if isinstance(x, str):
        if x.lower() == "true":
            return True
        elif x.lower() == "false":
            return False
    return x

class Collector:

    def __init__(self):
        data = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vQ94VJGZ79tMKLB8m_ELxIKNVbrZpujNbMDs_rZygvSuI14WxtIBxHpfdvzPsgh2Yf2mBz_KaHC9hQy/pub?output=csv")
        self.data = data.applymap(to_bool)
        self.cols = data.columns.values
        self.people = self.cols[1: 1+15]
        self.start_date = self.data["Start Dato"][0]
        self.end_date   = self.data["Slut Dato"][0]
        self.days = list(self.data["Dag"][1:6])
    
    def create_chefs(self):
        for p in self.people:
            unable_weekdays = [day for i, day in enumerate(self.days) if self.data[p][i]]
            specific_days = [datetime.strptime(date, DATE_FORMAT) for date in self.data[p][6:] if isinstance(date, str) ]
            c = Chef(p, self.data[p][0], unable_weekdays, specific_days)

#def get_days(start: str, end: str, include: Dict[str, bool]) -> List[datetime.datetime]:
    def get_days(self) -> List[datetime]:
        """
        Get all days between start and end date in which there should be a "Madklub"
        """
        start_datetime = datetime.strptime(self.start_date, DATE_FORMAT)
        end_datetime = datetime.strptime(self.end_date, DATE_FORMAT)
        date_list = [start_datetime + timedelta(days=x) for x in range(0, (end_datetime-start_datetime).days)]
        days_idx = set([i for day,i in day_to_num.items() if day in self.days])
        return list(filter(lambda x: x.weekday() in days_idx, date_list))
    
