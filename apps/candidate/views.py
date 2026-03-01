from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminRole

from .serializers import CandidateCreateSerializer


class CandidateCreateView(APIView):

    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request):
        serializer = CandidateCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        candidate = serializer.save()

        return Response(
            {"id": candidate.id, "detail": "Candidate created successfully"},
            status=status.HTTP_201_CREATED,
        )
