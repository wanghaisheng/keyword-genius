import csv
import requests
from bs4 import BeautifulSoup

def download_pinterest_search_recommendations(keywords, output_file):
    base_url = 'https://www.pinterest.com'
    search_url = f'{base_url}/search/pins/?q='

    recommendations = []

    for keyword in keywords:
        # Fetch the search page HTML content
        response = requests.get(search_url + keyword)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract search recommendations from the parsed HTML
        recommendation_elements = soup.select('div[data-test-id="typed_query_source_suggestion"]')

        recommendations.extend([recommendation.text.strip() for recommendation in recommendation_elements])

    # Save the recommendations to a CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Keyword', 'Recommendation'])

        for keyword, recommendation in zip(keywords, recommendations):
            writer.writerow([keyword, recommendation])

    print(f"Pinterest search recommendations downloaded and saved to {output_file}")

# Example usage:
keywords = ['keyword1', 'keyword2', 'keyword3']
output_file = 'pinterest_search_recommendations.csv'

download_pinterest_search_recommendations(keywords, output_file)
