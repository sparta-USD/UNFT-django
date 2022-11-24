from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Unft
from .serializers import *
from django.contrib.auth import get_user_model

# Create your views here.
class UnftList(APIView):
    def get (self, request):
        all_unft = Unft.objects.all().order_by('-created_at')
        serializer = UnftSerializer(all_unft, many=True)
        return Response(serializer.data)

    def post (self, request):
        # request_user = request.user        # 로그인한 유저
        request_user = get_user_model().objects.get(id=1)  # 로그인한 유저(임시 1번 유저)
        request.data.update({'creator': request_user.id, 'owner': request_user.id})
        serializer = UnftCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnftDetail(APIView):
    def get_object(self, id):
        try:
            return Unft.objects.get(id=id)
        except Unft.DoesNotExist:
            raise Http404

    def get (self, request, id):
        target_unft = self.get_object(id)
        serializer = UnftSerializer(target_unft)
        return Response(serializer.data)

    def put (self, request, id):
        target_unft = self.get_object(id)
        # request_user = request.user        # 로그인한 유저
        request_user = get_user_model().objects.get(id=1)  # 로그인한 유저(임시 1번 유저)
        target_deal_count = 1              # 거래내역(임시 0건)

        # 1. 거래내역 0건 & 크리에이터 & 소유자 일 경우만 [제목,설명,판매상태,판매가] 수정 가능
        if(not target_deal_count and target_unft.creator==request_user and target_unft.owner==request_user):
            serializer = UnftUpdateAllSerializer(target_unft, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # 2. 소유자 일 경우만 [판매상태,판매가] 수정 가능
        elif(target_unft.owner==request_user):
            serializer = UnftUpdateStatusSerializer(target_unft, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # 3. 그외 수정 불가
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    def delete (self, request, id):
        target_unft = self.get_object(id)
        # request_user = request.user        # 로그인한 유저
        request_user = get_user_model().objects.get(id=1)  # 로그인한 유저(임시 1번 유저)
        target_deal_count = 1              # 거래내역(임시 0건)

        # 거래내역 0건 & 크리에이터 & 소유자 일 경우만 삭제 가능
        if(not target_deal_count and target_unft.creator==request_user and target_unft.owner==request_user):
            target_unft.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)