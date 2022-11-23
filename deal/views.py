from deal.models import Deal
from deal.serializers import DealSerializer, DealUpdateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404

class DealView(APIView):
    def post(self, request):
        serializer = DealSerializer(data=request.data)
        if serializer.is_valid():
            #TODO from_user_id를 body에 담아 request.data에서 꺼내올 수 있는가?
            serializer.save(to_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        deals = Deal.objects.all()
        serializer = DealSerializer(deals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DealDetailView(APIView):
    def get(self, request, id):
        deal = get_object_or_404(Deal, id=id)
        serializer = DealSerializer(deal)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        deal = get_object_or_404(Deal, id=id)
        serializer = DealUpdateSerializer(deal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"거래내역이 수정되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        deal = get_object_or_404(Deal, id=id)
        serializer = DealUpdateSerializer(deal, data={"status":0})
        if serializer.is_valid():
            serializer.save()
        return Response({"message":"삭제 되었습니다."}, status=status.HTTP_204_NO_CONTENT)