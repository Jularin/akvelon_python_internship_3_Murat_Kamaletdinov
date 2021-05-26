from django.contrib.auth import logout
from django.contrib.auth.models import AnonymousUser
from django.core.validators import RegexValidator
from django.db.models import QuerySet, Sum
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin, ListModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from task.models import CustomUser, Transaction
from task.serializers.transaction_serializers import TransactionSerializer, TransactionOutputSerializer, \
    TransactionSortByDateSerializer, TransactionSortByDateOutputSerializer
from task.serializers.user_serializers import UserSerializer, CreateUserSerializer
from task.services.user import validate_create_user_data


class UserViewSet(
    GenericViewSet,
):
    """Api view with basic CRUD"""

    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        """Create partial update for patch API method"""
        instance = self.get_object()

        if isinstance(request.user, AnonymousUser):
            # checking is user is anonymous
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if instance != self.request.user:
            # checking is user trying to patch another user
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @swagger_auto_schema(request_body=CreateUserSerializer)
    def create(self, request: Request, *args, **kwargs) -> Response:
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                ["Forgot to enter something!"], status=status.HTTP_400_BAD_REQUEST
            )
        error_messages = validate_create_user_data(
            request.data
        )  # check if data is legit

        if error_messages:
            return Response(error_messages, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create_user(
            email,
            password,
            first_name=request.data.get("first_name"),
            last_name=request.data.get("last_name"),
        )
        user.save()
        return Response(self.serializer_class(user, context={"request": request}).data)

    @swagger_auto_schema(operation_id="user_read", request_body=no_body, responses={200: UserSerializer()})
    @action(methods=["GET"], url_path="", detail=False, permission_classes=(IsAuthenticated,))
    def get_current_user(self, request: Request) -> Response:
        return Response(self.serializer_class(self.request.user, context={"request": request}).data)

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        try:
            if CustomUser.objects.get(pk=request.parser_context["kwargs"]["pk"]) != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        request.user.delete()
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionViewSet(GenericViewSet, DestroyModelMixin, RetrieveModelMixin):
    queryset = Transaction.objects.all()
    serializer_class = TransactionOutputSerializer
    permission_classes = (IsAuthenticated,)

    def _get_queryset_by_date(self,
                              user: Request.user,
                              start_date: str = None,
                              end_date: str = None) -> QuerySet:
        """Transactions queryset sorted by date"""
        if start_date and end_date:
            transactions = self.queryset.filter(date__range=[start_date, end_date])
        elif start_date and not end_date:
            transactions = self.queryset.filter(date__gte=start_date)
        elif not start_date and end_date:
            transactions = self.queryset.filter(date__lte=end_date)
        else:
            transactions = self.queryset.filter(user=user)
        return transactions

    @swagger_auto_schema(request_body=TransactionSerializer, responses={201: TransactionOutputSerializer()})
    def create(self, request: Request, *args, **kwargs) -> Response:
        if self.get_object().user != self.request.user:
            # checking is user trying to check another user transaction
            return Response(status=status.HTTP_403_FORBIDDEN)

        amount = request.data.get('amount')
        transaction = Transaction.objects.create(user=request.user, amount=amount)

        return Response(TransactionOutputSerializer(transaction).data)

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        return DestroyModelMixin.destroy(self, request, *args, **kwargs)

    @swagger_auto_schema(request_body=no_body)
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        if self.get_object().user != self.request.user:
            # checking is user trying to check another user transaction
            return Response(status=status.HTTP_403_FORBIDDEN)
        return RetrieveModelMixin.retrieve(self, request, *args, **kwargs)

    def list(self, request: Request, *args, **kwargs) -> Response:
        return Response(self.serializer_class(Transaction.objects.filter(user=request.user), many=True).data,
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=TransactionSerializer, responses={200: TransactionOutputSerializer()})
    def partial_update(self, request: Request, *args, **kwargs):
        if self.get_object().user != self.request.user:
            # checking is user trying to check another user transaction
            return Response(status=status.HTTP_403_FORBIDDEN)
        if not request.data.get('amount'):
            return Response(
                ["Forgot to enter something!"], status=status.HTTP_400_BAD_REQUEST
            )
        try:
            transaction = Transaction.objects.get(pk=request.parser_context["kwargs"]["pk"])
        except Transaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        transaction.amount = request.data.get('amount')
        transaction.save()

        return Response(TransactionOutputSerializer(transaction).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="sort_transactions_by_date",
                         request_body=TransactionSortByDateSerializer,
                         responses={200: TransactionOutputSerializer(many=True)})
    @action(methods=["POST"], detail=False)
    def sort_transactions_by_date(self, request: Request, *args, **kwargs) -> Response:
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        # TODO add date validation
        transactions = self._get_queryset_by_date(request.user, start_date, end_date)
        return Response(TransactionOutputSerializer(transactions, many=True).data)

    @swagger_auto_schema(operation_id="view_sum_of_transactions by date",
                         request_body=TransactionSortByDateSerializer,
                         responses={200: TransactionSortByDateOutputSerializer()})
    @action(methods=["POST"], detail=False)
    def view_sum_of_transactions_by_date(self, request: Request, *args, **kwargs):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        transactions = self._get_queryset_by_date(request.user, start_date, end_date)
        summ = transactions.values().aggregate(sum=Sum('amount'))['sum']

        serializer = TransactionSortByDateOutputSerializer(data={
            'start_date': start_date if start_date else None,
            'end_date': end_date if end_date else None,
            'sum': summ})
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

