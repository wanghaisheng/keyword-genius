from google.auth import exceptions
from google.ads.google_ads.client import GoogleAdsClient

def download_keyword_data(keyword_list, output_file):
    # Set up Google Ads API client
    try:
        client = GoogleAdsClient.load_from_storage()
    except exceptions.GoogleAuthError as ex:
        print(f"Google Ads API authentication failed: {ex}")
        return
    
    # Create a query to retrieve keyword data
    query = f"""
        SELECT
          keyword_view.resource_name,
          keyword_view.keyword.text,
          keyword_view.keyword.match_type,
          keyword_view.search_term_view.search_term,
          keyword_view.search_term_view.keyword_match_type,
          keyword_view.average_cpc.micro_amount,
          keyword_view.average_monthly_searches
        FROM
          keyword_view
        WHERE
          keyword_view.keyword.text IN ({','.join([f"'{kw}'" for kw in keyword_list])})
        """

    try:
        # Issue a search request
        response = client.service.google_ads.search(query=query)
        
        # Extract data from the response and write to CSV
        with open(output_file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Keyword', 'Match Type', 'Search Term', 'Search Term Match Type', 'Average CPC', 'Average Monthly Searches'])
            
            for row in response:
                keyword = row.keyword_view.keyword.text
                match_type = row.keyword_view.keyword.match_type
                search_term = row.keyword_view.search_term_view.search_term
                term_match_type = row.keyword_view.search_term_view.keyword_match_type
                avg_cpc = row.keyword_view.average_cpc.micro_amount / 1e6
                avg_monthly_searches = row.keyword_view.average_monthly_searches
                
                writer.writerow([keyword, match_type, search_term, term_match_type, avg_cpc, avg_monthly_searches])
        
        print(f"Keyword data downloaded and saved to {output_file}")
    
    except Exception as ex:
        print(f"An error occurred: {ex}")

# Example usage:
keywords = ['keyword1', 'keyword2', 'keyword3']
output_file = 'keyword_data.csv'
download_keyword_data(keywords, output_file)
