from .events import Event, Events

class Subscriber:
    def handle_event(self, event: Event) -> [Event]:
        if type(event) != type([]):
            event = [event]
        return_ops = []
        for e in event:
            switcher = {
                Events.SEVEN_OUT: self.handle_seven_out,
                Events.ESTABLISH_POINT: self.handle_establish_point,
                Events.ROLL: self.handle_roll,
                Events.NEW_SHOOTER: self.handle_new_shooter,
                Events.PLACE_BET: self.handle_place_bet,
                Events.LOST_BET: self.handle_lost_bet,
                Events.POINT_MADE: self.handle_point_made,
                Events.BET_TAKE_DOWN: self.handle_bet_take_down,
                Events.COLLECT_WINNINGS: self.handle_collect_winnings

            }
            # Get the function from switcher dictionary
            func = switcher.get(e.id, lambda x: Event(id=Events.NO_OP))
            # Execute the function
            return_value = func(e)
            if type(return_value) == type([]):
                return_ops += return_value
            else:
                return_ops.append(func(e))
        return return_ops

    def handle_seven_out(self, event: Event) -> Event:
        return self.no_op()

    def handle_establish_point(self, event: Event) -> Event:
        return self.no_op()

    def handle_roll(self, event: Event) -> Event:
        return self.no_op()

    def handle_new_shooter(self, event: Event)  -> Event:
        return self.no_op()

    def handle_place_bet(self, event: Event)  -> Event:
        return self.no_op()

    def handle_lost_bet(self, event: Event)  -> Event:
        return self.no_op()

    def handle_point_made(self, event: Event) -> Event:
        return self.no_op()

    def handle_collect_winnings(self, event: Event) -> Event:
        return self.no_op()

    def handle_bet_take_down(self, event: Event) -> Event:
        return self.no_op()

    def no_op(self) -> Event:
        return Event(id=Events.NO_OP) 