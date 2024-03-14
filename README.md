# Major updates will explain later.
The Odds API provides live odds for loads of sports from bookmakers around the world, in an easy to use JSON format.

Before getting started, be sure to get a free API key from [https://the-odds-api.com](https://the-odds-api.com)

For more info on the API, [see the docs](https://the-odds-api.com/liveapi/guides/v4/)

# New Stuff

only works for AU and decimal odds at present

Edit config.cfg to add your Api key,

first run
``get_active_sports.py`` 

This will download all active sports to file active_sports.json 

This will also create two txt files with all sports listed.

edit active_sports_keys.txt, delete all sports you wish to not request

keep one sport per line with no leading or trailing spaces,

Then run  ```make_sports_list.py ```

this will create txt file for use when requesting sports.



```
python main.py 
```
This will
- use list of sports from sports/my_sports_keys
- Print events and odds for the next upcoming games (across sports in file)
- Dumps a .json file in Json_files/ for each sport wil all selected markets for all selected regions
- Requests used & remaining for your api key

To change setting look in config.cfg


After this you may wish to run ```find_arbitrage_2_way.py or find_arbitrage_3_way.py```

Before doing so you can edit config.cfg to change the bet amount and also change which bookies 

it will find arbitrage for **NOTE, ONLY FOR AU MARKETS AT CURRENT WILL ADD OTHERS LATER

This will check for any arbitrage bets in h2h markets and create 2 files in /files one for all bookies and one for selected bookies


#### TODO
- add all bookies
- fing API request to get bookies per region *dont know if possible
- clean and tidy up
- add more arbitrage oppertunities
- add dumps for easy to read all bookies for events and prices



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
