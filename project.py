#!/usr/bin/env python
# coding: utf-8

import requests #for api
import pandas as pd #for dataframe
import sys #for reading parameters when running script
import json #for api

#port in csv file
orig_df = pd.read_csv("Customer Support Engineer Take Home Project - Import File - MOCK_DATA.csv")

#capitalize each word in these columns
def capWords(df):
    df[['Company', 'Contact Name','Company US State']] = df[['Company', 'Contact Name','Company US State']].astype(str).applymap(lambda x: x.title())
    return df

###########################
#         PART I          #
###########################

#group by Company and uppercase the values
df1 = capWords(orig_df).groupby("Company")

#make a dictionary to store each contacts and their associated companies
result = {}
for company_name, group in df1:
    contacts = group[["Contact Name", "Contact Phones", "Contact Emails"]].to_dict(orient="records")
    result[company_name] = contacts

# Set the API endpoint URL and headers
url = "https://api.close.com/api/v1/lead/"
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'api_3ichhEjxpgKmoAH3spHda6.0tdki5JTWKV9iiEooXALxe'
}

#convert dataframe to json
json_data = json.dumps(result)

#post the change
response = requests.post(url, json=json_data, headers=headers)

#display reponse code and data
print(response.status_code)
print(response.json())


###########################
#         PART II         #
###########################

#assign value to parameters 
start_date = pd.to_datetime(sys.argv[1])
end_date = pd.to_datetime(sys.argv[2])

#drop rows with null values in these columns
#only these 4 were used in the report, so I decided to only drop rows with null values in these columns
#then capitalize words
df2 = orig_df.copy().dropna(subset=['Company','custom.Company Founded','custom.Company Revenue','Company US State'])
df2 = capWords(df2)

#change to date format for Comany Founded
df2['custom.Company Founded'] = pd.to_datetime(df2['custom.Company Founded'], format='%d.%m.%Y')

# change revenue column to float
df2['custom.Company Revenue'] = df2['custom.Company Revenue'].apply(lambda x: float(x.replace('$','').replace(',',''))if isinstance(x, str) else x)

#create new table with date filter
df2 = df2[(df2['custom.Company Founded'] >= start_date) & (df2['custom.Company Founded'] <= end_date)].copy()

# group the rows by US State
state_groups = df2.groupby('Company US State')

# create the report according to the spec 
state_df = pd.DataFrame({
    'state_name': state_groups['Company US State'].first(),
    'total_leads': state_groups.size(),
    'lead_with_most_revenue': state_groups.apply(lambda x: x.loc[x['custom.Company Revenue'].idxmax(), 'Company']),
    'total_revenue': state_groups['custom.Company Revenue'].sum(),
    'median_revenue': state_groups['custom.Company Revenue'].median()
}).reset_index(drop=True)

# sort the dataframe by total_revenue in descending order
state_df = state_df.sort_values('total_revenue', ascending=False).reset_index(drop=True)

# change the total_reveue and median_revenue to show as currency value format  
for col in ['total_revenue','median_revenue']:
    state_df[col] = state_df[col].apply(lambda x: "${:,.2f}".format(round(x, 2)))

#writes a csv file
state_df.to_csv('output.csv', index=False, sep='\t', header=True)

