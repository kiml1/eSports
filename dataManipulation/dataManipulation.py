import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import numpy
import squarify
import matplotlib.lines as mlines


# import data sets
earningsHistory = pd.read_csv('../scrapy/earningsHistory/eSports_players.csv')
earningsCountry = pd.read_csv(
    '../scrapy/earningsByCountry/earningsCountry_players.csv')
countryEarnings = pd.read_csv('../scrapy/countryEarnings/countryEarnings.csv')
femalePlayers = pd.read_csv('../scrapy/femalePlayers/femalePlayers.csv')
earningsU18 = pd.read_csv('../scrapy/earningsU18/U18_players.csv')
gamesRankings = pd.read_csv('../scrapy/gameRankings/gameRankings.csv')
steamCharts = pd.read_csv('../shiny/www/data/steamCharts.csv')
offlineTournaments = pd.read_csv(
    '../scrapy/offlineTournaments/offlineTournaments.csv')
onlineTournaments = pd.read_csv(
    '../scrapy/onlineTournaments/onlineTournaments.csv')
statsHistory = pd.read_csv(
    '../scrapy/tournamentsHistory/tournamentsHistory.csv')

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
# prepare data
U18earnings_df = earningsU18[['playerID', 'totalOverall', 'totalU18']]
U18earnings_df['totalOver18'] = U18earnings_df['totalOverall'] - \
    U18earnings_df['totalU18']

# plot
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
# plot9 - prize pool evolution history
# Draw plot
fig, ax = plt.subplots(figsize=(16, 10), dpi=80)
ax.hlines(y=statsHistory.index, xmin=0, xmax=250, color='gray',
          alpha=0.7, linewidth=1, linestyles='dashdot')
ax.scatter(y=statsHistory.index, x=statsHistory.totalPrize/1e6,
           s=75, color='#f73a18', alpha=0.7)

# Title, Label, Ticks and Ylim
ax.set_title('Prize pool by Year', fontdict={'size': 22})
ax.set_yticks(statsHistory.index)
ax.set_yticklabels(statsHistory.year, fontdict={
                   'horizontalalignment': 'right', 'size': 16})
plt.yticks(fontsize=16)
plt.xticks(fontsize=16)
plt.xlabel('Prize pool million US$', fontsize=16)
plt.show()


#=============================================================================#
# plot10 - country earnings now and then
years = [2009, 2019]
countryPrizepoolHistory = earningsHistory.groupby([
    earningsHistory.year, earningsHistory.country]).sum().reset_index()
countryPrizepoolHistory = countryPrizepoolHistory[countryPrizepoolHistory.year.isin(
    years)]
countryPrizepoolHistory = countryPrizepoolHistory.drop(
    columns=['totalOverall'])
countryPrizepoolHistory = countryPrizepoolHistory.set_index('country')
countryPrizepoolHistory = countryPrizepoolHistory.pivot(
    columns='year', values='totalYear')
countryPrizepoolHistory = countryPrizepoolHistory.reset_index()
countryPrizepoolHistory = countryPrizepoolHistory.dropna()

# draw line


def newline(p1, p2, color='black'):
    ax = plt.gca()
    l = mlines.Line2D([p1[0], p2[0]], [p1[1], p2[1]], color='red' if p1[1] -
                      p2[1] > 0 else 'green', marker='o', markersize=6)
    ax.add_line(l)
    return l


fig, ax = plt.subplots(1, 1, figsize=(14, 14), dpi=80)

# Vertical Lines
ax.vlines(x=1, ymin=500, ymax=13000, color='black',
          alpha=0.7, linewidth=1, linestyles='dotted')
ax.vlines(x=3, ymin=500, ymax=13000, color='black',
          alpha=0.7, linewidth=1, linestyles='dotted')

# Points
ax.scatter(y=countryPrizepoolHistory[2009], x=np.repeat(1, countryPrizepoolHistory.shape[0]),
           s=10, color='black', alpha=0.7)
ax.scatter(y=countryPrizepoolHistory[2019], x=np.repeat(3, countryPrizepoolHistory.shape[0]),
           s=10, color='black', alpha=0.7)

# Line Segmentsand Annotation
for p1, p2, c in zip(countryPrizepoolHistory[2009], countryPrizepoolHistory[2019], countryPrizepoolHistory['country']):
    newline([1, p1], [3, p2])
    ax.text(1-0.05, p1, c + ', ' + str(round(p1)), horizontalalignment='right',
            verticalalignment='center', fontdict={'size': 14})
    ax.text(3+0.05, p2, c + ', ' + str(round(p2)), horizontalalignment='left',
            verticalalignment='center', fontdict={'size': 14})

# 'Before' and 'After' Annotations
ax.text(1-0.05, 13000, '', horizontalalignment='right',
        verticalalignment='center', fontdict={'size': 18, 'weight': 700})
ax.text(3+0.05, 13000, '', horizontalalignment='left',
        verticalalignment='center', fontdict={'size': 18, 'weight': 700})

# Decoration
ax.set_title("Slopechart: Comparing GDP Per Capita between 1952 vs 1957",
             fontdict={'size': 22})
ax.set(xlim=(0, 4), ylim=(0, 14000), ylabel='Mean GDP Per Capita')
ax.set_xticks([1, 3])
ax.set_xticklabels(["2009", "2019"])
plt.yticks(np.arange(0, 25e6, 1e6), fontsize=12)

# Lighten borders
plt.gca().spines["top"].set_alpha(.0)
plt.gca().spines["bottom"].set_alpha(.0)
plt.gca().spines["right"].set_alpha(.0)
plt.gca().spines["left"].set_alpha(.0)
plt.show()


#=============================================================================#
# plot11 - scatter prizepool numbertournaments genre
# Prepare Data
prizeTournaments = gamesRankings.groupby('genre').sum().reset_index()
prizeTournaments = prizeTournaments.assign(
    totalOverall=lambda x: x.totalOverall / 1e6)

# Create as many colors as there are unique genre
genres = np.unique(prizeTournaments['genre'])
colors = [plt.cm.tab10(i/float(len(genres)-1))
          for i in range(len(genres))]

# Draw Plot for Each Category
plt.figure(figsize=(16, 10), dpi=80, facecolor='w', edgecolor='k')

for i, genre in enumerate(genres):
    plt.scatter('numberTournaments', 'totalOverall',
                data=prizeTournaments.loc[prizeTournaments.genre == genre, :],
                s=400, c=colors[i], label=str(genre))

# Decorations
plt.xlabel('Tournaments', fontsize=16)
plt.ylabel('Prize pool millions US$', fontsize=16)

plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.title("Scatterplot of Tournaments vs Prize pool", fontsize=22)
plt.legend(fontsize=16)
plt.show()


#=============================================================================#
# plot12 - popular genres by number of players
# Prepare Data
playersGenres = gamesRankings.groupby('genre').sum().reset_index()

# Draw plot
fig, ax = plt.subplots(figsize=(16, 10), dpi=80)
ax.vlines(x=playersGenres.index, ymin=0, ymax=playersGenres.numberPlayers,
          color='#ff1200', alpha=0.7, linewidth=2)
ax.scatter(x=playersGenres.index, y=playersGenres.numberPlayers,
           s=75, color='firebrick', alpha=0.7)

# Title, Label, Ticks and Ylim
ax.set_title('Number of players for genres', fontdict={'size': 22})
plt.ylabel('Number of players', fontsize=16)
ax.set_xticks(playersGenres.index)
ax.set_xticklabels(playersGenres.genre, rotation=60, fontdict={
                   'horizontalalignment': 'right', 'size': 12})
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.show()


#=============================================================================#
# plot13 - offline and online performances

onlineTournamentsMinus = onlineTournaments.assign(
    results=lambda x: x.results*-1)

offOnPerformance = pd.merge(
    offlineTournaments, onlineTournamentsMinus, how='inner', on='playerID')
offOnPerformance = offOnPerformance[['results_x', 'playerID', 'results_y']]
offOnPerformance = offOnPerformance.rename(
    columns={"results_x": "offline", "results_y": "online"})
offOnPerformance = offOnPerformance.melt(id_vars=[
    'playerID'], value_vars=['offline', 'online'])

top5offline = offOnPerformance[offOnPerformance.variable == 'offline'].sort_values(
    by='value')['playerID'][-5:].tolist()
top5online = offOnPerformance[offOnPerformance.variable == 'online'].sort_values(
    by='value')['playerID'][:5].tolist()
toplist = top5offline + top5online

offOnPerformance = offOnPerformance[offOnPerformance.playerID.isin(toplist)]

# Draw Plot
plt.figure(figsize=(13, 10), dpi=80)
group_col = 'variable'
colors = ['#f73a18', '#1a2139']

for c, group in zip(colors, offOnPerformance[group_col].unique()):
    sns.barplot(x='value', y='playerID',
                data=offOnPerformance.loc[offOnPerformance[group_col] == group, :], color=c, label=group)

# Decorations
plt.xlabel("Number of tournaments", fontsize=16)
plt.ylabel("")
plt.yticks(fontsize=16)
plt.title("Tournament earnings", fontsize=22)
plt.xticks(fontsize=16)
plt.legend(fontsize=14)
plt.show()


#=============================================================================#
# plot14 - tournament stats
meanMedianPlayers = statsHistory[[
    'year', 'meanEarningsPlayers', 'medianEarningsPlayers']].sort_values('year')
meanMedianPlayers = meanMedianPlayers[meanMedianPlayers.year < 2020]

# Define the upper limit, lower limit, interval of Y axis and colors
mycolors = ['#f73a18', '#1a2139']

# Draw Plot and Annotate
fig, ax = plt.subplots(1, 1, figsize=(16, 9))

columns = meanMedianPlayers.columns[1:]
for i, column in enumerate(columns):
    plt.plot(meanMedianPlayers.year,
             meanMedianPlayers[column].values, lw=1.5, color=mycolors[i], ls='solid')

# Decorations
ax.legend(['Mean Earnings/Player', 'Median Earnings/Player'], fontsize=14)
plt.title('Mean and median earnigns per player', fontsize=22)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel("Year", fontsize=16)
plt.ylabel("US$", fontsize=16)
plt.grid(alpha=.4)
plt.show()


#=============================================================================#
# plot15 - tournament stats
meanMedianTourn = statsHistory[[
    'year', 'meanTournamentPrizePool', 'medianTournamentPrizePool']].sort_values('year')
meanMedianTourn = meanMedianTourn[meanMedianTourn.year < 2020]

# Define the upper limit, lower limit, interval of Y axis and colors
mycolors = ['#f73a18', '#1a2139']

# Draw Plot and Annotate
fig, ax = plt.subplots(1, 1, figsize=(16, 9))

columns = meanMedianTourn.columns[1:]
for i, column in enumerate(columns):
    plt.plot(meanMedianTourn.year,
             meanMedianTourn[column].values, lw=1.5, color=mycolors[i])


# Decorations
ax.legend(['Mean Prize pool/Tournament',
           'Median Prize pool/Tournament'], fontsize=14)
plt.title('Mean and median prize pools per tournament', fontsize=22)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel("Year", fontsize=16)
plt.ylabel("US$", fontsize=16)
plt.grid(alpha=.4)
plt.show()
