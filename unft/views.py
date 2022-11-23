from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Unft
from .serializers import UnftSerializer
# Create your views here.
class UnftList(APIView):
    def get (self, request):
        all_unft = Unft.objects.all().order_by('-created_at')
        serializer = UnftSerializer(all_unft, many=True)
        return Response(serializer.data)
