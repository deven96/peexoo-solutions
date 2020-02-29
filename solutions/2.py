"""
Question
---------
Fetch data from a currency Api and Store the result in a .csv file API: https://fixer.io/quickstart
"""
import os
import urllib.request
import json

# usually kept a secret but since it's a free api ...
apikey = "276eb329d3dc022dfffb90384b016078"
fixerUrl = f"http://data.fixer.io/api/latest?access_key={apikey}"
main_dir = os.path.dirname(os.path.dirname(__file__))
processed_assets = os.path.join(main_dir, "assets", "processed")

def getResponse(url:str) -> dict:
    """
    Parse a json response from an endpoint
    """
    operUrl = urllib.request.urlopen(url)
    if(operUrl.getcode()==200):
        data = operUrl.read()
        # load it into a json object
        jsonData = json.loads(data)
    else:
        print("Error receiving data ", operUrl.getcode())
    return jsonData

def csvwriter(json_data:dict):
    """
    Converts json data to csv
    """
    timestamp = json_data["timestamp"]
    base = json_data["base"]
    rates = json_data["rates"]
    # save csv using timestamp
    currency_csv = os.path.join(processed_assets, f"currency-{base}-{str(timestamp)}.csv")
    with open(currency_csv, "w") as f:
        f.write("Index, Currency, Rate\n")
        for index, key in enumerate(rates.keys()):
            f.write(f"{index+1}, {key}, {rates[key]}\n")
    print(f"Saved currency information to {currency_csv}")


if __name__=="__main__":
    json_data = getResponse(fixerUrl)
    csvwriter(json_data)