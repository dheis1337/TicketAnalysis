import matplotlib as plt
import pandas as pd
import numpy as np
import os


# set working directory
os.chdir('C:/MyStuff/DataScience/Projects/TicketAnalysis')

# read in event data
events = pd.read_csv('events_clean.csv')

# check info
events.info()

# change listing_id to character
events['listing_id'] = events['listing_id'].astype('str')

# View a random subset of the data to 
events.sample(n = 100)


# Number of listings per team
listings_per_team = events['home_team'].value_counts()

# Number of listings per event per team
listings_per_event = events.groupby('home_team')['event_date'].value_counts()

# Number of listings per section per team
listings_per_section = events.groupby('home_team')['section_name'].value_counts()

# Mean of listing_price, current_price, price_change per team
events.groupby('home_team')[['listing_price', 'current_price', 'price_change']].mean()

# Quantiles of listing_price, current_price, per team
price_quants_by_team = events.groupby('home_team')['listing_price', 'current_price', 'price_change'].quantile([.25, .5, .75])

# add the change between listing_price and current_price for each quantile for above df
price_quants_by_team['quant_price_change'] = ((price_quants_by_team['current_price'] - price_quants_by_team['listing_price']) / 
                                        price_quants_by_team['listing_price'])
                                        
# Quantiles of current_price, listing_price, price_change by team
events[['home_team', 'current_price', 'listing_price']].plot(kind = 'hist', subplots = 'True')

# Density of current_price and listing_price for each team
events.groupby('home_team')['current_price', 'listing_price'].plot(kind = 'kde', xlim = [-100, 250])
                                                                 

# Let's look at the data grouped by home_team, then away_team to get an idea
# of how the average price change varies
events.groupby(['home_team', 'away_team'])['price_change'].mean().nlargest(15)


# Let's look at price data by the level now
events.groupby(['level'])['current_price', 'listing_price'].describe()


events[events['level'] == 'Upper'][['current_price', 'listing_price']].plot(kind = 'kde', xlim = [-10, 1500])

events[events['listing_price'] > 1400]