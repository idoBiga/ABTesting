import matplotlib.pyplot as plt
import pandas as pd
import pymc3 as pm
import numpy as np

from config import getConfig

config = getConfig()
df = pd.read_csv(config['dataPath'])

dfFiltered = df[df['totalCount'] > config['minSamples']].sort_values('totalCount', ascending=False).reset_index(
    drop=True)

traces = {}
for i in range(config['head']):
    appName = dfFiltered['bidRequest:::app:::bundle'].iloc[i]

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
        burned_trace = trace[5000:]

    traces[appName] = burned_trace['p']

cmap = plt.get_cmap('hsv')
colors = [cmap(i) for i in np.linspace(0., 1., num=config['head'])]

for i, (name, trace) in enumerate(traces.iteritems(), 1):
    plt.hist(trace, bins=50, alpha=0.5, histtype="stepfilled", normed=True, label=name, color=colors[i])

plt.title("Posterior CTR")
plt.legend()
plt.show()
