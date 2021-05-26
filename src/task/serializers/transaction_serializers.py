from rest_framework import serializers

from task.models import Transaction
from task.serializers.user_serializers import UserSerializer


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('amount',)


class TransactionOutputSerializer(serializers.ModelSerializer):
    """Serializer for transaction model"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'user', 'amount', 'date')


class TransactionSortByDateSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    class Meta:
        fields = (
          'start_date', 'end_date'
        )


class TransactionSortByDateOutputSerializer(TransactionSortByDateSerializer):
    sum = serializers.FloatField()

    class Meta:
        fields = TransactionSortByDateSerializer.Meta.fields + ('sum',)
