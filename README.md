### Overview
This is a repository dedicated to a project I'm working on to retrieve ticket 
data for NBA games and determining if there is any resell potential in them. This repository contains a few
important scripts:

#### s3_download.py
This script is dedicated to pulling some ticket data from an Amazon s3 bucket I was
using for the project. 

#### ticket_cleaning.py
This script is dedicated to cleaning the ticket data and getting it into a suitable
from for EDA. This script also contains some code in the beginning for pulling some
ticket data from my computer; the s3 bucket wasn't used for the entireity of the 
project. 

#### event_eda.py
This script is dedicated to conducting the EDA on the cleaned ticket data. 

In addition to the scripts mentioned above there are some important files:

#### events_clean.csv
This file contains all the cleaned ticket data. 

#### events_of_interest.csv
This file contains all cleaned tickets that have a listing price less than $150. 
The reason for this is that because I'm looking at reselling tickets I don't want 
to be investing over $150 into each ticket. This dataset reduces the sample to 
tickets I'd be more likely to invest in. 

#### s3_events.csv
This file contains all the ticket data on the s3 bucket. 

Finally, this repository contains a folder dedicated to some of the visualizations
I created during EDA. 

For a detailed report on this project, check out: 