from .bet import Bet
from .events import Events, Event
import numpy as np

class HardWays(Bet):

    hard_way:int = 4
    play_when_point_is_hard_way: bool = False
    always_work: bool = False
    odds = {
        4: 7,
        6: 9,
        8: 9,
        10: 7
    }

    def set_hard_way(self, n: int) -> None:
        if n not in [4,6,8,10]:
            raise ValueError(f'{n} is not a valid hard way number [4,6,8,10]')
        self.hard_way = n

    def handle_seven_out(self, event: Event) -> Event:
        if self.working and self.bet_placed:
            self.bet_placed = False
            return Event(id=Events.LOST_BET, data={'amount': self.bet_amount})
        elif not self.working and self.bet_placed:
            self.bet_placed = False
            return Event(id=Events.BET_TAKE_DOWN, data={'amount': self.bet_amount})       
        return self.no_op()

    def handle_establish_point(self, event: Event) -> Event:
        if not self.bet_placed and (self.play_when_point_is_hard_way or event.data['point'] != self.hard_way):
            self.working = True
            self.bet_placed = True
            return Event(id=Events.PLACE_BET, data={'amount': self.bet_amount})
        elif self.bet_placed and self.working and event.data['dice'] == [self.hard_way / 2, self.hard_way / 2]:
            return Event(id=Events.COLLECT_WINNINGS, data={'amount': self.calculate_winnings()})
        else:
            self.working = True
            return self.no_op()

    def handle_point_made(self, event: Event) -> Event:
        if self.working and self.bet_placed:
            self.working = False if not self.always_work else True
            if sum(event.data['dice']) == self.hard_way:
                if event.data['dice'] == [self.hard_way / 2, self.hard_way / 2]:
                    return Event(id=Events.COLLECT_WINNINGS, data={'amount': self.calculate_winnings()})
                self.bet_placed = False
                return Event(id=Events.LOST_BET, data={'amount': self.bet_amount})
        return self.no_op()

    def handle_roll(self, event: Event) -> Event:
        if self.working and self.bet_placed:
            if event.data['roll'].tolist() == [self.hard_way / 2, self.hard_way / 2]:
                return Event(id=Events.COLLECT_WINNINGS, data={'amount': self.calculate_winnings()})
            elif sum(event.data['roll']) == self.hard_way:
                self.bet_placed = False
                self.working = False
                return Event(id=Events.LOST_BET, data={'amount': self.bet_amount})
        return self.no_op()

    def calculate_winnings(self) -> float:
        return self.odds[self.hard_way] * self.bet_amount - self.bet_amount
        

def CreateNewHardways(num: int, bet_amount: int, play_when_point_is_hard_way:bool = False, always_work: bool = False) -> HardWays:
    hw = HardWays()
    hw.set_hard_way(num)
    hw.bet_amount = bet_amount
    hw.play_when_point_is_hard_way = play_when_point_is_hard_way
    hw.always_work = always_work
    return hw
