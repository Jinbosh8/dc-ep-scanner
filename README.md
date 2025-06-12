# EP Scanner

A lightweight Python tool that monitors Episodic Pivots (EPs) in the U.S. stock market and highlights potentially related news events. It’s designed to help traders stay informed and observe unusual market activity.

## Disclaimer

The tool is for informational purpose only, which can **NOT** be considered as financial advice.

## Features

- Fetch historical stock data via Alpaca API
- Filter EPs based on fetched stock data
- Fetch X posts via Apify API
- Correlate EPs with X posts with Gemini
- Send results to Discord via webhook

## Requirements

- pip packages:
  - `alpaca-py`
  - `apify-client`
  - `google-ai-generative`

## Credits

- This project was inspired by [a post](https://www.xiaohongshu.com/explore/683239820000000021002aa8?secondshare=weixin&share_from_user_hidden=true&appuid=&apptime=1748475846&share_id=6b31a0fac8f7417ebd05ac330f2615f0&xsec_source=h5_share&xsec_token=CB-3jl6VFcF00-nQOkrkttWwUFFeBYHX-I1SKN4y8ISkM=) on RedNote.

- Parts of the filtering logic are adapted from https://qullamaggie.com/
