import pandas as pd    
import boto3
import io


# Create key, key secret, and bucket_name
AWS_ACCESS_KEY_ID = 'AKIAJXPNC6JIDI5JXSJQ'
AWS_ACCESS_KEY_SECRET = '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'

# Create session connection
session = boto3.Session(AWS_ACCESS_KEY_ID, AWS_ACCESS_KEY_SECRET)
conn = session.resource('s3')

# Find all the bucket names on the s3 server
buckets = [bucket.name for bucket in conn.buckets.all()]


# Create a client  to download data
client = boto3.client('s3', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_ACCESS_KEY_SECRET)

# initiate empty data frame to populate data
events = pd.DataFrame()


def read_s3(bucket):
    """ This function creates a bucket connection, finds all the files in that 
    bucket, and then pulls the data from each .csv file into the df data frame - 
    this data frame represents the data that is in each file in the s3 bucket. Then
    the date_scraped column is added using the information in the file. Finally, 
    the events data frame is appended to. This function will be used in the build_df
    function to build a data frame of all the files in all the buckets.""" 

    buck = conn.Bucket(bucket)
    files = [object.key for object in buck.objects.all()]
    for file in files:
        obj = client.get_object(Bucket = buck.name, Key = file)
        df = pd.read_csv(io.BytesIO(obj['Body'].read()), encoding = 'latin1')
        df['date_scraped'] = file[-10:len(file)]
        global events 
        events = events.append(df)  
    return events

# initiate data frame that will hold all of the ticket data across all buckets
tickets = pd.DataFrame()

def build_df(buckets):
    """ This function uses the read_s3 function to read all the data from each 
    s3 bucket into a data frame. The duplicates are then dropped and then the
    tickets data frame is appended. This data frame represents all the ticket data
    in all of the buckets."""
    global tickets
    bucket_events = read_s3(buckets)
    bucket_events = bucket_events.drop_duplicates()
    tickets = tickets.append(bucket_events)
    return tickets

# map the build_df across the buckets object
list(map(build_df, buckets))

# remove duplicates
tickets = tickets.drop_duplicates()

# save to .csv 
tickets.to_csv('C:/MyStuff/DataScience/Projects/TicketAnalysis/s3_events.csv', index = False)