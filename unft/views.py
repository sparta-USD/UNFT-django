from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Unft
from .serializers import *
from django.contrib.auth import get_user_model
import os
import shutil

import datetime
from django.utils import timezone

# Create your views here.
class UnftList(APIView):
    def get (self, request):
        all_unft = Unft.objects.all().order_by('-created_at')
        serializer = UnftSerializer(all_unft, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post (self, request):
        request_user = request.user        # 로그인한 유저
        request.data.update({'creator': request_user.id, 'owner': request_user.id})
        serializer = UnftCreateSerializer(data=request.data)
 
        if serializer.is_valid():
            serializer.save()
            
            last_unft = Unft.objects.last()
            base_image = last_unft.base_image
            style_image = last_unft.style_image
            
            # style transfer 실행 명령어
            os.system(f'python unft/cli.py media/{base_image} media/{style_image} -s 156 --initial-iterations 100')
            
            # 생성된 파일명 가져오기
            os.chdir('./media/unft/result_pass')
            result = os.listdir()[0]
            last_unft.result_image = f'unft/result/{result}'
            
            last_unft.save()
            shutil.move(result,'../result')
            os.chdir('./../../..')

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

        # 당일날 밤 12시에 쿠키 초기화
        tomorrow = datetime.datetime.replace(timezone.datetime.now(), hour=23, minute=59, second=0)
        expires = datetime.datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")
        
        add_cookies = ''

        # 쿠키 읽어서 hits 값이 있는 지 확인
        if request.COOKIES.get('hits') is not None:
            cookies = request.COOKIES.get('hits')
            cookies_list = cookies.split('|')
            if str(id) not in cookies_list:
                # 쿠키 생성할 내용 : 쿠키가 있어서 기존 내용에 보고있는 id 추가
                add_cookies = f'{cookies}|{id}'
                # 조회수 추가
                target_unft.hits +=1
                target_unft.save()
        else :
            # 쿠키 생성할 내용 : 쿠키가 없어서 보고있는 id만 추가
            add_cookies = id
            # 조회수 추가
            target_unft.hits +=1
            target_unft.save()

        serializer = UnftSerializer(target_unft)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        if add_cookies: # 쿠키생성 
            response.set_cookie('hits', add_cookies, expires=expires) # 쿠키 생성
        return response

    def put (self, request, id):
        target_unft = self.get_object(id)
        request_user = request.user        # 로그인한 유저
        target_deal_count = 0              # 거래내역(임시 0건)

        # 1. 거래내역 0건 & 크리에이터 & 소유자 일 경우만 [제목,설명,판매상태,판매가] 수정 가능
        if(not target_deal_count and target_unft.creator==request_user and target_unft.owner==request_user):
            serializer = UnftUpdateAllSerializer(target_unft, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # 2. 소유자 일 경우만 [판매상태,판매가] 수정 가능
        elif(target_unft.owner==request_user):
            serializer = UnftUpdateStatusSerializer(target_unft, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # 3. 그외 수정 불가
        return Response({"message":"접근 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
            
    def delete (self, request, id):
        target_unft = self.get_object(id)
        request_user = request.user        # 로그인한 유저
        target_deal_count = 1              # 거래내역(임시 0건)

        # 거래내역 0건 & 크리에이터 & 소유자 일 경우만 삭제 가능
        if(not target_deal_count and target_unft.creator==request_user and target_unft.owner==request_user):
            target_unft.delete()
            return Response({"message":"성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message":"접근 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
    
