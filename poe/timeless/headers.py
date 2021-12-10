from constants import ssid

cookies = {
    "cf_clearance": "7d322aa725fafce9ef1ebc8a26759033b127dd7f-1618777267-0-150",
    "_ga": "GA1.2.1675387988.1618777334",
    "stored_data": "1",
    "POESESSID": ssid,
    "_gid": "GA1.2.1879284383.1636797311",
}
headers = {
    "Pragma": "no-cache",
    "Origin": "https://www.pathofexile.com",
    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6,pl;q=0.5,sl;q=0.4",
    "Sec-WebSocket-Key": "e5K704b5btGaJGoJ0Do+XA==",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
    "Upgrade": "websocket",
    "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
    "Cache-Control": "no-cache",
    "Connection": "Upgrade",
    "Sec-WebSocket-Version": "13",
    "Cookie": "; ".join(f"{key}={value}" for key, value in cookies.items()),
}