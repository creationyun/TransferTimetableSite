from django.shortcuts import render

# Create your views here.

def main(request):
    return render(request, 'web/index.html', {})


workweek2_list = [
    {'href': 'weekday', 'primary': True, 'name': '평일'},
    {'href': 'weekend_holiday', 'primary': False, 'name': '주말/공휴일'},
]

workweek3_list = [
    {'href': 'weekday', 'primary': True, 'name': '평일'},
    {'href': 'saturday', 'primary': False, 'name': '토요일'},
    {'href': 'sunday_holiday', 'primary': False, 'name': '일요일/공휴일'},
]


def imae(request, workweek='', filename='index'):
    if workweek == '':
        return render(request, 'web/select-workweek.html', {
            'workweek_list': workweek2_list
        })
    elif filename == 'index':
        arrival_list = [
            {'code': 'sbu', 'selected': True,  'name': '수인분당선 왕십리 방면 열차'},
            {'code': 'sbd', 'selected': False, 'name': '수인분당선 죽전/고색/인천 방면 열차'},
            {'code': 'ggu', 'selected': False, 'name': '경강선 판교 방면 열차'},
            {'code': 'ggd', 'selected': False, 'name': '경강선 여주 방면 열차'},
        ]
        transfer_list = arrival_list
        
        return render(request, 'web/select-transfer-direction.html', {
            'station': 'imae', 'workweek': workweek,
            'arrival_list': arrival_list, 'transfer_list': transfer_list
        })
    else:
        return render(request, f'web/imae/{workweek}/{filename}.html', {})


def choji(request, workweek='', filename='index'):
    if workweek == '':
        return render(request, 'web/select-workweek.html', {
            'workweek_list': workweek2_list
        })
    elif filename == 'index':
        arrival_list = [
            {'code': 'l4u', 'selected': True,  'name': '4호선 당고개 방면 열차'},
            {'code': 'l4d', 'selected': False, 'name': '4호선 오이도 방면 열차'},
            {'code': 'shu', 'selected': False, 'name': '서해선 소사 방면 열차'},
            {'code': 'shd', 'selected': False, 'name': '서해선 원시 방면 열차'},
            {'code': 'sbu', 'selected': False, 'name': '수인분당선 왕십리 방면 열차'},
            {'code': 'sbd', 'selected': False, 'name': '수인분당선 인천 방면 열차'},
        ]
        transfer_list = arrival_list
        
        return render(request, 'web/select-transfer-direction.html', {
            'station': 'choji', 'workweek': workweek,
            'arrival_list': arrival_list, 'transfer_list': transfer_list
        })
    else:
        return render(request, f'web/choji/{workweek}/{filename}.html', {})


def sinnae(request, workweek='', filename='index'):
    if workweek == '':
        return render(request, 'web/select-workweek.html', {
            'workweek_list': workweek3_list
        })
    elif filename == 'index':
        arrival_list = [
            {'code': 'l6d', 'selected': True,  'name': '6호선 신내 종착 열차'},
            {'code': 'gcu', 'selected': False, 'name': '경춘선 상봉/청량리 방면 열차'},
            {'code': 'gcd', 'selected': False, 'name': '경춘선 춘천 방면 열차'},
        ]
        transfer_list = [
            {'code': 'l6u', 'selected': True,  'name': '6호선 응암순환 방면 열차'},
            {'code': 'gcu', 'selected': False, 'name': '경춘선 상봉/청량리 방면 열차'},
            {'code': 'gcd', 'selected': False, 'name': '경춘선 춘천 방면 열차'},
        ]
        
        return render(request, 'web/select-transfer-direction.html', {
            'station': 'sinnae', 'workweek': workweek,
            'arrival_list': arrival_list, 'transfer_list': transfer_list
        })
    else:
        return render(request, f'web/sinnae/{workweek}/{filename}.html', {})


def daegok(request, workweek='', filename='index'):
    if workweek == '':
        return render(request, 'web/select-workweek.html', {
            'workweek_list': workweek2_list
        })
    elif filename == 'index':
        arrival_list = [
            {'code': 'l3u', 'selected': True,  'name': '3호선 대화 방면 열차'},
            {'code': 'l3d', 'selected': False, 'name': '3호선 오금 방면 열차'},
            {'code': 'gju', 'selected': False, 'name': '경의중앙선 서울역/용문 방면 열차'},
            {'code': 'gjd', 'selected': False, 'name': '경의중앙선 문산 방면 열차'},
        ]
        transfer_list = arrival_list
        
        return render(request, 'web/select-transfer-direction.html', {
            'station': 'daegok', 'workweek': workweek,
            'arrival_list': arrival_list, 'transfer_list': transfer_list
        })
    else:
        return render(request, f'web/daegok/{workweek}/{filename}.html', {})


def olympic_park(request, workweek='', filename='index'):
    if workweek == '':
        return render(request, 'web/select-workweek.html', {
            'workweek_list': workweek2_list
        })
    elif filename == 'index':
        arrival_list = [
            {'code': 'l5u',  'selected': True,  'name': '5호선 방화 방면 열차'},
            {'code': 'l5d',  'selected': False, 'name': '5호선 마천 방면 열차'},
            {'code': 'l9au', 'selected': False, 'name': '9호선 중앙보훈병원 방면 일반열차'},
            {'code': 'l9ad', 'selected': False, 'name': '9호선 개화 방면 일반열차'},
            {'code': 'l9eu', 'selected': False, 'name': '9호선 중앙보훈병원 방면 급행열차'},
            {'code': 'l9ed', 'selected': False, 'name': '9호선 김포공항 방면 급행열차'},
        ]
        transfer_list = arrival_list
        
        return render(request, 'web/select-transfer-direction.html', {
            'station': 'olympic_park', 'workweek': workweek,
            'arrival_list': arrival_list, 'transfer_list': transfer_list
        })
    else:
        return render(request, f'web/olympic_park/{workweek}/{filename}.html', {})


def sosa(request, workweek='', filename='index'):
    if workweek == '':
        return render(request, 'web/select-workweek.html', {
            'workweek_list': workweek2_list
        })
    elif filename == 'index':
        arrival_list = [
            {'code': 'shu', 'selected': True,  'name': '서해선 소사 종착 열차'},
            {'code': 'l1u', 'selected': False, 'name': '1호선 소요산 방면 열차'},
            {'code': 'l1d', 'selected': False, 'name': '1호선 인천 방면 열차'},
        ]
        transfer_list = [
            {'code': 'shd', 'selected': True,  'name': '서해선 원시 방면 열차'},
            {'code': 'l1u', 'selected': False, 'name': '1호선 소요산 방면 열차'},
            {'code': 'l1d', 'selected': False, 'name': '1호선 인천 방면 열차'},
        ]
        
        return render(request, 'web/select-transfer-direction.html', {
            'station': 'sosa', 'workweek': workweek,
            'arrival_list': arrival_list, 'transfer_list': transfer_list
        })
    else:
        return render(request, f'web/sosa/{workweek}/{filename}.html', {})

