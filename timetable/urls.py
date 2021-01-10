from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('report/', views.report, name='report'),
    path('imae/', views.Imae.as_view(), name='imae'),
    path('choji/', views.Choji.as_view(), name='choji'),
    path('sinnae/', views.Sinnae.as_view(), name='sinnae'),
    path('daegok/', views.Daegok.as_view(), name='daegok'),
    path('olympic_park/', views.OlympicPark.as_view(), name='olympic_park'),
    path('sosa/', views.Sosa.as_view(), name='sosa'),
    path('imae/<slug:workweek>/', views.Imae.as_view(), name='imae-workweek'),
    path('choji/<slug:workweek>/', views.Choji.as_view(), name='choji-workweek'),
    path('sinnae/<slug:workweek>/', views.Sinnae.as_view(), name='sinnae-workweek'),
    path('daegok/<slug:workweek>/', views.Daegok.as_view(), name='daegok-workweek'),
    path('olympic_park/<slug:workweek>/', views.OlympicPark.as_view(), name='olympic_park-workweek'),
    path('sosa/<slug:workweek>/', views.Sosa.as_view(), name='sosa-workweek'),
    path('imae/<slug:workweek>/<slug:arrival_code>/<slug:transfer_code>/', views.ImaeTimetable.as_view(), name='imae-workweek-timetable'),
    path('choji/<slug:workweek>/<slug:arrival_code>/<slug:transfer_code>/', views.ChojiTimetable.as_view(), name='choji-workweek-timetable'),
    path('sinnae/<slug:workweek>/<slug:arrival_code>/<slug:transfer_code>/', views.SinnaeTimetable.as_view(), name='sinnae-workweek-timetable'),
    path('daegok/<slug:workweek>/<slug:arrival_code>/<slug:transfer_code>/', views.DaegokTimetable.as_view(), name='daegok-workweek-timetable'),
    path('olympic_park/<slug:workweek>/<slug:arrival_code>/<slug:transfer_code>/', views.OlympicParkTimetable.as_view(), name='olympic_park-workweek-timetable'),
    path('sosa/<slug:workweek>/<slug:arrival_code>/<slug:transfer_code>/', views.SosaTimetable.as_view(), name='sosa-workweek-timetable'),
]
