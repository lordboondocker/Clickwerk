from django.urls import path
from . import views

boosts = views.BoostViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

urlpatterns = [
    path('call_click/', views.call_click),
    path('boosts/', boosts, name='boosts')
]