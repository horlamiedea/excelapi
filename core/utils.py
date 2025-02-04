import swisseph as swe
import datetime
import pandas as pd
import yfinance as yf
import os

csv_path = "cleaned_nifty_50_data.csv"

# Set the path to the ephemeris data
swe.set_ephe_path('./ephemeris')

# Define constants for planet names and zodiac signs
PLANET_NAMES = {
    swe.SUN: "Sun",
    swe.MOON: "Moon",
    swe.MERCURY: "Mercury",
    swe.VENUS: "Venus",
    swe.MARS: "Mars",
    swe.JUPITER: "Jupiter",
    swe.SATURN: "Saturn",
    swe.URANUS: "Uranus",
    swe.NEPTUNE: "Neptune",
    swe.PLUTO: "Pluto"
}

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", 
    "Virgo", "Libra", "Scorpio", "Sagittarius", 
    "Capricorn", "Aquarius", "Pisces"
]

# Function to evaluate sentiment based on astrological data
def evaluate_sentiment(date, planet):
    jd = swe.julday(date.year, date.month, date.day)
    planet_pos, _ = swe.calc_ut(jd, planet)
    lon = planet_pos[0]
    retrograde = planet_pos[3] < 0
    zodiac_sign = int(lon // 30)
    
    sentiment_score = 0.0
    
    # Retrograde Effect
    sentiment_score += -10 if retrograde else 10

    # Zodiac Position Effects (Continuous Scoring)
    fire_signs = ["Aries", "Leo", "Sagittarius"]
    water_signs = ["Cancer", "Scorpio", "Pisces"]
    earth_signs = ["Taurus", "Virgo", "Capricorn"]
    air_signs = ["Gemini", "Libra", "Aquarius"]
    
    if ZODIAC_SIGNS[zodiac_sign] in fire_signs:
        sentiment_score += 15
    elif ZODIAC_SIGNS[zodiac_sign] in water_signs:
        sentiment_score += -10
    elif ZODIAC_SIGNS[zodiac_sign] in earth_signs:
        sentiment_score += 5
    elif ZODIAC_SIGNS[zodiac_sign] in air_signs:
        sentiment_score += 8

    # Normalize Sentiment Percentage
    max_score = 100  # Hypothetical max score
    min_score = -100  # Hypothetical min score
    sentiment_percentage = ((sentiment_score - min_score) / (max_score - min_score)) * 100
    
    return {
        "planet": PLANET_NAMES[planet],
        "sentiment": "bullish" if sentiment_score > 0 else "bearish" if sentiment_score < 0 else "neutral",
        # "percentage": round(sentiment_percentage, 2),
        "sign": ZODIAC_SIGNS[zodiac_sign],
        "motion": "retrograde" if retrograde else "direct"  # Indicates if the planet is in retrograde or direct motion
    }


# List of planets to be used in the API
PLANETS = [swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS,
           swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO]

# Global variables for NIFTY 50 data
TICKER = "^NSEI"
CSV_FILE = "nifty_50_data.csv"
START_DATE = "2009-01-01"
END_DATE = pd.Timestamp.today().strftime("%Y-%m-%d")

# Ensure NIFTY 50 data is available
if not os.path.exists(CSV_FILE):
    print("Fetching NIFTY 50 data from 2009 to today...")
    nifty50_data = yf.download(TICKER, start=START_DATE, end=END_DATE)
    nifty50_data.reset_index(inplace=True)  # Convert index to column
    nifty50_data.to_csv(CSV_FILE, index=False)
else:
    print("Loading existing data...")
    nifty50_data = pd.read_csv(CSV_FILE, parse_dates=["Date"])

def get_stock_data(date_str):
    """
    Retrieves NIFTY 50 stock data for a specific date.
    
    Parameters:
    - date_str (str): Date in 'YYYY-MM-DD' format.
    
    Returns:
    - dict: Stock data for the given date.
    """
    try:
        # Convert to correct date format
        date = pd.to_datetime(date_str, errors="coerce")
        if date is pd.NaT:
            return {"error": "Invalid date format. Use YYYY-MM-DD."}

        # Check if the date exists in the dataset
        stock_row = nifty50_data[nifty50_data["Date"] == date]

        if not stock_row.empty:
            stock_info = {
                "Open": float(stock_row["Open"].values[0]),
                "High": float(stock_row["High"].values[0]),
                "Low": float(stock_row["Low"].values[0]),
                "Close": float(stock_row["Close"].values[0]),
                "Volume": int(stock_row["Volume"].values[0]),
            }

            print(stock_info)
            return stock_info
        

        return {"error": f"No stock data available for {date_str}"}

    except Exception as e:
        return {"error": str(e)}