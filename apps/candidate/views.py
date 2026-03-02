from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import AdminOrReadOnly, IsAdminRole
from apps.common.pagination import CustomPagination

from .models import Candidate
from .serializers import CandidateCreateSerializer, CandidateSearchSerializer


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


class CandidateSearchView(ListAPIView):

    serializer_class = CandidateSearchSerializer
    permission_classes = [IsAuthenticated, AdminOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Candidate.objects.all()

        q = self.request.query_params.get("q")
        status_param = self.request.query_params.getlist("status")
        created_from = self.request.query_params.get("createdFrom")
        created_to = self.request.query_params.get("createdTo")
        has_link = self.request.query_params.get("hasLink")
        sort = self.request.query_params.get("sort", "recent")

        # Search by name/email
        if q:
            queryset = queryset.filter(Q(name__icontains=q) | Q(email__icontains=q))

        # Filter by status (multiple allowed)
        if status_param:
            queryset = queryset.filter(current_status__in=status_param)

        # Date filtering
        if created_from:
            queryset = queryset.filter(created_at__date__gte=created_from)

        if created_to:
            queryset = queryset.filter(created_at__date__lte=created_to)

        # Has link filter
        if has_link == "true":
            queryset = queryset.exclude(link__isnull=True).exclude(link="")
        elif has_link == "false":
            queryset = queryset.filter(Q(link__isnull=True) | Q(link=""))

        # Sorting
        if sort == "recent":
            queryset = queryset.order_by("-created_at")
        elif sort == "status_then_recent":
            queryset = queryset.order_by("current_status", "-created_at")

        return queryset
