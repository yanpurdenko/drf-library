from datetime import date
from typing import Type

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.authentication import JWTAuthentication

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer, BorrowingListRetrieveSerializer


class BorrowingsPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100


class BorrowingsViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    pagination_class = BorrowingsPagination
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()

        is_active = self.request.query_params.get("is_active", None)

        if is_active == "1":
            queryset = queryset.filter(actual_return_date__isnull=True)
        elif is_active == "0":
            queryset = queryset.filter(actual_return_date__isnull=False)

        if self.request.user.is_staff:
            user_id = self.request.query_params.get("user_id", None)
            if user_id:
                queryset = queryset.filter(user_id=user_id)
                return queryset

        return queryset.filter(user_id=self.request.user)

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action in ("list", "retrieve"):
            return BorrowingListRetrieveSerializer

        return super().get_serializer_class()

    @action(
        detail=True, methods=["POST"], url_path="return", serializer_class=Serializer
    )
    def return_book(self, request: Request, pk: int = None) -> Response:
        borrowing = self.get_object()
        if borrowing.actual_return_date is not None:
            return Response(
                {"message": "This borrowing is already returned!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        borrowing.actual_return_date = date.today()
        borrowing.book_id.inventory += 1
        borrowing.save()
        borrowing.book_id.save()

        return Response(BorrowingSerializer(borrowing).data, status=status.HTTP_200_OK)

    def perform_create(self, serializer: BorrowingSerializer):
        return serializer.save(user_id=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "user_id",
                type={"type": "list", "items": {"type": "int"}},
                description="Filter by user id (ex. ?user_id=id)"
            ),
            OpenApiParameter(
                "is_active",
                type=int,
                description="Filter by user_id & is_active (ex. ?is_active=(1/0))",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
