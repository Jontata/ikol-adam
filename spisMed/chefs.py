import heapq
from typing import List, Tuple, Set
from datetime import datetime
from datetime import timedelta
import functools

day_to_num = { "mandag": 1, "tirsdag": 2, "onsdag": 3, "torsdag": 4, "fredag": 5, "lørdag": 6, "søndag": 7}
num_to_day = {v: k for k, v in day_to_num.items()}
ONE_DAY = timedelta(days=1)

@functools.total_ordering
class Chef:
    all_chefs: List['Chef'] = []
    secondary_days_flag: bool = False
    def __init__(self, name, assistent_chef: bool, unable_weekdays: List[str] = [], unable_dates: List[str] = []):
        self.name = name
        self.unable_weekdays = set(unable_weekdays)
        self.unable_dates = set(unable_dates)
        self.main_days:         Set[datetime] = set()
        self.days_left: int  = 0

        self.assistent_chef = assistent_chef
        self.secondary_days: Set[datetime] = set()

        Chef.all_chefs.append(self)

    def __repr__(self):
        return f"Chef({self.name})"
    
    def __eq__(self, other: 'Chef'):
        return other.days_left == self.days_left 
    
    def __lt__(self, other: 'Chef'):
        return self.days_left < other.days_left
    

    def __check_day(self, day:datetime, strict: bool = True) -> bool:
        can_work =  (not strict or (day.weekday() not in self.unable_weekdays)) and \
                    (not strict or (day not in self.unable_dates)) and \
                    (day not in self.main_days) and \
                    (day not in self.secondary_days)
        return can_work
    
    def add_day(self, day: datetime) -> None:
        assert(self.days_left > 0)
        if Chef.secondary_days_flag:
            self.secondary_days.add(day)
        else:
            self.main_days.add(day)
        self.days_left -= 1
    
    def remove_day(self,day: datetime) -> None:
        if Chef.secondary_days_flag:
            if day in self.secondary_days:
                self.secondary_days.remove(day)
                self.days_left += 1
        else:
            if day in self.main_days:
                self.main_days.remove(day)
                self.days_left += 1



    def is_able(self, day: datetime, strict:bool = True) -> bool:
        can_work_day = self.__check_day(day)
        can_work_before = self.__check_day(day-ONE_DAY, strict = False)
        can_work_after = self.__check_day(day+ONE_DAY, strict = False)
        return can_work_day and (not strict or (can_work_before and can_work_after))


class ChefHeap:
    def __init__(self):
        self.heap: List[Tuple[int, Chef]] = []
        heapq.heapify(self.heap)

    def push(self, c: Chef) -> None:
        if c.days_left != 0:
            heapq.heappush(self.heap, (-c.days_left, c))

    def pop(self) -> Chef:

        _ , item = heapq.heappop(self.heap)
        return item
    
    def __iter__(self):
        while len(self.heap) > 0:
            yield self.pop()

    def __len__(self):
        return len(self.heap)

