#Here is the source file for our project. Do what you want with it and be sure to comment the work you do with your name.
import math as m

class WorldSeries:
    def __init__(self, data = []):
        self.data = data

    #Training data is the array of arrays full of stats separated by year    
    def train(self, trainingData):
        self.data = trainingData

    #Targerts is the array of stats for the year we are using to predict the 
    # next year i.e. stats for 2017 to predict 2018
    # K is the number of nearest neigbors we are using
    def predict(self, targets, k):
        #####################DAVID'S CODE##############################
        # Column breakdown = year, name, win %, runs/game, AVG, ERA, WHIP
        # Loop through each team in target array
        # For each team, loop through each year in data array
        # For each year, loop through each team
        resultsOfKNN = []
        for currentTeam in targets:
            count = 0
            sumOfWinPercentage = 0.0
            for year in self.data:
                temp = k
                resultsPerTrial = []
                for pastTeam in year:   
                    distance1 = (currentTeam[3] - pastTeam[3]) ** 2
                    distance2 = (currentTeam[4] - pastTeam[4]) ** 2
                    distance3 = (currentTeam[5] - pastTeam[5]) ** 2
                    distance4 = (currentTeam[6] - pastTeam[6]) ** 2  

                    resultsPerTrial.append(m.sqrt(distance1 + distance2 + distance3 + distance4))
                    count += 1
                while (temp > 0):    
                    sumOfWinPercentage += year[resultsPerTrial.index(min(resultsPerTrial))][2]
                    temp -= 1
            resultsOfKNN.append(sumOfWinPercentage / count)
        # At this point, resultsOfKNN should have a result for every team based on the last 40 years.
        # This is where Shawn will take over to predict the
        ###############################################################
                return 0
        