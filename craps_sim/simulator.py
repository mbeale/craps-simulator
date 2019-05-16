import numpy as np
from .events import Event, Events
from .simulator_summary import SimulatorSummary, summary_dtype

class CrapsSimulator:
    is_point_established = False
    point_is = None
    simulation = None
    current_roll = []
    roll_count = 1
    
    established_bets = []
    non_established_bets = []

    events = []
    shooter_summary = None
    current_shooter = None
    
    player_balance = 0
    bets = []

    def __init__(self):
        self.events = []
        self.bets = []
        self.current_shooter = None

    def add_bets(self, bets: list) -> None:
        if type(bets) == type([]):
            self.bets += bets
        else:
            self.bets += [bets]
    
    def combinations(self, num):
        combos = []
        for l in range(1,7):
            for r in range(1,7):
                if l + r == num:
                    combos.append([l,r])
        return combos
    
    def establishing_point(self, roll):
        return roll.tolist() not in sorted(self.combinations(2) + self.combinations(3) + self.combinations(7) + self.combinations(11) + self.combinations(12))
    
    def seven_out(self, roll):
        return roll.tolist() in self.combinations(7)

    def set_sample_data(self, data):
        self.simulation = data
    
    def generate_rolls(self, rolls):
        left = np.random.choice([1,2,3,4,5,6], rolls)
        right = np.random.choice([1,2,3,4,5,6], rolls)
        self.simulation = np.array([left, right]).reshape((rolls, 2))

    def emit_event(self, event):
        self.handle_event(event)
        if type(event) != type([]):
            event = [event]
        for e in event:
            for bet in self.bets:
                self.handle_event(bet.handle_event(e))
    
    def handle_event(self, event):
        if type(event) != type([]):
            event = [event]
        for e in event:
            self.events.append(e)
            if e.id in [Events.SEVEN_OUT, Events.ESTABLISH_POINT, Events.POINT_MADE]:
                self.flip_established_point()
            if e.id == Events.ESTABLISH_POINT:
                self.point_is = e.data['point']
            elif e.id == Events.NEW_SHOOTER:
                if self.current_shooter:
                    if type(self.shooter_summary) != type(None):
                        self.shooter_summary = np.vstack([self.shooter_summary, self.current_shooter.np_array])
                    else:
                        self.shooter_summary = self.current_shooter.np_array
                self.current_shooter = SimulatorSummary()
            self.current_shooter.handle_event(e)


        
    def flip_established_point(self):
        self.is_point_established = False if self.is_point_established else True

    def summarize_data(self):
        summary = None
        return {'shooters': self.shooter_summary, 'summary': summary}


    def simulate(self): 
        self.emit_event(Event(id=Events.NEW_SHOOTER))
        for roll in self.simulation:
            if self.is_point_established:
                if self.seven_out(roll):
                    self.emit_event(Event(id=Events.SEVEN_OUT))
                    self.emit_event(Event(id=Events.NEW_SHOOTER))
                elif sum(roll) == self.point_is:
                    self.emit_event(Event(id=Events.POINT_MADE, data={'point': sum(roll), 'dice': roll.tolist()}))
                else:
                    self.emit_event(Event(id=Events.ROLL, data={'roll': roll}))
            else:
                if self.establishing_point(roll):
                    self.emit_event(Event(id=Events.ESTABLISH_POINT, data={'point': sum(roll), 'dice': roll.tolist()}))
                else:
                    self.emit_event(Event(id=Events.ROLL, data={'roll': roll}))  
        return self.summarize_data()        