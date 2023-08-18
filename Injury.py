class Injury():
    def __init__(self, name, pos, injuries, status):
        self.name = name
        self.pos = pos
        self.injuries = injuries
        self.status = status

    def getInjury(self):
        return (self.name, self.pos, self.injuries, self.status)
    
    def toString(self):
        return f"{self.name}, {self.pos}, {self.injuries}, {self.status}"