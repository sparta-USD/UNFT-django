from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Unft
from .serializers import UnftSerializer,UnftCreateSerializer
from django.contrib.auth import get_user_model

# Create your views here.
class UnftList(APIView):
    def get (self, request):
        all_unft = Unft.objects.all().order_by('-created_at')
        serializer = UnftSerializer(all_unft, many=True)
        return Response(serializer.data)

    def post (self, request):
        request_user = get_user_model().objects.get(id=1)
        request.data.update({'creator': request_user.id, 'owner': request_user.id})
        serializer = UnftCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
