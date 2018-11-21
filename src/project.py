#Here is the source file for our project. Do what you want with it and be sure to comment the work you do with your name.

#####################DAVID'S CODE##############################
class WorldSeries:
    def __init__(self, data = []):
        self.data = data

    #Training data is the array of arrays full of stats separated by year    
    def train(self, trainingData):
        self.data = trainingData

    #Targerts is the array of stats for the year we are using to predict the 
    # next year i.e. stats for 2017 to predict 2018
    def predict(self, targets):
        return targets


###############################################################