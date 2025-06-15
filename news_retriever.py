from apify_client import ApifyClient
import json

class NewsRetriever:
    def __init__(self):
        self.apify_client = self._client_init()
        self.retrieved_news = []

    def _client_init(self):
        with open("tokens.json", "r") as file:
            tokens = json.load(file)
        
        return ApifyClient(token = tokens["apify_token"])

    def fetch_news(self, start_date, result_count="30"):

        start_urls = [
            {
                "url": "https://twitter.com/financialjuice",
                "method": "GET"
            }
        ]

        run_input = {
            "start_urls": start_urls,
            "since_date": start_date,
            "result_count": result_count,
        }

        run = self.apify_client.actor("2dZb9qNraqcbL8CXP").call(run_input=run_input)

        # Fetch and print Actor results from the run's dataset (if there are any)
        for item in self.apify_client.dataset(run["defaultDatasetId"]).iterate_items():

            if not item.get("full_text"):
                continue

            news_item = {
                "timestamp": item.get("created_at", "No timestamp parsed"),
                "author": item.get("user", {}).get("name", "No author parsed"),
                "text": item.get("full_text"),
            }

            self.retrieved_news.append(news_item)
        
        return self.retrieved_news

if __name__ == "__main__":
    retriever = NewsRetriever()
    retriever.fetch_news()