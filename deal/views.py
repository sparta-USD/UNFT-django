from deal.models import Deal
from deal.serializers import DealSerializer, DealUpdateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from django.db.models import Q

class DealView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"message":"로그인이 필요합니다!"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # 이미 제안중인 거래내역이 있는지 확인
        isDeal = Deal.objects.filter(status=3, to_user=request.user)
        if isDeal:
            return Response({"message":"이미 제안했습니다!"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = DealSerializer(data=request.data)
        if serializer.is_valid():
            #TODO from_user_id를 body에 담아 request.data에서 꺼내올 수 있는가?
            serializer.save(to_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        deals = Deal.objects.exclude(status=0)
        serializer = DealSerializer(deals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DealDetailView(APIView):
    def get(self, request, id):
        deal = get_object_or_404(Deal, id=id)
        serializer = DealSerializer(deal)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        if not request.user.is_authenticated:
            return Response({"message":"로그인이 필요합니다!"}, status=status.HTTP_401_UNAUTHORIZED)
        
        deal = get_object_or_404(Deal, id=id)
        if deal.to_user == request.user or deal.from_user == request.user: # 요청한 유저가 판매자 또는 구매자인지 검증하는 코드
            serializer = DealUpdateSerializer(deal, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"거래내역이 수정되었습니다."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, id):
        if not request.user.is_authenticated:
            return Response({"message":"로그인이 필요합니다!"}, status=status.HTTP_401_UNAUTHORIZED)

        deal = get_object_or_404(Deal, id=id)
        if deal.to_user == request.user:
            serializer = DealUpdateSerializer(deal, data={"status":0})
            if serializer.is_valid():
                serializer.save()
            return Response({"message":"삭제 되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)