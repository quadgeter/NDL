class Player:
    def __init__(self, name, est_score) -> None:
        self.name = name
        self.est_score = est_score

    
    def setName(self, name):
        self.name = name

    def setScore(self, est_score):
        self.est_score = est_score

    def getName(self):
        return self.name
    def getScore(self):
        return self.est_score
    
    def toString(self):
        return f"{self.getName()}: {self.getScore()}"
        
