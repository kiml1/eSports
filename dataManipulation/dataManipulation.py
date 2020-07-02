import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import numpy
import squarify


# import data sets
earningsHistory = pd.read_csv('../scrapy/earningsHistory/eSports_players.csv')
earningsCountry = pd.read_csv(
    '../scrapy/earningsByCountry/earningsCountry_players.csv')
countryEarnings = pd.read_csv('../scrapy/countryEarnings/countryEarnings.csv')
femalePlayers = pd.read_csv('../scrapy/femalePlayers/femalePlayers.csv')
earningsU18 = pd.read_csv('../scrapy/earningsU18/U18_players.csv')
gamesRankings = pd.read_csv('../scrapy/gameRankings/gameRankings.csv')
steamCharts = pd.read_csv('../shiny/www/data/steamCharts.csv')

# plots fonts
osaka = {'fontname': 'Osaka'}
font = {'size': 24}


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
# plot2 - number of players by country
# Draw Plot
plt.figure(figsize=(16, 10), dpi=80)
plt.plot(steamCharts.date, steamCharts.Users, color='#1a2139')

# Decoration
plt.xticks(rotation=0,
           fontsize=12, horizontalalignment='center', alpha=.7)
plt.yticks(fontsize=12, alpha=.7)
plt.title("Steam Users", fontsize=22)
plt.grid(axis='both', alpha=.3)

# Remove borders
plt.gca().spines["top"].set_alpha(0.0)
plt.gca().spines["bottom"].set_alpha(0.3)
plt.gca().spines["right"].set_alpha(0.0)
plt.gca().spines["left"].set_alpha(0.3)
plt.show()

#=============================================================================#
# plot3 - most successful players
plt.figure(figsize=(16, 10))
topPlayers_df = earningsCountry.sort_values(
    'totalOverall', ascending=False).head(10)

topPlayers_plot = plt.bar(
    topPlayers_df['playerID'], topPlayers_df['totalOverall']/1e6, color='#1a2139')
#plt.title('Top players earnings all time',  **font, ** osaka)
plt.ylabel('Millions US$', **font, **osaka)
plt.tick_params(axis='both', labelsize=16)
plt.grid(b=None, axis='x')

plt.savefig('../shiny/www/img/topPlayers.png')


#=============================================================================#
# plot4 - games rank by prize money
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 10), tight_layout=True)

gr_df = gamesRankings.sort_values('totalOverall', ascending=False)
genresR_df = gamesRankings.groupby('genre').sum(
).sort_values('totalOverall', ascending=False).reset_index()
# some games names are too long, need to shorten them
gr_df.loc[gr_df['game'] == 'PLAYERUNKNOWN’S BATTLEGROUNDS', 'game'] = 'PUBG'
gr_df.loc[gr_df['game'] == 'Counter-Strike: Global Offensive', 'game'] = 'CS:GO'
gr_df.loc[gr_df['game'] == 'Heroes of the Storm', 'game'] = 'HOTS'
gr_df.loc[gr_df['game'] == 'Arena of Valor', 'game'] = 'AoV'

color = ['#f73a18', '#C72508', '#AD351F', '#BD4631',
         '#A64230', '#F05F46', '#AB5141', '#96230F', '#993D2C', '#CF523C']
color2 = ['#1a2139', '#7B839E', '#183185', '#040A1C',
          '#688AFC', '#717582', '#223D94', '#575E75', '#2154FC', '#233982']

plt.subplot(1, 2, 1)
squarify.plot(sizes=gr_df.totalOverall.head(
    10), label=gr_df.game.head(10), color=color, text_kwargs={'fontsize': 15, 'color': 'white'})
plt.title('Game titles by prize pool', **font, ** osaka)
plt.axis('off')

plt.subplot(1, 2, 2)
squarify.plot(sizes=genresR_df.totalOverall.head(
    10), label=genresR_df.genre.head(10), color=color2, text_kwargs={'fontsize': 15, 'color': 'white'})
plt.title('Genres by prize pool', **font, ** osaka)
plt.axis('off')

plt.savefig('../shiny/www/images/gamesgenresPrizePool.png')


#=============================================================================#
# plot5 - steam charts
steamCharts['date'] = pd.to_datetime(steamCharts['DateTime'])
steamCharts.groupby(
    steamCharts.date.dt.year).mean().reset_index()

# Draw Plot
plt.figure(figsize=(16, 10), dpi=80)
plt.plot(steamCharts.date, steamCharts.Users, color='#1a2139')

# Decoration
plt.xticks(rotation=0,
           fontsize=12, horizontalalignment='center', alpha=.7)
plt.yticks(fontsize=12, alpha=.7)
plt.title("Steam Users", fontsize=22)
plt.grid(axis='both', alpha=.3)

# Remove borders
plt.gca().spines["top"].set_alpha(0.0)
plt.gca().spines["bottom"].set_alpha(0.3)
plt.gca().spines["right"].set_alpha(0.0)
plt.gca().spines["left"].set_alpha(0.3)
plt.show()


#=============================================================================#
# table6 - top 20 female players
plt.figure(figsize=(12, 6))
femalePlayers[['country', 'game', 'playerID',
               'playerName', 'totalOverall']].head(10).to_html('femalePlayersTable.html')


#=============================================================================#
# plot7 - men vs women comparison in prize money
labels = 'Top 500 female \n players earnings', "Johan 'N0tail' Sundstein \n earnings"
sizes = [femalePlayers.totalOverall.sum(),
         earningsCountry.totalOverall.max()]
explode = (0.1, 0)
colors = ['#ff1200', '#1a2139']
total = sum(sizes)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct=lambda p: '${:,.0f}'.format(p * total / 100), colors=colors,
        shadow=True, startangle=90, textprops={'color': "w", 'weight': 'bold'})
ax1.legend(labels,
           loc="center left",
           bbox_to_anchor=(1, 0, 0.5, 1))
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.savefig('../shiny/www/images/menVSwomen_earnings.png')


#=============================================================================#
# plot8 - U18 earnings
# ---------prepare data
U18earnings_df = earningsU18[['playerID', 'totalOverall', 'totalU18']]
U18earnings_df['totalOver18'] = U18earnings_df['totalOverall'] - \
    U18earnings_df['totalU18']

# ---------plot
plt.figure(figsize=(16, 10))

p1 = plt.bar(U18earnings_df.playerID.head(
    15), U18earnings_df.totalU18.head(15)/1e6, color='#f73a18')
p2 = plt.bar(U18earnings_df.playerID.head(15), U18earnings_df.totalOver18.head(15)/1e6,
             bottom=U18earnings_df.totalU18.head(15)/1e6, color='#1a2139')
plt.title('Top players with earnings under 18 years of age', ** osaka)
plt.ylabel('Millions US$', **osaka)
plt.xticks(U18earnings_df.playerID.head(15), **osaka)
plt.legend((p1[0], p2[0]), ('Under 18', 'Over 18'))
plt.grid(b=None, axis='x')

plt.savefig('../shiny/www/images/U18_earnings.png')


#=============================================================================#
# plot9 - top game by year
plt.figure(figsize=(12, 6))
earningsHistory.groupby('year')['totalOverall', 'game']
