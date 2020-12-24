from django.shortcuts import render

# Create your views here.

def main(request):
    return render(request, 'web/index.html', {})

def imae(request, workweek='', filename='index'):
    if workweek == 'weekday':
        return render(request, f'web/imae/weekday/{filename}.html', {})
    elif workweek == 'weekend_holiday':
        return render(request, f'web/imae/weekend_holiday/{filename}.html', {})
    else:
        return render(request, 'web/imae/index.html', {})

def choji(request, workweek='', filename='index'):
    if workweek == 'weekday':
        return render(request, f'web/choji/weekday/{filename}.html', {})
    elif workweek == 'weekend_holiday':
        return render(request, f'web/choji/weekend_holiday/{filename}.html', {})
    else:
        return render(request, 'web/choji/index.html', {})

def sinnae(request, workweek='', filename='index'):
    if workweek == 'weekday':
        return render(request, f'web/sinnae/weekday/{filename}.html', {})
    elif workweek == 'saturday':
        return render(request, f'web/sinnae/saturday/{filename}.html', {})
    elif workweek == 'sunday_holiday':
        return render(request, f'web/sinnae/sunday_holiday/{filename}.html', {})
    else:
        return render(request, 'web/sinnae/index.html', {})

def daegok(request, workweek='', filename='index'):
    if workweek == 'weekday':
        return render(request, f'web/daegok/weekday/{filename}.html', {})
    elif workweek == 'weekend_holiday':
        return render(request, f'web/daegok/weekend_holiday/{filename}.html', {})
    else:
        return render(request, 'web/daegok/index.html', {})

def olympic_park(request, workweek='', filename='index'):
    if workweek == 'weekday':
        return render(request, f'web/olympic_park/weekday/{filename}.html', {})
    elif workweek == 'weekend_holiday':
        return render(request, f'web/olympic_park/weekend_holiday/{filename}.html', {})
    else:
        return render(request, 'web/olympic_park/index.html', {})

def sosa(request, workweek='', filename='index'):
    if workweek == 'weekday':
        return render(request, f'web/sosa/weekday/{filename}.html', {})
    elif workweek == 'weekend_holiday':
        return render(request, f'web/sosa/weekend_holiday/{filename}.html', {})
    else:
        return render(request, 'web/sosa/index.html', {})

