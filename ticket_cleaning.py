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

# It looks like everything worked out well, except the Trail Blazers got cut to 
# just Trail. Let's fix that 
events.loc[events['away_team'].str.contains('Trail', case = False), 'away_team'] = "Trail Blazers" 

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

# I want to add a column that summarizes the section by its level, i.e. level 
# in the arena. First, I want to get a general idea of all the different section 
# categories
events['section_name'].unique()

# It looks like a lot of the tickets are related to Club, Suite, Loge and other 
# high-end tickets. We don't want these.  I'll map these to two categories - 
# Club, and Courtside. 
events.loc[events['section_name'].str.contains('Club|Suite|Premier|Loge|lounge|box', case = False), 'level'] = "club" 

# See what remaining sections are left
events[events['level'] != 'Club']['section_name'].unique()

# Courtside and floor tickets are next
events.loc[events['section_name'].str.contains('courtside|floor' , case = False), 'level'] = "courtside" 

# See what is remaining
events[events['level'].isnull()]['section_name'].unique()

# It looks like most sections have numbers with them. I'm going to roughly create
# categories called Upper, Mid, Lower which will correspond to numbers 300+, 200-299,
# and 0-199, respectively
events.loc[events['section_name'].str.contains('3[0-9][0-9]|4[0-9][0-9]|5[0-9][0-9]'), 'level'] = 'upper'
events.loc[events['section_name'].str.contains('2[0-9][0-9]'), 'level'] = 'middle'
events.loc[events['section_name'].str.contains('[0-9][0-9]|1[0-9][0-9]'), 'level'] = "lower"

# Let's see what values didn't get mapped to one of the above levels
events[events['level'].isnull()]['section_name'].unique()


events_of_interest = events[events['listing_price'] < 150]

events.to_csv('C://MyStuff/DataScience/Projects/TicketAnalysis/events_clean.csv', index = False)

events_of_interest.to_csv('C://MyStuff/DataScience/Projects/TicketAnalysis/events_of_interest.csv', index = False)