from django.http import JsonResponse
import datetime
import swisseph as swe
from django.views.decorators.csrf import csrf_exempt
from .utils import evaluate_sentiment, PLANETS  # Ensure evaluate_sentiment and PLANETS are moved to utils.py or similar
from dateutil.parser import parse


@csrf_exempt
def sentiment_analysis(request):
    # Parse date from query parameters
    date_str = request.GET.get('date', '')
    try:
        date = parse(date_str).date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    results = []
    for planet in PLANETS:
        sentiment_data = evaluate_sentiment(date, planet)
        results.append(sentiment_data)

    return JsonResponse(results, safe=False)
