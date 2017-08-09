import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymc3 as pm

from config import getConfig


def plotPosterior():
    global i, trace
    cmap = plt.get_cmap('hsv')
    colors = []
    for i in np.linspace(0.0, 1.0, config['head']):
        colors.append(cmap(i))
    for i, (name, trace) in enumerate(traces.iteritems(), 0):
        plt.hist(trace, label=name, color=colors[i], **config['histParams'])


config = getConfig()
df = pd.read_csv(config['dataPath'])

dfFiltered = df[df['totalCount'] > config['minSamples']].sort_values('totalCount', ascending=False).reset_index(
    drop=True)

traces = {}
for i in range(1, config['head']):
    appName = dfFiltered.iloc[i]['bidRequest:::app:::bundle']

    occurrences = [True] * dfFiltered[config['colNameForTrue']].iloc[i] + [False] * (
        dfFiltered['totalCount'].iloc[i] - dfFiltered[config['colNameForTrue']].iloc[i])

    # Laplace smoothing
    occurrences.append(True)
    occurrences.append(False)

    with pm.Model() as model:
        p = pm.Beta('p', alpha=1, beta=1)

    with model:
        obs = pm.Bernoulli("obs", p, observed=occurrences)
        step = pm.Metropolis()
        trace = pm.sample(config['mcRuns'], step=step)
        burnedTrace = trace[5000:]

    traces[appName] = burnedTrace['p']

plotPosterior()

plt.title("Posterior CTR")
plt.legend()
plt.show()
