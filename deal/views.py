from deal.models import Deal
from deal.serializers import DealSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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