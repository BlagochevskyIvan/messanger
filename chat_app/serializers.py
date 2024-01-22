from rest_framework import serializers

from .models import Dialog, Content, Message

class DialogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dialog
        fields = ('id','name','avatar')

class ContentSerializer(serializers.ModelSerializer):
    dialog_info = DialogSerializer()

    class Meta:
        model = Content
        fields = ('id', 'dialog', 'dialog_info', 'message')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'type_message', 'text', 'attached_photo','attached_file', 'author')
