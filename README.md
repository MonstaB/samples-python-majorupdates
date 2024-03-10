# Major updates will explain later.
The Odds API provides live odds for loads of sports from bookmakers around the world, in an easy to use JSON format.

Before getting started, be sure to get a free API key from [https://the-odds-api.com](https://the-odds-api.com)

For more info on the API, [see the docs](https://the-odds-api.com/liveapi/guides/v4/)

```
python main.py --api-key YOUR_API_KEY
```
Ths will
- use list of sports from sports/my_sports_keys
- Print events and odds for the next upcoming games (across sports in file)
- Dumps a .json file in Json_files/ for each sport wil all selected markets for all selected regions
- Requests used & remaining for your api key

To change setting look in config.cfg



### The Odds API Code Samples (v4) - Python

The Odds API provides live odds for loads of sports from bookmakers around the world, in an easy to use JSON format.

Before getting started, be sure to get a free API key from [https://the-odds-api.com](https://the-odds-api.com)

For more info on the API, [see the docs](https://the-odds-api.com/liveapi/guides/v4/)


### Get Started

```
python odds.py --api-key YOUR_API_KEY
```

This will print:
- A list of in-season sports
- Events and odds for the next 8 upcoming games (across all sports)
- Requests used & remaining for your api key

To change the sport, region and market, see the parameters specified at the beginning of odds.py

Make sure the requests library is installed `pip install requests`


---


### Using Docker (Mac and Linux)
#### *Dont know if this still works**
Build the image

```
docker build -t theoddsapi/sample:latest .
```

Run the python script in the container

```
docker run -t -i --rm -v "$(pwd)":/usr/src/app/ theoddsapi/sample:latest python odds.py --api-key YOUR_API_KEY
```
