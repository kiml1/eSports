import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# import data sets
earningsHistory = pd.read_csv('../scrapy/earningsHistory/eSports_players.csv')
earningsCountry = pd.read_csv(
    '../scrapy/earningsByCountry/earningsCountry_players.csv')


# plot1 - countries ranking by total earnings
sns.set(style="whitegrid")
f, ax = plt.subplots(figsize=(6, 15))

countriesRankingEarnings_df = earningsHistory[['country', 'totalYear']]
countriesRankingEarnings = countriesRankingEarnings_df.groupby(
    'country', as_index=False).sum().sort_values('totalYear', ascending=False).head(20)


sns.set_color_codes("pastel")
sns.barplot(x="totalYear", y="country",
            data=countriesRankingEarnings, label="Total", color="b")


# plot2 - eSports earnings by year
plt.figure(figsize=(12, 6))
earningsHistory.groupby('year')['totalYear'].sum().sort_values(
    ascending=True).plot.bar(color='r')

# plot3 - most successful players
plt.figure(figsize=(12, 6))
earningsCountry.sort_values('totalOverall', ascending=False).head(10)

# plot4 - games rank by prize money
plt.figure(figsize=(12, 6))
earningsCountry.groupby('game')['totalOverall'].sum().sort_values(
    ascending=False).head(20).plot.bar(color='r')

# plot5 - top game by year
plt.figure(figsize=(12, 6))
earningsHistory.groupby('year')['totalOverall', 'game']
