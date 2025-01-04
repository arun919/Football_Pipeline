import os
import requests
import pandas as pd


def check_rate_limits():
    """
    Check the API quota allocated to your account
    """
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    daily_limits = response.headers.get('x-ratelimit-requests-limit')
    daily_remaining = response.headers.get('x-ratelimit-requests-remaining')
    calls_per_min_allowed = response.headers.get('X-RateLimit-Limit')
    calls_per_min_remaining = response.headers.get('X-RateLimit-Remaining')
    
    rate_limits = {
        'daily_limit': daily_limits,
        'daily_remaining': daily_remaining,
        'minute_limit': calls_per_min_allowed,
        'minute_remaining': calls_per_min_remaining
    }
    return rate_limits



def get_top_scorer(url,headers,params):
    """
    fetch the top scorers using the API
    """
    try:
        response = requests.get(url,headers = headers,params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as http_error_message:
        print (f"❌ [HTTP ERROR]: {http_error_message}")
    
    except requests.exceptions.ConnectionError as connection_error_message:
        print (f"❌ [CONNECTION ERROR]: {connection_error_message}")
    
    except requests.exceptions.Timeout as timeout_error_message:
        print (f"❌ [TIMEOUT ERROR]: {timeout_error_message}")
    
    except requests.exceptions.RequestException as other_error_message:
        print (f"❌ [UNKNOWN ERROR]: {other_error_message}")


#top = get_top_scorer(url,headers,params)
#print(top)