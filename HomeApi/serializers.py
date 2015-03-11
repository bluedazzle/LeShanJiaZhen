from HomeApi.models import *
from rest_framework import serializers

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback

class AssociatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Associator

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
