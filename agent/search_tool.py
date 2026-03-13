import requests

# Simple web search tool using DuckDuckGo's API
def search_web(query):

    url = "https://duckduckgo.com/?q=" + query.replace(" ", "+") + "&format=json"

    try:
        response = requests.get(url)
        return response.text[:2000]  # limit response to 2000 characters
    except Exception as e:
        return str(e)