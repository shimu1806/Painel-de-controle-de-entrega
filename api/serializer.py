from rest_framework import serializers
from .models import Produto

class Produto_serializer(serializers.ModelSerializer):
    class Meta:
        model   = Produto
        fields  = '__all__'