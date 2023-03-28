from django.views import generic
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView, status
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import filters


class HelloAPIView(APIView):
    def get(self, request):
        content = {
            "xabar":"Salom, Dunyo!",

        }
        return Response(content)

    def post(self, request):
        data = request.data
        content = {
            "xabar":"Ma'lumot qo'shildi",
            "ma'lumot": data
        }
        return Response(content)

# class AktyorAPIView(APIView):
#     def get(self, request):
#         akyor = Aktyor.objects.all()
#         serializer = AktyorSeializer(akyor, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         aktyor = request.data
#         serializer = AktyorSeializer(data=aktyor)
#         if serializer.is_valid():
#             Aktyor.objects.create(
#                 ism=serializer.validated_data.get("ism"),
#                 tugilgan_yili = serializer.validated_data.get("tugilgan_yili"),
#                 jins = serializer.validated_data.get("jins"),
#                 davlat = serializer.validated_data.get("davlat")
#             )
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AktyorDetailView(APIView):
    def get(self, request, pk):
        if len(Aktyor.objects.filter(id=pk)) == 1:
            serializer = AktyorSeializer(Aktyor.objects.get(id=pk))
            return Response(serializer.data)
        return Response({"xabar":"Bunday id da aktyor yo'q"})

    def put(self, request, pk):
        aktyor = Aktyor.objects.get(id=pk)
        serializer = AktyorSeializer(aktyor, data=request.data)
        if serializer.is_valid():
            aktyor.ism = serializer.validated_data.get("ism")
            aktyor.davlat = serializer.validated_data.get("davlat")
            aktyor.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TarifAPIView(APIView):
    def get(self, request):
        tarif = Tarif.objects.all()
        serializer = TarifSerializer(tarif, many=True)
        return Response(serializer.data)

    def post(self, request):
        tarif = request.data
        serializer = TarifSerializer(data=tarif)
        if serializer.is_valid():
            Tarif.objects.create(
                nom = serializer.validated_data.get("nom"),
                narx = serializer.validated_data.get("narx"),
                muddat = serializer.validated_data.get("muddat")
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TarifOchirishAPIView(APIView):
    def delete(self, request, pk):
        tarif = Tarif.objects.get(id=pk).delete()
        return Response({"xabar":"ochirildi"})

class TarifDetailView(APIView):
    def get(self, request, pk):
        if len(Tarif.objects.filter(id=pk)) == 1:
            serializer = TarifSerializer(Tarif.objects.get(id=pk))
            return Response(serializer.data)
        return Response({"xabar":"Bunday id da aktyor yo'q"})

    def put(self, request, pk):
        tarif = Tarif.objects.get(id=pk)
        serializer = TarifSerializer(tarif, data=request.data)
        if serializer.is_valid():
            tarif.nom = serializer.validated_data.get("nom")
            tarif.narx = serializer.validated_data.get("narx")
            tarif.muddat = serializer.validated_data.get("muddat")
            tarif.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class KinoAPIViews(APIView):
#     def get(self, request):
#         kino = Kino.objects.all()
#         serializer = KinoSerializer(kino, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         kino = request.data
#         serializer = KinoCreateSerializer(data=kino)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class KinoDetailAPIView(APIView):
#     def get(self, request, pk):
#         if len(Kino.objects.filter(id=pk)) == 1:
#             serializer = KinoSerializer(Kino.objects.get(id=pk))
#             return Response(serializer.data)
#         return Response({"xabar":"Bunday id dagi kino yoq"})
#
#     def put(self, request, pk):
#         kino = Kino.objects.get(id=pk)
#         serializer = KinoCreateSerializer(kino, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class KinoViewSet(ModelViewSet):
    queryset = Kino.objects.all()
    serializer_class = KinoSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, ]
    search_fields = ("nom", )
    ordering_fields = ("yil", )

    # def get_queryset(self):
    #     soz = self.request.query_params.get("qidirish")
    #     if soz is None or soz == "":
    #         natija = Kino.objects.all()
    #     else:
    #         natija = Kino.objects.filter(nom__contains=soz)
    #     return natija

    @action(detail=True)
    def aktyorlar(self, request, pk):
        actors =  Kino.objects.get(id=pk).aktyorlar.all()
        serializer = AktyorSeializer(actors, many=True)
        return Response(serializer.data)

class IzohViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Izoh.objects.all()
    serializer_class = IzohSerializer

    def get_queryset(self):
        queryset = Izoh.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class AktyorViewSet(ModelViewSet):
    queryset = Aktyor.objects.all()
    serializer_class = AktyorSeializer
    filter_backends = [filters.OrderingFilter, ]
    search_fields = ("nom", "albom__nom", )
    ordering_fields = ("tugilgan_yili", )

    def get_queryset(self):
        soz = self.request.query_params.get("qidirish")
        if soz is None or soz == "":
            natija = Aktyor.objects.all()
        else:
            natija = Aktyor.objects.filter(ism__contains=soz)
        return natija
