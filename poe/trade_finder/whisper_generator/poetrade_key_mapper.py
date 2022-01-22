import bs4
import pandas as pd

LEAGUE = "Scourge"
if __name__ == "__main__":
    with open("exchange.html") as f:
        soup = bs4.BeautifulSoup(f.read())
    df = pd.Series()
    for tag in soup.select("[data-id]"):
        try:
            data_id, name = tag["data-id"], tag.get("title")
            if not name:
                name = tag.get("data-original-title")
            df[name] = data_id
            print(data_id, name)
        except:
            raise
    df = df.reset_index()
    df.columns = ["name", "key"]
    df = df.set_index("key")
    df.to_csv("poe_keys.csv")
