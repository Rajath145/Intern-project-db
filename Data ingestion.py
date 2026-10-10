import os
import pandas as pd
from apify_client import ApifyClient
from tavily import TavilyClient

def ingest_macro_data(apify_token, tavily_api_key):
    apify_client = ApifyClient(apify_token)
    run_input = {
        "days": 180, "countries": ["us"]
                 }
    actor_call = apify_client.actor("parseforge/investing-com-economic-calendar-scraper").call(run_input=run_input)
    macro_records = [ 
        {
           "timestamp": item.get("date"),
           "event_name": item.get("title"),
            "actual": item.get("actual"),
            "forecast": item.get("forecast"),
            "previous": item.get("previous"),
         }
    for item in apify_client.dataset(actor_call["defaultDatasetId"]).iterate_items()
    ]
    df_macro = pd.DataFrame(macro_records)
    tavily_client = TavilyClient(api_key=tavily_api_key)
    news_response = tavily_client.search(
        query="FOMC CPI macroeconomic policy sentiment impact", 
        max_results=10
    )
    
    news_records = []
    for result in news_response.get("results", []):
        news_records.append({
            "published_at": result.get("published_date"),
            "title": result.get("title"),
            "content": result.get("content")
        })
    df_news = pd.DataFrame(news_records)
    
    return df_macro, df_news