from datetime import date

from django.db.models import QuerySet
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer


class BorrowingsViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

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

    @action(detail=True, methods=["POST"], url_path="return", serializer_class=Serializer)
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
        return serializer.save(user=self.request.user)
