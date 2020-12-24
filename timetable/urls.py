from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('imae/', views.imae, name='imae'),
    path('choji/', views.choji, name='choji'),
    path('sinnae/', views.sinnae, name='sinnae'),
    path('daegok/', views.daegok, name='daegok'),
    path('olympic_park/', views.olympic_park, name='olympic_park'),
    path('sosa/', views.sosa, name='sosa'),
    path('imae/<slug:workweek>/', views.imae, name='imae-workweek'),
    path('choji/<slug:workweek>/', views.choji, name='choji-workweek'),
    path('sinnae/<slug:workweek>/', views.sinnae, name='sinnae-workweek'),
    path('daegok/<slug:workweek>/', views.daegok, name='daegok-workweek'),
    path('olympic_park/<slug:workweek>/', views.olympic_park, name='olympic_park-workweek'),
    path('sosa/<slug:workweek>/', views.sosa, name='sosa-workweek'),
    path('imae/<slug:workweek>/<slug:filename>.html', views.imae, name='imae-workweek-timetable'),
    path('choji/<slug:workweek>/<slug:filename>.html', views.choji, name='choji-workweek-timetable'),
    path('sinnae/<slug:workweek>/<slug:filename>.html', views.sinnae, name='sinnae-workweek-timetable'),
    path('daegok/<slug:workweek>/<slug:filename>.html', views.daegok, name='daegok-workweek-timetable'),
    path('olympic_park/<slug:workweek>/<slug:filename>.html', views.olympic_park, name='olympic_park-workweek-timetable'),
    path('sosa/<slug:workweek>/<slug:filename>.html', views.sosa, name='sosa-workweek-timetable'),
]
