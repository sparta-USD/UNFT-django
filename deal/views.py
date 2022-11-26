from deal.models import Deal
from deal.serializers import DealSerializer, DealUpdateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from django.db.models import Q
from unft.models import Unft
from users.models import User

class DealView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"message":"로그인이 필요합니다!"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # 이미 제안중인 거래내역이 있는지 확인
        isDeal = Deal.objects.filter(status=3, to_user=request.user, unft_id=request.data["unft"])
        if isDeal:
            return Response({"message":"이미 제안했습니다!"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = DealSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(to_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        # 서비스 전체 거래내역 조회
        if not request.GET:
            deals = Deal.objects.exclude(status=0).order_by("-updated_at")
            serializer = DealSerializer(deals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # 특정 작품 전체 거래내역 조회
        if "unft" in request.GET:
            unft_id = request.GET["unft"]
            specific_unft_deals = Deal.objects.filter(Q(unft=unft_id) & ~Q(status=0)).order_by("-updated_at")
            if not specific_unft_deals:
                return Response({"message":"거래/제안 내역이 없습니다."}, status=status.HTTP_200_OK)
            serializer = DealSerializer(specific_unft_deals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # 내 거래내역 조회
        if ("from_user" and "to_user" in request.GET) and (len(request.GET) == 2):
            from_user_is_me = request.GET["from_user"]
            to_user_is_me = request.GET["to_user"]
            specific_my_deals = Deal.objects.filter(
                                                    (Q(from_user=from_user_is_me)|Q(to_user=to_user_is_me))
                                                    & Q(status=1)
                                                    ).order_by("-updated_at")
            if not specific_my_deals:
                return Response({"message":"내 거래내역이 없습니다."}, status=status.HTTP_200_OK)
            serializer = DealSerializer(specific_my_deals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # 내가 받은 제안내역 조회
        if "from_user" in request.GET:
            from_user_is_me = request.GET["from_user"]
            specific_my_offerd = Deal.objects.filter(Q(from_user=from_user_is_me) & Q(status=3)).order_by("-updated_at")
            if not specific_my_offerd:
                return Response({"message":"받은 제안내역이 없습니다."}, status=status.HTTP_200_OK)
            serializer = DealSerializer(specific_my_offerd, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # 내가 제안한 내역 조회
        if "to_user" in request.GET:
            to_user_is_me = request.GET["to_user"]
            specific_my_offer = Deal.objects.filter(Q(to_user=to_user_is_me) & Q(status=3)).order_by("-updated_at")
            if not specific_my_offer:
                return Response({"message":"제안한 내역이 없습니다."}, status=status.HTTP_200_OK)
            serializer = DealSerializer(specific_my_offer, many=True)
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

class DealCompleteView(APIView):
    def put(self, request, id):
        if not request.user.is_authenticated:
            return Response({"message":"로그인이 필요합니다!"}, status=status.HTTP_401_UNAUTHORIZED)
        
        deal = get_object_or_404(Deal, id=id)
        if deal.from_user == request.user and int(request.data["status"]) == 1:
            serializer = DealUpdateSerializer(deal, data=request.data)
            if serializer.is_valid():
                serializer.save()
                unft_id = serializer.data["unft"]
                unft = get_object_or_404(Unft, id=unft_id)
                unft.owner = deal.to_user
                unft.save()
                
                from_user = get_object_or_404(User, id=deal.from_user.id)
                to_user = get_object_or_404(User, id=deal.to_user.id)
                from_user.usd += deal.price
                to_user.usd -= deal.price
                from_user.save()
                to_user.save()
                return Response({"message":"거래가 완료되었습니다."}, status=status.HTTP_200_OK)
        return Response({"message":"잘못된 요청입니다."}, status=status.HTTP_403_FORBIDDEN)
