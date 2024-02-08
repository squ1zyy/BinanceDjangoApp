def get_coin(request):
    coin = request.GET.get('coin', default='BTCUSDT')
    return coin