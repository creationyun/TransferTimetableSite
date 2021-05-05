from django.views import View
from django.http import Http404
from django.shortcuts import render
from .models import RequestedStation
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
    return render(request, 'web/index.html', {'alert': False, 'alert_msg': ''})


def report(request):
    if request.method == 'POST':
        station = request.POST['station']
        if station == '':
            return render(request, 'web/index.html', {'alert': True, 'alert_msg': '역명을 입력해주세요.'})
        if len(station) > 50:
            return render(request, 'web/index.html', {'alert': True, 'alert_msg': '역명은 50자 미만이어야 합니다.'})

        # Create object
        RequestedStation.objects.create(station_name=station)

        return render(request, 'web/index.html', {'alert': True, 'alert_msg': '성공적으로 반영되었습니다.'})
    else:
        return Http404("Accessed without request.")


class Station(View):
    station_name = None
    arrival_list = []
    transfer_list = []
    workweek_list = workweek2_list
    map_image_filename = ''

    def get(self, request, workweek=''):
        if workweek == '':
            return render(request, 'web/select-workweek.html', {
                'workweek_list': self.workweek_list
            })
        else:
            return render(request, 'web/select-transfer-direction.html', {
                'station': self.station_name, 'workweek': workweek,
                'arrival_list': self.arrival_list, 'transfer_list': self.transfer_list,
                'map_image': self.map_image_filename
            })


class Timetable(View):
    station_name = None
    code_to_timetable = {}
    before_bound_for_dict = {}
    after_bound_for_dict = {}

    def walk_time_rule(self, arrival_code, transfer_code):
        return timedelta(minutes=0)

    def set_bound_for_dict(self, workweek, arrival_code, transfer_code):
        # Read 'before' timetable
        before, before_info = tt.read_timetable(
            f'timetable/TransferTimetable/{self.station_name}/{workweek}/{self.code_to_timetable[arrival_code]}')

        self.before_bound_for_dict = {}

        for elem in before:
            if elem['bound_for'] in self.before_bound_for_dict:
                self.before_bound_for_dict[elem['bound_for']] += 1
            else:
                self.before_bound_for_dict[elem['bound_for']] = 1

        # Read 'after' timetable
        after, after_info = tt.read_timetable(
            f'timetable/TransferTimetable/{self.station_name}/{workweek}/{self.code_to_timetable[transfer_code]}',
            allow_terminal=False)

        self.after_bound_for_dict = {}

        for elem in after:
            if elem['bound_for'] in self.after_bound_for_dict:
                self.after_bound_for_dict[elem['bound_for']] += 1
            else:
                self.after_bound_for_dict[elem['bound_for']] = 1

        return before, before_info, after, after_info

    def get(self, request, workweek, arrival_code, transfer_code):
        try:
            before, before_info, after, after_info = self.set_bound_for_dict(workweek, arrival_code, transfer_code)

            before_bound_for_list = [x[0] for x in sorted(self.before_bound_for_dict.items(),
                                                          key=lambda item: -item[1])]
            after_bound_for_list = [x[0] for x in sorted(self.after_bound_for_dict.items(),
                                                         key=lambda item: -item[1])]
            walk_time = self.walk_time_rule(arrival_code, transfer_code)
        except (KeyError, FileNotFoundError, IndexError):
            raise Http404("Workweek or arrival/transfer code is not valid.")

        result = tt.derive_transfer_timetable(before, after, walk_time)

        return render(request, f'web/transfer-timetable.html',
                      {'before_info': before_info, 'after_info': after_info, 'result': result, 'walk_time': walk_time,
                       'before_bound_for_list': before_bound_for_list, 'after_bound_for_list': after_bound_for_list,
                       'before_bound_for_selected': before_bound_for_list,
                       'after_bound_for_selected': after_bound_for_list
                       })

    def post(self, request, workweek, arrival_code, transfer_code):
        try:
            self.set_bound_for_dict(workweek, arrival_code, transfer_code)

            # Before Transfer
            before_bound_for_selected = request.POST.getlist('before[]')
            before_bound_for_list = [x[0] for x in sorted(self.before_bound_for_dict.items(),
                                                          key=lambda item: -item[1])]

            before, before_info = tt.read_timetable(
                f'timetable/TransferTimetable/{self.station_name}/{workweek}/{self.code_to_timetable[arrival_code]}',
                exclude_bound_for=[x for x in before_bound_for_list if x not in before_bound_for_selected])

            # After Transfer
            after_bound_for_selected = set(request.POST.getlist('after[]'))
            after_bound_for_list = [x[0] for x in sorted(self.after_bound_for_dict.items(),
                                                         key=lambda item: -item[1])]

            after, after_info = tt.read_timetable(
                f'timetable/TransferTimetable/{self.station_name}/{workweek}/{self.code_to_timetable[transfer_code]}',
                allow_terminal=False,
                exclude_bound_for=[x for x in after_bound_for_list if x not in after_bound_for_selected]
            )

            walk_time = self.walk_time_rule(arrival_code, transfer_code)
        except (KeyError, FileNotFoundError, IndexError):
            raise Http404("Workweek or arrival/transfer code is not valid.")

        result = tt.derive_transfer_timetable(before, after, walk_time)

        return render(request, f'web/transfer-timetable.html',
                      {'before_info': before_info, 'after_info': after_info, 'result': result, 'walk_time': walk_time,
                       'before_bound_for_list': before_bound_for_list, 'after_bound_for_list': after_bound_for_list,
                       'before_bound_for_selected': before_bound_for_selected,
                       'after_bound_for_selected': after_bound_for_selected})


class Imae(Station):
    station_name = 'imae'
    arrival_list = [
        {'code': 'sbu', 'selected': True, 'name': '수인분당선 왕십리 방면 열차 (서현 → 이매)'},
        {'code': 'sbd', 'selected': False, 'name': '수인분당선 죽전/고색/인천 방면 열차 (야탑 → 이매)'},
        {'code': 'ggu', 'selected': False, 'name': '경강선 판교 방면 열차 (삼동 → 이매)'},
        {'code': 'ggd', 'selected': False, 'name': '경강선 여주 방면 열차 (판교 → 이매)'},
    ]
    transfer_list = [
        {'code': 'sbu', 'selected': True, 'name': '수인분당선 왕십리 방면 열차 (이매 → 야탑)'},
        {'code': 'sbd', 'selected': False, 'name': '수인분당선 죽전/고색/인천 방면 열차 (이매 → 서현)'},
        {'code': 'ggu', 'selected': False, 'name': '경강선 판교 방면 열차 (이매 → 판교)'},
        {'code': 'ggd', 'selected': False, 'name': '경강선 여주 방면 열차 (이매 → 삼동)'},
    ]
    map_image_filename = 'images/imae-map.jpg'


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
        {'code': 'l4u', 'selected': True, 'name': '4호선 당고개 방면 열차 (안산 → 초지)'},
        {'code': 'l4d', 'selected': False, 'name': '4호선 오이도 방면 열차 (고잔 → 초지)'},
        {'code': 'shu', 'selected': False, 'name': '서해선 소사 방면 열차 (시우(원곡) → 초지)'},
        {'code': 'shd', 'selected': False, 'name': '서해선 원시 방면 열차 (선부 → 초지)'},
        {'code': 'sbu', 'selected': False, 'name': '수인분당선 왕십리 방면 열차 (안산 → 초지)'},
        {'code': 'sbd', 'selected': False, 'name': '수인분당선 인천 방면 열차 (고잔 → 초지)'},
    ]
    transfer_list = [
        {'code': 'l4u', 'selected': True, 'name': '4호선 당고개 방면 열차 (초지 → 고잔)'},
        {'code': 'l4d', 'selected': False, 'name': '4호선 오이도 방면 열차 (초지 → 안산)'},
        {'code': 'shu', 'selected': False, 'name': '서해선 소사 방면 열차 (초지 → 선부)'},
        {'code': 'shd', 'selected': False, 'name': '서해선 원시 방면 열차 (초지 → 시우(원곡))'},
        {'code': 'sbu', 'selected': False, 'name': '수인분당선 왕십리 방면 열차 (초지 → 고잔)'},
        {'code': 'sbd', 'selected': False, 'name': '수인분당선 인천 방면 열차 (초지 → 안산)'},
    ]
    map_image_filename = 'images/choji-map.jpg'


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
        {'code': 'l6d', 'selected': True, 'name': '6호선 신내 종착 열차 (봉화산 → 신내)'},
        {'code': 'gcu', 'selected': False, 'name': '경춘선 상봉/청량리 방면 열차 (갈매 → 신내)'},
        {'code': 'gcd', 'selected': False, 'name': '경춘선 춘천 방면 열차 (망우 → 신내)'},
    ]
    transfer_list = [
        {'code': 'l6u', 'selected': True, 'name': '6호선 응암순환 방면 열차 (신내 → 봉화산)'},
        {'code': 'gcu', 'selected': False, 'name': '경춘선 상봉/청량리 방면 열차 (신내 → 망우)'},
        {'code': 'gcd', 'selected': False, 'name': '경춘선 춘천 방면 열차 (신내 → 갈매)'},
    ]
    workweek_list = workweek2_list
    map_image_filename = 'images/sinnae-map.jpg'


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
        {'code': 'l3u', 'selected': True, 'name': '3호선 대화 방면 열차 (화정 → 대곡)'},
        {'code': 'l3d', 'selected': False, 'name': '3호선 오금 방면 열차 (백석 → 대곡)'},
        {'code': 'gju', 'selected': False, 'name': '경의중앙선 서울역/용문 방면 열차 (곡산 → 대곡)'},
        {'code': 'gjd', 'selected': False, 'name': '경의중앙선 문산 방면 열차 (능곡 → 대곡)'},
    ]
    transfer_list = [
        {'code': 'l3u', 'selected': True, 'name': '3호선 대화 방면 열차 (대곡 → 백석)'},
        {'code': 'l3d', 'selected': False, 'name': '3호선 오금 방면 열차 (대곡 → 화정)'},
        {'code': 'gju', 'selected': False, 'name': '경의중앙선 서울역/용문 방면 열차 (대곡 → 능곡)'},
        {'code': 'gjd', 'selected': False, 'name': '경의중앙선 문산 방면 열차 (대곡 → 곡산)'},
    ]
    map_image_filename = 'images/daegok-map.jpg'


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
        {'code': 'l5u', 'selected': True, 'name': '5호선 방화 방면 열차 (방이 → 올림픽공원)'},
        {'code': 'l5d', 'selected': False, 'name': '5호선 마천 방면 열차 (둔촌동 → 올림픽공원)'},
        {'code': 'l9au', 'selected': False, 'name': '9호선 중앙보훈병원 방면 일반열차 (한성백제 → 올림픽공원)'},
        {'code': 'l9ad', 'selected': False, 'name': '9호선 개화 방면 일반열차 (둔촌오륜 → 올림픽공원)'},
        {'code': 'l9eu', 'selected': False, 'name': '9호선 중앙보훈병원 방면 급행열차 (석촌 → 올림픽공원)'},
        {'code': 'l9ed', 'selected': False, 'name': '9호선 김포공항 방면 급행열차 (중앙보훈병원 → 올림픽공원)'},
    ]
    transfer_list = [
        {'code': 'l5u', 'selected': True, 'name': '5호선 방화 방면 열차 (올림픽공원 → 둔촌동)'},
        {'code': 'l5d', 'selected': False, 'name': '5호선 마천 방면 열차 (올림픽공원 → 방이)'},
        {'code': 'l9au', 'selected': False, 'name': '9호선 중앙보훈병원 방면 일반열차 (올림픽공원 → 둔촌오륜)'},
        {'code': 'l9ad', 'selected': False, 'name': '9호선 개화 방면 일반열차 (올림픽공원 → 한성백제)'},
        {'code': 'l9eu', 'selected': False, 'name': '9호선 중앙보훈병원 방면 급행열차 (올림픽공원 → 중앙보훈병원)'},
        {'code': 'l9ed', 'selected': False, 'name': '9호선 김포공항 방면 급행열차 (올림픽공원 → 석촌)'},
    ]
    map_image_filename = 'images/olympic_park-map.jpg'


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
        return timedelta(minutes=3)


class Sosa(Station):
    station_name = 'sosa'
    arrival_list = [
        {'code': 'shu', 'selected': True, 'name': '서해선 소사 종착 열차 (소새울 → 소사)'},
        {'code': 'l1u', 'selected': False, 'name': '1호선 소요산 방면 열차 (부천 → 소사)'},
        {'code': 'l1d', 'selected': False, 'name': '1호선 인천 방면 열차 (역곡 → 소사)'},
    ]
    transfer_list = [
        {'code': 'shd', 'selected': True, 'name': '서해선 원시 방면 열차 (소사 → 소새울)'},
        {'code': 'l1u', 'selected': False, 'name': '1호선 소요산 방면 열차 (소사 → 역곡)'},
        {'code': 'l1d', 'selected': False, 'name': '1호선 인천 방면 열차 (소사 → 부천)'},
    ]
    map_image_filename = 'images/sosa-map.jpg'


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


class Hoegi(Station):
    station_name = 'hoegi'
    arrival_list = [
        {'code': 'l1u', 'selected': False, 'name': '1호선 소요산 방면 열차 (청량리 → 회기)'},
        {'code': 'l1d', 'selected': False, 'name': '1호선 인천/신창 방면 열차 (외대앞 → 회기)'},
        {'code': 'gju', 'selected': False, 'name': '경의중앙선 문산 방면 열차 (중랑 → 회기)'},
        {'code': 'gjd', 'selected': False, 'name': '경의중앙선 용문 방면 열차 (청량리 → 회기)'},
        {'code': 'gcu', 'selected': False, 'name': '경춘선 청량리 방면 열차 (중랑 → 회기)'},
        {'code': 'gcd', 'selected': False, 'name': '경춘선 춘천 방면 열차 (청량리 → 회기)'},
    ]
    transfer_list = [
        {'code': 'l1u', 'selected': False, 'name': '1호선 소요산 방면 열차 (회기 → 외대앞)'},
        {'code': 'l1d', 'selected': False, 'name': '1호선 인천/신창 방면 열차 (회기 → 청량리)'},
        {'code': 'gju', 'selected': False, 'name': '경의중앙선 문산 방면 열차 (회기 → 청량리)'},
        {'code': 'gjd', 'selected': False, 'name': '경의중앙선 용문 방면 열차 (회기 → 중랑)'},
        {'code': 'gcu', 'selected': False, 'name': '경춘선 청량리 방면 열차 (회기 → 청량리)'},
        {'code': 'gcd', 'selected': False, 'name': '경춘선 춘천 방면 열차 (회기 → 중랑)'},
    ]
    map_image_filename = 'images/hoegi-map.jpg'


class HoegiTimetable(Timetable):
    station_name = 'hoegi'
    code_to_timetable = {
        'l1u': '1_soyosan.txt',
        'l1d': '1_incheon_sinchang.txt',
        'gju': 'gyeonguijungang_munsan.txt',
        'gjd': 'gyeonguijungang_yongmun.txt',
        'gcu': 'gyeongchun_cheongnyangni.txt',
        'gcd': 'gyeongchun_chuncheon.txt'
    }

    def walk_time_rule(self, arrival_code, transfer_code):
        if arrival_code[:2] == 'l1' or transfer_code[:2] == 'l1':
            return timedelta(minutes=2)
        else:
            return timedelta(minutes=0)
