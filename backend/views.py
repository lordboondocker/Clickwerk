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
        Boost.objects.create(core=core, price=core.coins, power=core.level * 2)
    core.save()

    return Response({'core': CoreSerializers(core).data, 'is_lvlup': is_lvlup})


class BoostViewSet(viewsets.ModelViewSet):
    queryset = Boost.objects.all()
    serializer_class = BoostSerializer

    def get_queryset(self):
        core = Core.objects.get(user=self.request.user)
        boosts = Boost.objects.filter(core=core)
        return boosts

    def partial_update(self, request, pk, **kwargs):
        boost = self.queryset.get(pk=pk)

        is_levelup = boost.levelup()
        if not is_levelup:
            return Response({'error': 'Не хватает денег'})

        old_boost_stats, new_boost_stats = is_levelup

        return Response({
            'old_boost_stats': self.serializer_class(old_boost_stats).data,
            'new_boost_stats': self.serializer_class(new_boost_stats).data
        })
