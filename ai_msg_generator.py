from abc import ABC, abstractmethod
import google.generativeai as genai
import json


class AIMessageGenerator(ABC):
    @abstractmethod
    def generate_message(self, stocks, news) -> str:
        """Generate a message based on stock data."""
        pass

class Gemini(AIMessageGenerator):
    def __init__(self, model_name="gemini-2.0-flash"):
        self.model = self._model_init(model_name)
    
    def _model_init(self, model_name):

        with open("tokens.json", "r") as file:
            tokens = json.load(file)
        genai.configure(api_key=tokens["google_gemini"])

        return genai.GenerativeModel(model_name=model_name)

    def generate_message(self, stocks, news) -> str:

        prompt = f"Generate a message about episodic pivots of following stocks. "
       
        prompt += f"Please follow following rules:\n"
        prompt += f"1. The output should be at the format for discord webhook\n"
        prompt += f"2. Correlate with the provided news. If none of the news is relevant, "
        prompt += f"just output the stock data without any news correlation.\n"
        prompt += f"3. Title should just be the ticker.\n"
        prompt += f"4. There could be multiple related news. Pick the top 3 if applicable\n"
        prompt += f"5. Watch for the indentation for bullet points in the news correlation.\n"
        prompt += f"6. Limit the stocks to 10 for the restriction of discord. Pick the most "
        prompt += f"relevant ones with huge opportunity to call or put"

        prompt += f"Example output:\n"
        example_output = {
            "embeds": [
                {
                    "title": "MSFT",
                    "fields": [
                        {
                            "name": "Price",
                            "value": "$478.73",
                            "inline": True
                        },
                        {
                            "name": "Volume",
                            "value": "2,015,273",
                            "inline": True
                        },
                        {
                            "name": "Yesterday's High",
                            "value": "$473.25",
                            "inline": True
                        },
                        {
                            "name": "Today's Open",
                            "value": "$469.68",
                            "inline": True
                        },
                        {
                            "name": "Potential News Correlation - Top 3",
                            "value": """1. Wed Jun 11 04:29:11 +0000 2025 FinancialJuice French watchdog likely to rule on Qwant request by September and on whether to begin Microsoft probe, according to a source.
                                        2. Timestamp Author Test message for discord webhook.""",
                            "inline": False
                        }
                    ],
                    "color": 3447003
                }
            ]
        }
        prompt += f"{json.dumps(example_output, indent=2)}\n"

        prompt += f"Here are the stocks:\n"
        for ticker, stock in stocks.items():
            prompt += f" - {ticker}: current price {stock.cur_price}, current volume {stock.cur_vol}, "
            prompt += f"yesterday highest price {stock.prev_high}, today open price {stock.open_price}\n"

        prompt += f"Here are the news:\n"
        for n in news:
            prompt += f" - {n['timestamp']}: {n['author']} - {n['text']}\n"
        
        response = self.model.generate_content(prompt)
        
        return response.text