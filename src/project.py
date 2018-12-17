#Here is the source file for our project. Do what you want with it and be sure to comment the work you do with your name.
import json
import os
import pandas
from scipy import mean
from scipy.stats import zscore
from scipy.spatial.distance import cdist
from numpy import argpartition, add

def main(filename):
    winningData = {
        2016: 'Chicago Cubs', 
        2015: 'Kansas City Royals', 
        2014: 'San Francisco Giants', 
        2013: 'Boston Red Sox', 
        2012: 'San Francisco Giants', 
        2011: 'St. Louis Cardinals', 
        2010: 'San Francisco Giants', 
        2009: 'New York Yankees', 
        2008: 'Philadelphia Phillies',
        2007: 'Boston Red Sox',
        2006: 'St. Louis Cardinals',
        2005: 'Chicago White Sox',
        2004: 'Boston Red Sox',
        2003: 'Florida Marlins',
        2002: 'Anaheim Angels',
        2001: 'Arizona Diamondbacks',
        2000: 'New York Yankees',
        1999: 'New York Yankees',
        1998: 'New York Yankees',
        1997: 'Florida Marlins',
        1996: 'New York Yankees',
        1995: 'Atlanta Braves',
        1994: 'Not held',
        1993: 'Toronto Blue Jays',
        1992: 'Toronto Blue Jays',
        1991: 'Minnesota Twins',
        1990: 'Cincinnati Reds',
        1989: 'Oakland Athletics',
        1988: 'Los Angeles Dodgers',
        1987: 'Minnesota Twins',
        1986: 'New York Mets' 
    }

    nameTranslations = {   
        'Seattle Mariners': 'SEA', 
        'New York Yankees': 'NYY',
        'Cleveland Indians': 'CLE',
        'New York Mets': 'NYM',
        'Atlanta Braves': 'ATL',
        'Montreal Expos': 'MON', 
        'St. Louis Cardinals': 'STL', 
        'Detroit Tigers': 'DET',
        'Oakland Athletics': 'OAK',
        'Baltimore Orioles': 'BAL',
        'San Francisco Giants': 'SFG',
        'Chicago Cubs': 'CHC',
        'Cincinnati Reds': 'CIN',
        'Kansas City Royals': 'KCR',
        'Houston Astros': 'HOU',
        'Philadelphia Phillies': 'PHI', 
        'Arizona Diamondbacks': 'ARI',
        'Los Angeles Angels of Anaheim': 'ANA',
        'Toronto Blue Jays': 'TOR',
        'Chicago White Sox': 'CHW',
        'Anaheim Angels': 'ANA',
        'Boston Red Sox': 'BOS',
        'Los Angeles Dodgers': 'LAD',
        'Pittsburgh Pirates': 'PIT',
        'San Diego Padres': 'SDP',
        'Washington Nationals': 'WSN',
        'Tampa Bay Rays': 'TBR',
        'Minnesota Twins': 'MIN',
        'Milwaukee Brewers': 'MIL',
        'Texas Rangers': 'TEX',
        'California Angels': 'CAL',
        'Florida Marlins': 'FLA',
        'Colorado Rockies': 'COL',
        'Miami Marlins': 'MIA',
        'Tampa Bay Devil Rays': 'TBD',
        'Not held': 'No Winner'
    }

    numberOfCorrectPredictions = 0
    numberOfTotalPredictions = 0
    for currentYear in range(1986, 2017):
        
        seasonDataObject = SeasonData(filename)

        historicalSeasonData = seasonDataObject.getHistoricalSeasonData(currentYear)
        currentSeasonData = seasonDataObject.getCurrentSeasonData(currentYear)

        factory = teamPerformanceModelFactory(historicalSeasonData)
        model = factory.fit(historicalSeasonData)

        # Predict a winner from the current season data
        prediction = model.predict(currentSeasonData)

        print prediction
        # print 'We predict that the', prediction, '[', nameTranslations[prediction], '] will win the', currentYear, 'World Series'
        if nameTranslations[prediction] == nameTranslations[winningData[currentYear]]:
            print "We got it right! The", prediction, "did win the world series in", currentYear
            numberOfCorrectPredictions += 1
        print ""
        numberOfTotalPredictions += 1

    accuracy = numberOfCorrectPredictions / float(numberOfTotalPredictions)
    
    print "The accuracy of our predictions was", accuracy, "percent."
    
    return accuracy

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

    def getCurrentSeasonData(self, currentYear):
        return {currentYear: self.scaledDataFromFile.query('year==@currentYear')}

    def getHistoricalSeasonData(self, currentYear):
        return {yearNumber: self.scaledDataFromFile.query('year==@yearNumber') for yearNumber in range(currentYear-10, currentYear)}


class teamPerformanceModelFactory():  
    def __init__(self, historicalSeasonData):
        self.historicalSeasonData = historicalSeasonData

    def fit(self, historicalSeasonData):
        """ historicalSeasonData is the list of DataFrames full of stats separated by year """
        return(teamPerformanceModel(historicalSeasonData, k=8))


class teamPerformanceModel():
    def __init__(self, historicalSeasonData, k):
        """ The constructor stores the training data """
        self.historicalSeasonData = historicalSeasonData
        self.k = k

    def predict(self, currentSeasonData):

        currentYear = currentSeasonData.keys()[0]

        columnList = ["runsPerGame", "AVG", "ERA", "WHIP"]
        teamNames = currentSeasonData[currentYear]['teamName'].unique()

        # Create a dict of lists to hold each current team's predicted performances by year
        currentMLBTeamPredictedPerformancesByYear = {}

        # Populate the dict of predicted performances by comparing each team to every year's league stats.
        # Store the resulting win average predictions by year
        for year in range(currentYear-10, currentYear):
            numberOfHistoricalTeams = len(self.historicalSeasonData[year]['teamName'].unique())
            distanceMatrix = cdist(currentSeasonData[currentYear][columnList].values, self.historicalSeasonData[year][columnList].values, metric='euclidean')
            
            # Create a dict to represent the set of modern teams' predicted performances in a particular year 
            teamPerformances = {}

            # Every row in the distanceMatrix represents how close a current team is to each of the historical teams that existed that year 
            # Use this info to find the indexes of the K nearest neighbors in the list of historical teams that existed that year
            for i, row in enumerate(distanceMatrix):
                kNearestNeighborIndices = argpartition(row, self.k)[:self.k]
                kNearestNeighborWinAverages = self.historicalSeasonData[year].iloc[kNearestNeighborIndices]['winPercentage'].mean()

                # Store the team's predicted win percentage against this year's MLB
                teamName = currentSeasonData[currentYear].iloc[i]['teamName']
                teamPerformances[teamName] = kNearestNeighborWinAverages

            # Store this year's calculated team performances
            currentMLBTeamPredictedPerformancesByYear[year] = teamPerformances

        # Average a team's predicted performances across the years
        getAverageTeamPredictedPerformance = lambda teamName: sum([currentMLBTeamPredictedPerformancesByYear[year][teamName] for year in range(currentYear-10, currentYear)]) / 10
        averagePredictedPerformances = {teamName: getAverageTeamPredictedPerformance(teamName) for teamName in teamNames}
        
        # Sort the teams by their average predicted performance
        # Predict the team with the highest predicted performance
        sortedList = sorted(averagePredictedPerformances.items(), key=lambda x: x[1])

        prediction = sortedList[-1][0]

        return prediction


def lambda_handler(event, context):
    """ This is for when the function is run in the cloud, don't worry about it."""

    filename = os.environ['LAMBDA_TASK_ROOT'] + "/data/stats.data"
    accuracy = main(filename)

    return {
        'statusCode': 200,
        'headers': { 
            "Access-Control-Allow-Origin": "*" 
        },
        'body': json.dumps('We predicted world series winners with an accuracy of ' + accuracy + ' percent.')
    }

if __name__ == "__main__":
    main("data/stats.data")
