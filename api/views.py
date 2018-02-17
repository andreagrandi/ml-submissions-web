from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.serializers import UserSerializer
from api.serializers import SubmissionSerializer
from api.models import Submission


class UserCreate(APIView):
    """
    Creates the user.
    """

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)


class SubmissionUploadView(generics.ListCreateAPIView):

    parser_classes = (MultiPartParser, FormParser)
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user,
            datafile=self.request.data.get('datafile'))
