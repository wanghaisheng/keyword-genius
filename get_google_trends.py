import csv
from pytrends.request import TrendReq

def download_trends_data(keywords, timeframe, geo):
    pytrends = TrendReq(hl='en-US', tz=360)

    # Set the keywords, timeframe, and geo parameters
    pytrends.build_payload(keywords, timeframe=timeframe, geo=geo)

    # Get the interest over time data
    interest_over_time_df = pytrends.interest_over_time()

    # Save the data to a CSV file
    output_file = 'trends_data.csv'
    interest_over_time_df.to_csv(output_file, index=True)

    print(f"Trends data downloaded and saved to {output_file}")

# Example usage:
keywords = ['keyword1', 'keyword2', 'keyword3']
timeframe = 'today 1-m'  # Modify the timeframe as per your requirements
geo = 'US'  # Modify the geographic location as per your requirements

download_trends_data(keywords, timeframe, geo)
