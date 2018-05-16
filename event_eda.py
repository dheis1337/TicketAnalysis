import matplotlib as plt
import pandas as pd
import numpy as np
import os
import seaborn as sns

sns.set(style = 'whitegrid', color_codes = True)


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

# It looks like there's some outliers in the data. Let's use the events_of_interest 
# csv, which is basically a csv with a limit on the listing_price of 150
events_of_interest = pd.read_csv('C:/MyStuff/DataScience/Projects/TicketAnalysis/events_of_interest.csv')

# Now let's look at the summarizing information of the data broken down by level
events_of_interest.groupby('level')['current_price', 'listing_price'].describe()

# This data looks much better than what we had for some of the values in the events 
# data frame. Now let's visualize some of the density plots for the current_price
# and listing_price for each level
levels_density = events_of_interest.groupby('level')['current_price', 'listing_price'].plot(kind = "kde")

# Save plots
club_density = levels_density[0].get_figure()
lower_density = levels_density[1].get_figure()
middle_density = levels_density[2].get_figure()
upper_density = levels_density[3].get_figure()

# Set some titles
club_density.suptitle('Club Level Density of Current Price and Listing Price')
lower_density.suptitle('Lower Level Density of Current Price and Listing Price')
middle_density.suptitle('Middle Level Density of Current Price and Listing Price')
upper_density.suptitle('Upper Level Density of Current Price and Listing Price')


# Save the figures
club_density.savefig('C:/MyStuff/DataScience/Projects/TicketAnalysis/visualizations/club_density_cprice_lprice.png')
lower_density.savefig('C:/MyStuff/DataScience/Projects/TicketAnalysis/visualizations/lower_density_cprice_lprice.png')
middle_density.savefig('C:/MyStuff/DataScience/Projects/TicketAnalysis/visualizations/middle_density_cprice_lprice.png')
upper_density.savefig('C:/MyStuff/DataScience/Projects/TicketAnalysis/visualizations/upper_density_cprice_lprice.png')

# Now let's change this up slightly and compare the density of current_price and listing_price
# separately, with a density for each level on the plot
events_of_interest.groupby('level')['current_price'].plot(kind = 'kde')



# Create a boxplot of the current_price, listing_price, and price_change by level and then save them
cprice_box = sns.boxplot(x = 'current_price', y = 'level', data = events_of_interest)
cprice_fig = cprice_box.get_figure()
cprice_fig.savefig('C:/MyStuff/DataScience/Projects/TicketAnalysis/visualizations/cprice_boxplot.png')

# Listing price
lprice_box = sns.boxplot(x = 'listing_price', y = 'level', data = events_of_interest)
lprice_fig = lprice_box.get_figure()
lprice_fig.savefig('C:/MyStuff/DataScience/Projects/TicketAnalysis/visualizations/lprice_boxplot.png')

# Price change
pchange_box = sns.boxplot(x = 'price_change', y = 'level', data = events_of_interest)
pchange_fig = pchange_box.get_figure()
pchange_fig.savefig('C:/MyStuff/DataScience/Projects/TicketAnalysis/visualizations/pchange_boxplot.png')


#

   

