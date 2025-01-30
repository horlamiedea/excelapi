import swisseph as swe
import datetime

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