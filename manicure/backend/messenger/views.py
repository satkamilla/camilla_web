from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, CreateConversationSerializer
from authorization.models import CustomUser
import logging
from django.db.models import Q

logger = logging.getLogger(__name__)

class UserConversationsView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

class ConversationMessagesView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        return Message.objects.filter(conversation_id=conversation_id)

    def perform_create(self, serializer):
        conversation = Conversation.objects.get(id=self.kwargs['conversation_id'])
        serializer.save(conversation=conversation, sender=self.request.user)

class CreateMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            logger.error(f'Conversation {conversation_id} does not exist.')
            return Response({'detail': 'Conversation not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f'Error fetching conversation: {str(e)}')
            return Response({'detail': 'Internal server error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            data = request.data.copy()
            data['conversation'] = conversation.id
            data['sender'] = request.user.id
            logger.info(f'Data for message creation: {data}')  # Log the data being passed to the serializer
            serializer = MessageSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            logger.error(f'Serialization error: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Error saving message: {str(e)}')
            return Response({'detail': 'Internal server error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            logger.error(f'Conversation {conversation_id} does not exist.')
            return Response({'detail': 'Conversation not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f'Error fetching conversation: {str(e)}')
            return Response({'detail': 'Internal server error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            data = request.data.copy()
            data['conversation'] = conversation.id
            data['sender'] = request.user.id
            serializer = MessageSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            logger.error(f'Serialization error: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Error saving message: {str(e)}')
            return Response({'detail': 'Internal server error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    
class CreateConversationView(generics.CreateAPIView):
    serializer_class = CreateConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        try:
            other_user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        conversation, created = Conversation.objects.get_or_create(
            participants__in=[request.user, other_user],
            defaults={'participants': [request.user, other_user]}
        )

        if not created:
            conversation.participants.add(request.user, other_user)

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    
    

class CreateOrGetConversationView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConversationSerializer

    def post(self, request):
        other_user_id = request.data.get('other_user_id')
        if not other_user_id:
            return Response({"detail": "other_user_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        other_user = CustomUser.objects.get(id=other_user_id)
        user = request.user

        conversation = Conversation.objects.filter(
            Q(participants=user) & Q(participants=other_user)
        ).distinct().first()

        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.add(user, other_user)

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_200_OK)