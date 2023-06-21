import csv
from googlesearchconsole import GoogleSearchConsole

def download_search_console_data(keywords, start_date, end_date):
    # Set up Google Search Console API client
    gsc = GoogleSearchConsole('credentials.json')  # Replace with your credentials file path

    # Define the desired search console fields
    fields = ['date', 'query', 'page', 'country', 'device', 'clicks', 'impressions', 'ctr', 'position']

    # Fetch search console data for the specified keywords and date range
    data = gsc.query(
        keywords=keywords,
        start_date=start_date,
        end_date=end_date,
        dimensions=['date', 'query', 'page', 'country', 'device'],
        row_limit=-1  # Fetch all available rows
    )

    # Save the data to a CSV file
    output_file = 'search_console_data.csv'
    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

    print(f"Search Console data downloaded and saved to {output_file}")

# Example usage:
keywords = ['keyword1', 'keyword2', 'keyword3']
start_date = '2022-01-01'  # Modify the start date as per your requirements
end_date = '2022-12-31'  # Modify the end date as per your requirements

download_search_console_data(keywords, start_date, end_date)
