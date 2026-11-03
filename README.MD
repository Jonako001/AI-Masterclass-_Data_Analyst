# AI Masterclass - Data Analyst - API Phase

Week 1: Learning APIs, authentication, and fetching live data.

## Projects

- **Day 1 - API Basics**: `day1-api-basics/day1_api.py` - First API call
- **Day 2 - Exchange Rate**: `day2-exchange-rate/day2_rate.py` - Currency conversion
- **Day 3 - Travel Info**: `day3-travel-info/day3_travel_info.py` - Chained APIs (weather + country)
- **Day 4 - Live data (Browser)**: `day4-live-data/day4_fetch_exercise.html` fetch() with loading & error states - Live Bitcoin price from CoinGecko
- **Day 5 - Portfolio Project**: `kenyan-currency-tracker/tracker.py` - Kenyan Business Currency Tracker for SMEs

# Weather Now - Live CLI Weather Tool 
**Problem it solves:** You need fast, accurate weather for any city for travel, farming, or planning your day without as or complex websites.

** How it works:**
- Takes city name from user
- call 1: Geocoding API to get coordinates
- Call 2: Weather API to get live temperature, wind, humidity
- Saves Json and prints clean output

**How to run:**
'''bash
pip install requests
python weather_noy.py
# Enter: Nairobi

# Day 4 - Fetch API $ Live Data

Live Demo:`https://YOUR_USERNAME.github.io/YOUR_REPO/day4_fetch.html`
> Replace Your_USERNAME / YOUR_REPO with yours after enabling GitHub Pages.

### What it does
Fetches live Bitcoin price from CoinGecko API and displays it in USD & KES.

I started with REST Countries API (Country Info) but the API was unstable / blocked on my network and kept returning `Failed to fetch`. I switched to a more reliable public API that still meets Day 4 requirements.

### Features (meets all assignment criteria)
- [x] Uses `fetch()` with `async / await`
- [x] Shows **Loading...** state while fetching
- [x] shows **formatted output** - not raw JSON
- [x] shows **clear error handling** for invalid input
- [x] Clean, responsive UI

### How to test
1. Open `day_fetch.html`
2. Click `Refresh Price` -> Success: Shows BITCOIN, USD, KES
3. Type `bad-coin` in input -> Click Refresh -> Error: red box `Coin "bad-coin" not found...`

### Tech
- HTML, CSS, Vanilla JavaScrip
- API: https://api.coingecko.com/api/v3/simple/price

### API Example
`https://api/coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,kes`

### What I learned
- Difference between `" "` and backticks `` ` `` for template literals `${ }`
- Handling CORS / network failures with try/catch
- Using `response.ok` to detect 404s
- Live Server on VS Code (port 5500)

### Files
- `day4_fetch.html` - Main Day 4 project

## Day 5 - How to run
