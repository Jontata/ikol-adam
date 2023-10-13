from typing import Dict, List, Tuple, Optional
import json
import datetime
import random
import os
from spisMed.chefs import ChefHeap, Chef
from spisMed.data_collecter import Collector

def find(day: datetime.datetime, secondary_chef: bool = False) -> Chef:
    if secondary_chef:
        for chef in Chef.all_chefs:
            if day in chef.secondary_days:
                return chef
    else:
        for chef in Chef.all_chefs:
            if day in chef.main_days:
                return chef
    return Chef('NOT_FOUND')


def fix(to_add: List[Chef], prev_days: List[datetime.datetime]) -> None:
    """
    """

    days_rev = prev_days[::-1]
    cur_day = days_rev[0]
    for swap_day in days_rev[1:]:
        chef = find(swap_day, Chef.secondary_days_flag)
        assert chef.name != 'NOT_FOUND', "Aaaaargh, den er vidst ikke helt god mester"
        if chef.is_able(cur_day):
            # Try and swap
            for swap_chef in to_add:
                if swap_chef.is_able(swap_day):
                    swap_chef.add_day(swap_day)
                    chef.remove_day(swap_day)
                    chef.add_day(cur_day)
                    return 
    print("Could not fix :(")
    exit(1)


def assign_chefs(days: List[datetime.datetime], chefs: List[Chef]):
    if len(days) == 0: return
    days_each = len(days) // len(chefs)
    needs_extra = len(days) % len( chefs) # How many will get an extra day
    random.shuffle(chefs) # Shuffle so the `needs_extra` chefs are random
    heap = ChefHeap()
    for c in chefs:
        c.days_left = days_each + (1 if needs_extra > 0 else 0)
        needs_extra -= 1
        heap.push(c)

    for i, day in enumerate(days):
        found = False
        to_add = []
        for chef in heap:
            to_add.append(chef)
            if chef.is_able(day):
                chef.add_day(day)
                found = True
                break
            
        if not found:
            fix(to_add, days[:i+1])

        # Add all people who could not this day and were therefore skipped
        for p in to_add:
            heap.push(p)
        

def main():

    c = Collector()
    c.create_chefs()
    food_days = c.get_days()
    assign_chefs(food_days, Chef.all_chefs)

    secondary_chefs = list(filter(lambda c: c.assistent_chef, Chef.all_chefs))
    secondary_days = [day for day in food_days if find(day, False).assistent_chef]
    Chef.secondary_days_flag = True
    assign_chefs(secondary_days, secondary_chefs)

    ans = {}
    for day in food_days:
        main_chef = find(day, False)
        sec_chef = Chef('', False)
        if main_chef.assistent_chef:
            sec_chef = find(day, True)
        ans[day.strftime("%d-%m-%Y")] = [main_chef.name, sec_chef.name]
    with open(os.path.join(os.path.dirname(__file__),"output.json"), 'w') as file:
        json.dump(ans, file, indent=4)




if __name__ == '__main__':
    main()
