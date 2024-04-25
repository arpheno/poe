import requests
from requests.exceptions import ChunkedEncodingError, RequestException

from poe_secrets import ssid


def make_request(url, headers=None,data={}):
    try:
        response = requests.post(url, headers=headers,json=data)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX, 5XX)
        print(f"Successful response from {url}")
        print("Status Code:", response.status_code)
        # print("Response Body Snippet:", response.text[:500])  # Print the first 500 characters of the response
        return response
    except ChunkedEncodingError as e:
        print("Chunked Encoding Error:")
    except RequestException as e:
        print("HTTP Request failed:", e)
    except Exception as e:
        print("An error occurred:")
    return None


def main():
    # Base URL of the Path of Exile API
    base_url = "https://www.pathofexile.com"
    # Path specific to your request
    # endpoint_path = "api/trade/data/stats"
    endpoint_path = f"api/trade/exchange/necropolis"
    # URL of the actual API endpoint

    query = {
        'engine':'new',
        "status": {"option": "online"},
        "query": {
            "have": ["chaos"],
            "want": ["orb-of-horizons"],
            "minimum": 100,
        }
    }
    api_url = f"{base_url}/{endpoint_path}"
    # URL of your proxy server, adjust the port/path as needed
    proxy_url = f"http://localhost:8999/{endpoint_path}"

    # Optional: Headers, if required by the API
    headers = {
        "authority": "www.pathofexile.com",
        'accept': '*/*',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6,pl;q=0.5,sl;q=0.4',
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        'cookie': f'cf_clearance=jwZmq02SAhIZjXQQRU4oWAdyF2pA2lR0gz7vpMFxOt0-1654637582-0-150; POESESSID={ssid}',
        'dnt': '1',
        'origin': 'https://www.pathofexile.com',
    }

    # print("Making direct request to the API...")
    # direct_response = make_request(api_url, headers=headers,data=query)

    print("\nMaking request through the proxy...")
    for i in range(10):
        proxy_response = make_request(proxy_url, headers=headers,data=query)

    # Comparing both responses if both were successful


if __name__ == "__main__":
    main()
