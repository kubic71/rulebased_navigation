from db_helper import indent
import time

class Condition:
    def match(self, db):
        return False

    def __or__(self, other):
        return Or(self, other)
    
    def __and__(self, other):
        return And(self, other)
    
    def __invert__(self):
        return Not(self)
    
    def __str__(self):
        return self.__class__.__name__


    def __repr__(self):
        return self.__str__()
    
class Or(Condition):
    def __init__(self, r1, r2):
        self.r1 = r1
        self.r2 = r2

    def match(self, db):
        return self.r1.match(db) or self.r2.match(db)
    
    def __str__(self):
        return f"({self.r1} | {self.r2})"

class And(Condition):
    def __init__(self, r1, r2):
        self.r1 = r1
        self.r2 = r2

    def match(self, db):
        return self.r1.match(db) and self.r2.match(db)

    def __str__(self):
        return f"({self.r1} & {self.r2})"


class Not(Condition):
    def __init__(self, r):
        self.r = r

    def match(self, db):
        return not self.r.match(db)

    def __str__(self):
        return f"~{self.r}"

class AlwaysCondition(Condition):
    """Condition, that is always true"""

    def match(self, db):
        return True

    def __str__(self):
        return "AlwaysTrue"



class BasicCond(Condition):
    def __init__(self, name="condition_1"):
        self.name = name
    
    def __str__(self):
        return self.name
        

class Action:

    def do(self, db):
        pass

    def __str__(self):
        return self.__class__.__name__


class Rule:
    def __init__(self, condition, *actions):
        self.condition = condition
        self.actions = actions
    
    def do_actions(self, db):
        for action in self.actions:
            action.do(db)
    
    def actions_str(self):
        s = ""
        for i, action in enumerate(self.actions):
            s += f"{i+1}. {action}\n"
        return s


    def __str__(self):
        return "Condition:\n" + indent(str(self.condition)) + "\nActions:\n" + indent(self.actions_str())


class RuleEngine:
    def __init__(self, rules, db, maze, delay=1, verbose=False):
        self.rules = rules
        self.db = db
        self.maze = maze
        self.delay = delay
        self.verbose = verbose

    def print_progress(self):
        if self.verbose:
            print(self.maze.db)

        print(self.maze)
        time.sleep(self.delay)

    
    def step(self):
        # go through the rules and execute all matching
        matched_any = False
        for r in self.rules:
            if r.condition.match(self.db):
                print("Matched rule:\n", indent(str(r)))
                r.do_actions(self.db)
                matched_any = True

                self.print_progress()

        if not matched_any:
            raise Exception("No matching rule found!")

if __name__ == "__main__":
    conj = BasicCond("cond1") & BasicCond("cond2") & BasicCond("cond3")
    print(conj)

    disj = BasicCond("cond1") | BasicCond("cond2")
    print(disj)

    notr = ~conj
    print(notr)
