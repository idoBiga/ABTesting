import os

dir = os.path.dirname(__file__)

config = {
    "dataPath": os.path.join(dir, 'Recources/appsGrouped.csv'),
    "minSamples": 50000,
    "head": 5,
    "colNameForTrue": 'totalInstalls',
    'mcRuns': 15000,
    "histParams": {
        'bins': 50,
        'alpha': 0.5,
        'histtype': "stepfilled",
        'normed': True
    }
}


def getConfig():
    return config
