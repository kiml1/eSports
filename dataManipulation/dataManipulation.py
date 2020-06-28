import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import numpy


# import data sets
earningsHistory = pd.read_csv('../scrapy/earningsHistory/eSports_players.csv')
earningsCountry = pd.read_csv(
    '../scrapy/earningsByCountry/earningsCountry_players.csv')
countryEarnings = pd.read_csv('../scrapy/countryEarnings/countryEarnings.csv')
femalePlayers = pd.read_csv('../scrapy/femalePlayers/femalePlayers.csv')
earningsU18 = pd.read_csv('../scrapy/earningsU18/U18_players.csv')

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

plt.savefig('../shiny/www/images/countriesEarnings.png')

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

plt.savefig('../shiny/www/images/topPlayers.png')


#=============================================================================#
# plot4 - games rank by prize money
plt.figure(figsize=(12, 6))
earningsCountry.groupby('game')['totalOverall'].sum().sort_values(
    ascending=False).head(20).plot.bar(color='r')

plt.savefig('../shiny/www/images/topGames_prizepool.png')


#=============================================================================#
# plot5 - top game by year
plt.figure(figsize=(12, 6))
earningsHistory.groupby('year')['totalOverall', 'game']


#=============================================================================#
# table6 - top 20 female players
plt.figure(figsize=(12, 6))
femalePlayers[['country', 'game', 'playerID',
               'playerName', 'totalOverall']].head(10).to_html('femalePlayersTable.html')


#=============================================================================#
# plot7 - men vs women comparison in prize money
labels = 'Top 500 female players earnings', 'Top 1 male player earnings'
sizes = [femalePlayers.totalOverall.sum(),
         earningsCountry.totalOverall.max()]
explode = (0.1, 0)
colors = ['lightcoral', 'lightskyblue']
total = sum(sizes)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct=lambda p: '${:,.2f}'.format(p * total / 100), colors=colors,
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.savefig('../shiny/www/images/menVSwomen_earnings.png')


#=============================================================================#
# plot8 - U18 earnings
# ---------prepare data
U18earnings_df = earningsU18[['playerID', 'totalOverall', 'totalU18']]
U18earnings_df['totalOver18'] = U18earnings_df['totalOverall'] - \
    U18earnings_df['totalU18']

# ---------plot
plt.figure(figsize=(12, 6))
plt.bar(U18earnings_df.playerID.head(10), U18earnings_df.totalU18.head(10))
plt.bar(U18earnings_df.playerID.head(10), U18earnings_df.totalOver18.head(10),
        bottom=U18earnings_df.totalU18.head(10))

plt.savefig('../shiny/www/images/U18_earnings.png')
