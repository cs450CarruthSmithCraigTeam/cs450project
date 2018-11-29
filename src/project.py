#Here is the source file for our project. Do what you want with it and be sure to comment the work you do with your name.
import math as m
import json
import pandas

def main():
    myData = WorldSeriesData()
    return 0

class WorldSeriesData():
    def __init__(self):
        self.filename = "data/stats.data"
        self.attributeNames = ["year", "teamName", "winPercentage", "runsPerGame", "AVG", "ERA", "WHIP"]
        self.dataFromFile = pandas.read_csv(self.filename, header=None, names=self.attributeNames)
        
        self.yearData = {}
        for yearNumber in range(1976,2016):
            self.yearData[yearNumber] = self.dataFromFile.query('year==@yearNumber')


class WorldSeriesClassifier():  
    def __init__(self, trainingData = []):
        self.data = trainingData

    #Training data is the array of arrays full of stats separated by year    
    def fit(self, trainingData):
        return(WorldSeriesModel(trainingData))


class WorldSeriesModel():
    def __init__(self, trainingData):
        pass

    
    def predict(self, targets, k):
        """ Targets is the array of stats for the year we are using to predict the next year,
        i.e. stats for 2017 to predict 2018. K is the number of nearest neigbors we are using """

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
                    year[resultsPerTrial.index(min(resultsPerTrial))] = m.inf
                    temp -= 1
            resultsOfKNN.append(sumOfWinPercentage / count)
        # At this point, resultsOfKNN should have a result for every team based on the last 40 years.
        # This is where Shawn will take over to predict the
        ###############################################################
        return 0

########Added by Daniel#############
def lambda_handler(event, context):
    """ This is for when the function is run in the cloud, don't worry about it."""
    return {
        'statusCode': 200,
        'headers': { 
            "Access-Control-Allow-Origin": "*" 
        },
        'body': json.dumps('Hello from Lambda!')
    }

if __name__ == "__main__":
    main()
