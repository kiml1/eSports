import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter


# import data sets
earningsHistory = pd.read_csv('../scrapy/earningsHistory/eSports_players.csv')
earningsCountry = pd.read_csv(
    '../scrapy/earningsByCountry/earningsCountry_players.csv')
countryEarnings = pd.read_csv('../scrapy/countryEarnings/countryEarnings.csv')

#=============================================================================#
# plot1 - countries ranking by total earnings
# ---------prepare data
countriesRankingEarnings_df = countryEarnings[['country', 'totalOverall']]
countriesRankingEarnings = countriesRankingEarnings_df.groupby(
    'country', as_index=False).sum().sort_values('totalOverall', ascending=False).head(20)

# ---------plot
plt.figure(figsize=(20, 6))
sns.set(style="whitegrid")
countriesRankingEarnings_plot = sns.barplot(
    x="totalOverall", y="country", data=countriesRankingEarnings, color='g')
plt.xlabel('Purchase amount', fontsize=18)
countriesRankingEarnings_plot.set(xlabel='Total Earnings in US$', ylabel='')
plt.savefig('countriesEarnings.png')

#=============================================================================#
# plot2 - eSports earnings by year
plt.figure(figsize=(12, 6))
earningsHistory.groupby('year')['totalYear'].sum().sort_values(
    ascending=True).plot.bar(color='r')


#=============================================================================#
# plot3 - most successful players
plt.figure(figsize=(20, 6))
topPlayers_df = earningsCountry.sort_values(
    'totalOverall', ascending=False).head(15)

topPlayers_plot = plt.bar(
    topPlayers_df['playerID'], topPlayers_df['totalOverall'])
plt.xlabel('Player in-game ID')
plt.ylabel('Earnings US$')
plt.savefig('topPlayers.png')


#=============================================================================#
# plot4 - games rank by prize money
plt.figure(figsize=(12, 6))
earningsCountry.groupby('game')['totalOverall'].sum().sort_values(
    ascending=False).head(20).plot.bar(color='r')
plt.savefig('topGames_prizepool.png')

#=============================================================================#
# plot5 - top game by year
plt.figure(figsize=(12, 6))
earningsHistory.groupby('year')['totalOverall', 'game']
