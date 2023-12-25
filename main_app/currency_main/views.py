from django.shortcuts import render, redirect
from django.http import HttpResponse
from binance.client import Client
from django.http import JsonResponse

client = Client()

additional_symbols = ['ETHUSDT', 'XRPUSDT', 'LTCUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'LINKUSDT', 'DOTUSDT', 'UNIUSDT', 'SOLUSDT']

def update_binance_data(request):
    data = []

    for symbol in ['BTCUSDT'] + additional_symbols:
        try:
            ticker_stats = client.get_ticker(symbol=symbol)

            # Extract relevant data
            ticker_percentage = ticker_stats['priceChangePercent']
            ticker_volume = ticker_stats['volume']
            ticker_high = ticker_stats['highPrice']
            ticker_low = ticker_stats['lowPrice']

            coin_data = {
                'symbol': symbol,
                'high': ticker_high,
                'low': ticker_low,
                'percentage': ticker_percentage,
                'volume': ticker_volume,
            }

            data.append(coin_data)

        except Exception as e:
            coin_data = {
                'symbol': symbol,
                'error': f"Error fetching data: {e}",
            }
            data.append(coin_data)

    context = {
        'coin_data': data,
    }

    return render(request, 'main-page.html', context)


def main_page(request):
    return render(request,'main-page.html')

def graphics(request):
    return render(request,'graphics.html')