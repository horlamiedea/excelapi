from django.http import JsonResponse
import datetime
import swisseph as swe
from django.views.decorators.csrf import csrf_exempt
from .utils import evaluate_sentiment, PLANETS, get_stock_data  # Ensure evaluate_sentiment and PLANETS are moved to utils.py or similar
from dateutil.parser import parse


@csrf_exempt

def sentiment_analysis(request):
    # Parse date from query parameters
    date_str = request.GET.get('date', '')
    if not date_str:
        return JsonResponse({'error': 'Date parameter is required'}, status=400)

    try:
        date = parse(date_str).date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    # Get stock data
    stock_data = get_stock_data(date_str)

    # Format stock data correctly
    stock_response = {
        "Open": stock_data.get("Open"),
        "High": stock_data.get("High"),
        "Low": stock_data.get("Low"),
        "Close": stock_data.get("Close"),
        "Volume": stock_data.get("Volume")
    }

    # Get sentiment analysis for all planets
    results = []
    for planet in PLANETS:
        sentiment_data = evaluate_sentiment(date, planet)
        results.append(sentiment_data)

    # Return combined response (without nesting inside keys)
    response_data = [stock_response] + results  # Stock data first, followed by sentiment analysis

    return JsonResponse(response_data, safe=False)