import pandas as pd
import numpy as np
import glob as glob
import itertools

files = glob.glob("D://TicketData/*.csv")

events = pd.DataFrame()

for file in files:
    event = pd.read_csv(file, encoding = 'latin1')
    events = events.append(event)


# First I'll remove the duplicates from the data set
events = events.drop_duplicates()

# It looks like there are some NaN values in the seatNumbers variable
# Let's look at this by itself and get an idea
events['seatNumbers']

# change the nan values in seatNumbers into ""
events['seatNumbers'] = events['seatNumbers'].fillna("")

# One this I want to do is take the date component of the eventtitle column 
# and make a column for it
events['split'] = events['eventtitle'].str.split(' ')

# Make the first element in the split column the event_date
events['event_date'] = events['split'].str.get(0)

# Make a home_team column
events['home_team'] = events['split'].str.get(1)

# Make an away_team column
events['away_team'] = events['split'].str.get(3)

# Now let's get rid of all the columns we don't need
events = events.drop(['split', 'eventtitle'], axis = 1)

# Let's clean the event_date column a little more
events['event_date'] = events['event_date'].str.replace('.', '/')

# Add year to date
events['event_date'] = events['event_date'] + '/18' 

seats = pd.DataFrame(events['seatNumbers'].str.split(',').tolist(), index = events['listingId']).stack().reset_index().drop('level_1', axis = 1)

events = pd.merge(left = events, right = seats, left_on = 'listingId', right_on = 'listingId')
events = events.drop('seatNumbers', axis = 1)

# Remove dupliclates
events = events.drop_duplicates()

# Reset index
events = events.reset_index()

# Rename columns
events.columns = ['index', 'listing_id', 'quantity', 'row', 'section_name', 'current_price',
                  'listing_price', 'event_date', 'home_team', 'away_team', 'seat_number']


# Reorder column
events = events[['listing_id', 'home_team', 'away_team', 'event_date' ,'quantity', 'row', 'seat_number', 
                'section_name', 'current_price', 'listing_price']]

# Create a column that is the percentage increase from listing_price to current_price
events['price_change'] = (events['current_price'] - events['listing_price']) / events['listing_price']

# Change dtypes
events[['quantity', 'current_price', 'listing_price', 'price_change']] = events[['quantity', 'current_price', 'listing_price', 'price_change']].apply(pd.to_numeric)

# event_date to datetime
events['event_date'] = pd.to_datetime(events['event_date'])

# listing_id to character
events['listing_id'] = events['listing_id'].astype('str')


events.to_csv('C://MyStuff/DataScience/Projects/TicketAnalysis/events_clean.csv')