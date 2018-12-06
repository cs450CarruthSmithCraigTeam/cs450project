#Here is the source file for our project. Do what you want with it and be sure to comment the work you do with your name.
import json
import os
import pandas
from scipy import mean
from scipy.stats import zscore
from scipy.spatial.distance import cdist
from numpy import argpartition, add

def main():
    seasonDataObject = SeasonData("data/stats.data")

    historicalSeasonData = seasonDataObject.getHistoricalSeasonData()
    currentSeasonData = seasonDataObject.getCurrentSeasonData()

    factory = teamPerformanceModelFactory(historicalSeasonData)
    model = factory.fit(historicalSeasonData)

    # Predict a winner from the current season data
    prediction = model.predict(currentSeasonData)

    print 'We predict that the ' + prediction + ' will win the 2016 World Series'


class SeasonData():
    def __init__(self, filename):
        self.filename = filename
        self.attributeNames = ["year", "teamName", "winPercentage", "runsPerGame", "AVG", "ERA", "WHIP"]
        dataFromFile = pandas.read_csv(self.filename, header=None, names=self.attributeNames)

        self.scaledDataFromFile = pandas.DataFrame({
            "year": dataFromFile["year"],
            "teamName": dataFromFile["teamName"],
            "winPercentage": dataFromFile["winPercentage"],
            "runsPerGame": zscore(dataFromFile["runsPerGame"]),
            "AVG": zscore(dataFromFile["AVG"]),
            "ERA": zscore(dataFromFile["ERA"]),
            "WHIP": zscore(dataFromFile["WHIP"])
        })

    def getCurrentSeasonData(self):
        return {2016: self.scaledDataFromFile.query('year==2016')}

    def getHistoricalSeasonData(self):
        return {yearNumber: self.scaledDataFromFile.query('year==@yearNumber') for yearNumber in range(1976, 2016)}


class teamPerformanceModelFactory():  
    def __init__(self, historicalSeasonData):
        self.historicalSeasonData = historicalSeasonData

    def fit(self, historicalSeasonData):
        """ historicalSeasonData is the list of DataFrames full of stats separated by year """
        return(teamPerformanceModel(historicalSeasonData, k=3))


class teamPerformanceModel():
    def __init__(self, historicalSeasonData, k):
        """ The constructor stores the training data """
        self.historicalSeasonData = historicalSeasonData
        self.k = k

    def predict(self, currentSeasonData):

        columnList = ["runsPerGame", "AVG", "ERA", "WHIP"]
        teamNames = currentSeasonData[2016]['teamName'].unique()

        # Create a dict of lists to hold each current team's predicted performances by year
        currentMLBTeamPredictedPerformancesByYear = {}

        # Populate the dict of predicted performances by comparing each team to every year's league stats.
        # Store the resulting win average predictions by year
        for year in range(1976, 2016):
            numberOfHistoricalTeams = len(self.historicalSeasonData[year]['teamName'].unique())
            distanceMatrix = cdist(currentSeasonData[2016][columnList].values, self.historicalSeasonData[year][columnList].values, metric='euclidean')
            
            # Create a dict to represent the set of modern teams' predicted performances in a particular year 
            teamPerformances = {}

            # Every row in the distanceMatrix represents how close a current team is to each of the historical teams that existed that year 
            # Use this info to find the indexes of the K nearest neighbors in the list of historical teams that existed that year
            for i, row in enumerate(distanceMatrix):
                kNearestNeighborIndices = argpartition(row, self.k)[:self.k]
                kNearestNeighborWinAverages = self.historicalSeasonData[year].iloc[kNearestNeighborIndices]['winPercentage'].mean()

                # Store the team's predicted win percentage against this year's MLB
                teamName = currentSeasonData[2016].iloc[i]['teamName']
                teamPerformances[teamName] = kNearestNeighborWinAverages

            # Store this year's calculated team performances
            currentMLBTeamPredictedPerformancesByYear[year] = teamPerformances

        # Average a team's predicted performances across the years
        getAverageTeamPredictedPerformance = lambda teamName: sum([currentMLBTeamPredictedPerformancesByYear[year][teamName] for year in range(1976, 2016)]) / len(teamNames)
        averagePredictedPerformances = {teamName: getAverageTeamPredictedPerformance(teamName) for teamName in teamNames}
        
        # Sort the teams by their average predicted performance
        # Predict the team with the highest predicted performance
        sortedList = sorted(averagePredictedPerformances.items(), key=lambda x: x[1])

        prediction = sortedList[-1][0]

        return prediction


def lambda_handler(event, context):
    """ This is for when the function is run in the cloud, don't worry about it."""
    
    filename = os.environ['LAMBDA_TASK_ROOT'] + "/data/stats.data"
    seasonDataObject = SeasonData(filename)

    historicalSeasonData = seasonDataObject.getHistoricalSeasonData()
    currentSeasonData = seasonDataObject.getCurrentSeasonData()

    factory = teamPerformanceModelFactory(historicalSeasonData)
    model = factory.fit(historicalSeasonData)

    # Predict a winner from the current season data
    prediction = model.predict(currentSeasonData)

    print 'We predict that the ' + prediction + ' will win the 2016 World Series'
    
    return {
        'statusCode': 200,
        'headers': { 
            "Access-Control-Allow-Origin": "*" 
        },
        'body': json.dumps('We predict that the ' + prediction + ' will win the 2016 World Series')
    }

if __name__ == "__main__":
    main()
