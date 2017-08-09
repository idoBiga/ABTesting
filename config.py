import os

dir = os.path.dirname(__file__)

config = {
    "dataPath": os.path.join(dir, 'Recources/appsGrouped.csv'),
    "minSamples": 50000,
    "head": 1,
    "colNameForTrue": 'totalInstalls',
    'mcRuns': 1000
}


def getConfig():
    return config
