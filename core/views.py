from django.http import JsonResponse
import datetime
import swisseph as swe
from django.views.decorators.csrf import csrf_exempt
from .utils import evaluate_sentiment, PLANETS  # Ensure evaluate_sentiment and PLANETS are moved to utils.py or similar


@csrf_exempt
def sentiment_analysis(request):
    # Parse date from query parameters
    date_str = request.GET.get('date', '')
    try:
        date = datetime.datetime.strptime(date_str, '%d-%b-%Y').date()
    except ValueError:
        date = datetime.datetime.strptime(date_str, '%d-%m-%Y').date()

    results = []
    for planet in PLANETS:
        sentiment_data = evaluate_sentiment(date, planet)
        results.append(sentiment_data)

    return JsonResponse(results, safe=False)
