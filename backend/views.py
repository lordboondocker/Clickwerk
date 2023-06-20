from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Core, Boost
from .serializers import CoreSerializers, BoostSerializer


@api_view(['GET'])
def call_click(request):
    core = Core.objects.get(user=request.user)
    is_lvlup = core.click()
    if is_lvlup:
        Boost.objects.create(core=core, price=core.level*50, power=core.level * 20)
    core.save()

    return Response({'core': CoreSerializers(core).data, 'is_lvlup': is_lvlup})


class BoostViewSet(viewsets.ModelViewSet):
    queryset = Boost.objects.all()
    serializer_class = BoostSerializer

    def get_queryset(self):
        core = Core.objects.get(user=self.request.user)
        boosts = Boost.objects.filter(core=core)
        return boosts
