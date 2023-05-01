# CloseProject
This project is for Customer Support Engineer take home project as part of the interview process. 
Included with a CSV that has information on companies, contacts, phone numbers, emails, company founded date, revenue, US state.

## Part I: Import Leads to Close from a CSV file

Using the companies and contacts (leads) from the CSV file and convert them into an acceptable format to transmit via API. This allows an automated process to upload leads to Close platform all at once.

**Ths part will likely give 402 authorization error, I think the issue may be the header** 😕

The script should:
- group the csv data by Company
- iterate the data to create a dictionary that will have contacts for each company
- convert the dictionary into a format acceptable to transmit via API
- import to Close using API and provide the response code and leads

## Part II: Create Report from a CSV file

Using the companies, company founded date, revenue and US state to create a report in csv file format. The report categorized the companies by state and shows these info for each state:
- how many companies
- company that has highest revenue 
- total revenue 
- median revenue 

Here's what the script does:
- load CSV file
- remove null values in these columns because only these were used in the report
    - Comapny, Company Founded, Revenue and US State
- corrected the datatype for Revenue (float) and Company Founded (datetime)
- filter for the date range
- group the rows by US State column
- creat new table/report following the requirements
- sort it in descending order of revenue 
- format the Revenue columns with $ and , separators
- create the report as a csv file


## Running the Script
- download the csv file and the python file
- run the script in the terminal with date parameters, example format:
     <pre><code>python.py 1920-01-01 2020-01-01 </code></pre>
This should import all the leads to Close, then create a csv file in the folder between the date range.
