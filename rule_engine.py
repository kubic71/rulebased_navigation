
class Condition:
    def match(self, db):
        return False

    def __or__(self, other):
        return Or(self, other)
    
    def __and__(self, other):
        return And(self, other)
    
    def __invert__(self):
        return Not(self)

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


class BasicCond(Condition):
    def __init__(self, name="condition_1"):
        self.name = name
    
    def __str__(self):
        return self.name
        

class Action:

    def do(self, db):
        pass


class UpdateMapWithSensorData(Action):
    def do(self, db):
        # Add Walls/Free space information to the db based on sensor data
        pass


class RuleEngine:
    def __init__(self, rules, db):
        self.rules = rules
        self.db = db
    
    def step(self):
        # go through the rules and return the one matching
        for r in self.rules:
            if r.match(self.db):
                r.action(self.db)
                return
        raise Exception("No matching rule found!")

if __name__ == "__main__":
    conj = BasicCond("cond1") & BasicCond("cond2") & BasicCond("cond3")
    print(conj)

    disj = BasicCond("cond1") | BasicCond("cond2")
    print(disj)

    notr = ~conj
    print(notr)
