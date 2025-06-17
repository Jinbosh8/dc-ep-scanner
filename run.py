#!/usr/bin/env python3
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from stock_scanner import StockScanner, StockQueryClient
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from news_retriever import NewsRetriever
from ai_msg_generator import Gemini
from dc_msg_sender import dc_send_msg
import json
import re
import time

prev_high_and_open_price_updated = False

def get_latest_time_window_utc(interval_mins=15):

    cur_utc = datetime.now(timezone.utc)
    end_utc = cur_utc - timedelta(minutes=16) # api only allows querying data from 15 minutes ago
    start_utc = end_utc - timedelta(minutes = interval_mins)
    
    return start_utc, end_utc, TimeFrame(interval_mins, TimeFrameUnit.Minute)

def floor_to_15_minutes(dt):
    return dt - timedelta(minutes = dt.minute % 15, \
        seconds = dt.second, microseconds = dt.microsecond)

def clean_gemini_msg(ai_msg):

    match = re.search(r'```json\s*(\{.*\})\s*```', ai_msg, re.DOTALL)
    if match:
        extracted_json_str = match.group(1)

        try:
            real_json_object = json.loads(extracted_json_str)

        except json.JSONDecodeError as e:
            print(f"Error decoding the inner JSON: {e}")
            print("Problematic string segment:")
            print(fixed_json_str)

    else:
        print("Failed to parse message from gemini")

    return real_json_object

def main():

    print("Hello~ EP scanner starts running!")

    stock_query_client = StockQueryClient()
    stock_scanner = StockScanner()

    gemini = Gemini()
    news_retriever = NewsRetriever()

    global prev_high_and_open_price_updated

    # long running process
    while True:

        cur_est = datetime.now(timezone.utc).astimezone(ZoneInfo("America/New_York"))

        if cur_est.weekday() >= 5:
            print(cur_est.strftime("%Y-%m-%d %H:%M:%S %Z") + " Sleep 60min")
            time.sleep(3600)  # Sleep for 1 hour if it's weekend
            continue

        rounded_time = floor_to_15_minutes(cur_est)

        # update previous high and open price for all stocks when the market is open
        if rounded_time.hour == 9 and rounded_time.minute == 30:
            prev_high_and_open_price_updated = False

            # update tickers on every Monday
            if rounded_time.weekday == 0:
                tickers = stock_scanner.get_all_tickers(stock_query_client)
                stock_scanner.stock_init_all

        if not prev_high_and_open_price_updated:
            print(f"Updating previous high and open price for all stocks at {rounded_time}")
            stock_scanner.update_prev_high_and_open_price_all(stock_query_client)
            prev_high_and_open_price_updated = True

        # filter ep stocks every 15 minutes while the market is open
        if (rounded_time.hour >= 10) and \
           (rounded_time.hour < 16 or (rounded_time.hour == 16 and rounded_time.minute == 0)):

            start_utc, end_utc, timeframe = get_latest_time_window_utc()
            print(f"Filtering latest stocks from {start_utc} to {end_utc}, Interval: {timeframe}")
            stock_scanner.filter_latest_stock(stock_query_client, start_utc, end_utc, timeframe)

            # check if any ep stocks are available
            if stock_scanner.cur_ep_stocks:
                print("Found episodic pivot stocks. Generating messages...")
                news = news_retriever.fetch_news(start_date=start_utc.strftime("%Y-%m-%d"))
                ai_msg = gemini.generate_message(stock_scanner.cur_ep_stocks, news)

                dc_msg = clean_gemini_msg(ai_msg)
                dc_send_msg(dc_msg)

        print(cur_est.strftime("%Y-%m-%d %H:%M:%S %Z") + " Sleep 15min")
        time.sleep(900)


if __name__ == "__main__":
    main()
    