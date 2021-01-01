from django.views import View
from django.http import Http404
from django.shortcuts import render
from .TransferTimetable import transfer_timetable as tt
from datetime import timedelta

workweek2_list = [
    {'href': 'weekday', 'primary': True, 'name': '평일'},
    {'href': 'weekend_holiday', 'primary': False, 'name': '주말/공휴일'},
]

workweek3_list = [
    {'href': 'weekday', 'primary': True, 'name': '평일'},
    {'href': 'saturday', 'primary': False, 'name': '토요일'},
    {'href': 'sunday_holiday', 'primary': False, 'name': '일요일/공휴일'},
]


def main(request):
    return render(request, 'web/index.html', {})


class Station(View):
    station_name = None
    arrival_list = []
    transfer_list = []
    workweek_list = workweek2_list

    def get(self, request, workweek='', filename='index'):
        if workweek == '':
            return render(request, 'web/select-workweek.html', {
                'workweek_list': self.workweek_list
            })
        elif filename == 'index':
            return render(request, 'web/select-transfer-direction.html', {
                'station': self.station_name, 'workweek': workweek,
                'arrival_list': self.arrival_list, 'transfer_list': self.transfer_list
            })


class Timetable(View):
    station_name = None
    code_to_timetable = {}

    def walk_time_rule(self, arrival_code, transfer_code):
        return timedelta(minutes=0)

    def get(self, request, workweek, arrival_code, transfer_code):
        try:
            before, before_info = tt.read_timetable(
                f'timetable/TransferTimetable/{self.station_name}/{workweek}/{self.code_to_timetable[arrival_code]}')
            after, after_info = tt.read_timetable(
                f'timetable/TransferTimetable/{self.station_name}/{workweek}/{self.code_to_timetable[transfer_code]}',
                allow_terminal=False)
            walk_time = self.walk_time_rule(arrival_code, transfer_code)
        except (KeyError, FileNotFoundError, IndexError):
            raise Http404("Workweek or arrival/transfer code is not valid.")

        result = tt.derive_transfer_timetable(before, after, walk_time)

        return render(request, f'web/transfer-timetable.html',
                      {'before_info': before_info, 'after_info': after_info, 'result': result, 'walk_time': walk_time})


class Imae(Station):
    station_name = 'imae'
    arrival_list = [
        {'code': 'sbu', 'selected': True, 'name': '수인분당선 왕십리 방면 열차'},
        {'code': 'sbd', 'selected': False, 'name': '수인분당선 죽전/고색/인천 방면 열차'},
        {'code': 'ggu', 'selected': False, 'name': '경강선 판교 방면 열차'},
        {'code': 'ggd', 'selected': False, 'name': '경강선 여주 방면 열차'},
    ]
    transfer_list = arrival_list


class ImaeTimetable(Timetable):
    station_name = 'imae'
    code_to_timetable = {
        'sbu': 'suinbundang_wangsimni.txt',
        'sbd': 'suinbundang_incheon.txt',
        'ggu': 'gyeonggang_pangyo.txt',
        'ggd': 'gyeonggang_yeoju.txt'
    }

    def walk_time_rule(self, arrival_code, transfer_code):
        return timedelta(minutes=3)


class Choji(Station):
    station_name = 'choji'
    arrival_list = [
        {'code': 'l4u', 'selected': True, 'name': '4호선 당고개 방면 열차'},
        {'code': 'l4d', 'selected': False, 'name': '4호선 오이도 방면 열차'},
        {'code': 'shu', 'selected': False, 'name': '서해선 소사 방면 열차'},
        {'code': 'shd', 'selected': False, 'name': '서해선 원시 방면 열차'},
        {'code': 'sbu', 'selected': False, 'name': '수인분당선 왕십리 방면 열차'},
        {'code': 'sbd', 'selected': False, 'name': '수인분당선 인천 방면 열차'},
    ]
    transfer_list = arrival_list


class ChojiTimetable(Timetable):
    station_name = 'choji'
    code_to_timetable = {
        'l4u': '4_danggogae.txt',
        'l4d': '4_oido.txt',
        'shu': 'seohae_sosa.txt',
        'shd': 'seohae_wonsi.txt',
        'sbu': 'suinbundang_wangsimni.txt',
        'sbd': 'suinbundang_incheon.txt'
    }

    def walk_time_rule(self, arrival_code, transfer_code):
        if arrival_code[:2] == 'sh' or transfer_code[:2] == 'sh':
            return timedelta(minutes=5)
        elif arrival_code[2:] == transfer_code[2:]:
            return timedelta(minutes=0)
        else:
            return timedelta(minutes=3)


class Sinnae(Station):
    station_name = 'sinnae'
    arrival_list = [
        {'code': 'l6d', 'selected': True, 'name': '6호선 신내 종착 열차'},
        {'code': 'gcu', 'selected': False, 'name': '경춘선 상봉/청량리 방면 열차'},
        {'code': 'gcd', 'selected': False, 'name': '경춘선 춘천 방면 열차'},
    ]
    transfer_list = [
        {'code': 'l6u', 'selected': True, 'name': '6호선 응암순환 방면 열차'},
        {'code': 'gcu', 'selected': False, 'name': '경춘선 상봉/청량리 방면 열차'},
        {'code': 'gcd', 'selected': False, 'name': '경춘선 춘천 방면 열차'},
    ]
    workweek_list = workweek3_list


class SinnaeTimetable(Timetable):
    station_name = 'sinnae'
    code_to_timetable = {
        'l6u': '6_eungam_loop.txt',
        'l6d': '6_sinnae.txt',
        'gcu': 'gyeongchun_cheongnyangni.txt',
        'gcd': 'gyeongchun_chuncheon.txt'
    }

    def walk_time_rule(self, arrival_code, transfer_code):
        return timedelta(minutes=3)


class Daegok(Station):
    station_name = 'daegok'
    arrival_list = [
        {'code': 'l3u', 'selected': True, 'name': '3호선 대화 방면 열차'},
        {'code': 'l3d', 'selected': False, 'name': '3호선 오금 방면 열차'},
        {'code': 'gju', 'selected': False, 'name': '경의중앙선 서울역/용문 방면 열차'},
        {'code': 'gjd', 'selected': False, 'name': '경의중앙선 문산 방면 열차'},
    ]
    transfer_list = arrival_list


class DaegokTimetable(Timetable):
    station_name = 'daegok'
    code_to_timetable = {
        'l3u': '3_daehwa.txt',
        'l3d': '3_ogeum.txt',
        'gju': 'gyeonguijungang_seoul_yongmun.txt',
        'gjd': 'gyeonguijungang_munsan.txt'
    }

    def walk_time_rule(self, arrival_code, transfer_code):
        return timedelta(minutes=4)


class OlympicPark(Station):
    station_name = 'olympic_park'
    arrival_list = [
        {'code': 'l5u', 'selected': True, 'name': '5호선 방화 방면 열차'},
        {'code': 'l5d', 'selected': False, 'name': '5호선 마천 방면 열차'},
        {'code': 'l9au', 'selected': False, 'name': '9호선 중앙보훈병원 방면 일반열차'},
        {'code': 'l9ad', 'selected': False, 'name': '9호선 개화 방면 일반열차'},
        {'code': 'l9eu', 'selected': False, 'name': '9호선 중앙보훈병원 방면 급행열차'},
        {'code': 'l9ed', 'selected': False, 'name': '9호선 김포공항 방면 급행열차'},
    ]
    transfer_list = arrival_list


class OlympicParkTimetable(Timetable):
    station_name = 'olympic_park'
    code_to_timetable = {
        'l5u': '5_banghwa.txt',
        'l5d': '5_macheon.txt',
        'l9au': '9a_vhs_medical_center.txt',
        'l9ad': '9a_gaehwa.txt',
        'l9eu': '9e_vhs_medical_center.txt',
        'l9ed': '9e_gimpo_intl_airport.txt'
    }

    def walk_time_rule(self, arrival_code, transfer_code):
        return timedelta(minutes=2)


class Sosa(Station):
    station_name = 'sosa'
    arrival_list = [
        {'code': 'shu', 'selected': True, 'name': '서해선 소사 종착 열차'},
        {'code': 'l1u', 'selected': False, 'name': '1호선 소요산 방면 열차'},
        {'code': 'l1d', 'selected': False, 'name': '1호선 인천 방면 열차'},
    ]
    transfer_list = [
        {'code': 'shd', 'selected': True, 'name': '서해선 원시 방면 열차'},
        {'code': 'l1u', 'selected': False, 'name': '1호선 소요산 방면 열차'},
        {'code': 'l1d', 'selected': False, 'name': '1호선 인천 방면 열차'},
    ]


class SosaTimetable(Timetable):
    station_name = 'sosa'
    code_to_timetable = {
        'shu': 'seohae_sosa.txt',
        'shd': 'seohae_wonsi.txt',
        'l1u': '1_soyosan.txt',
        'l1d': '1_incheon.txt'
    }

    def walk_time_rule(self, arrival_code, transfer_code):
        return timedelta(minutes=4)

