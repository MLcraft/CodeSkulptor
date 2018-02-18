"""
Cookie Clicker Simulator
Made by MLcraft
"""

import simpleplot

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._cur_cookies = 0.0
        self._cur_time = 0.0
        self._cur_cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
    def __str__(self):
        """
        Return human readable state
        """
        string = "\nTime: " + str(self._cur_time) + \
        " Current cookies: " + str(self._cur_cookies) + \
        " CPS: " + str(self._cur_cps) + \
        " Total cookies: " + str(self._total_cookies) + \
        " History (length: " + str(len(self._history)) + "): " \
        + str(self._history)
        return string
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._cur_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cur_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._cur_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if (cookies - self._cur_cookies) > 0:
            return (cookies - self._cur_cookies) / (self._cur_cps)
        else:
            return 0.0
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time > 0:
            self._cur_time += time
            self._cur_cookies += self._cur_cps * time
            self._total_cookies += self._cur_cps * time
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost <= self._cur_cookies:
            self._cur_cookies -= cost
            self._cur_cps += additional_cps
            self._history.append((self._cur_time, item_name, cost, self._total_cookies))
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """

    # Replace with your code
    buildinfo = build_info.clone()
    while True:
        item = strategy(clickerState.get_cookies(), clickerState.get_cps(), duration - clickerState.get_time(), buildinfo)
        if item == None:
            break
        if item in buildinfo.build_items():    
            time_until = clickerState.time_until(buildinfo.get_cost(item))
            if time_until <= (duration - clickerState.get_time()):
                clickerState.wait(time_until)
                clickerState.buy_item(item, buildinfo.get_cost(item), buildinfo.get_cps(item))
                buildinfo.update_item(item)
                print item, buildinfo.get_cost(item), buildinfo.get_cps(item)
            else:
                return None
    return clickerState


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    Always buy the cheapest item you can afford.
    """
    items = {}
    for i in build_info.build_items():
        if build_info.get_cost(i) < cookies + cps * time_left:
            items[build_info.get_cost(i)] = i
    if len(items) > 0:
        return items[min(items)]
    else:
        return None
def strategy_expensive(cookies, cps, time_left, build_info):
    """
    Always buy the most expensive item you can afford.
    """
    items = {}
    for i in build_info.build_items():
        if build_info.get_cost(i) < cookies + cps * time_left:
            items[build_info.get_cost(i)] = i
    if len(items) > 0:
        return items[max(items)]
    else:
        return None

def strategy_best(cookies, cps, time_left, build_info):
    """
    The best strategy the programmer can think of.
    """
    return None
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cheap)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
clickerState = ClickerState()   
run()
