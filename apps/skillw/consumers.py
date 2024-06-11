import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, Themes, Courses_Of_User, Mentors
from datetime import datetime
from channels.layers import get_channel_layer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.theme_id = self.scope['url_route']['kwargs']['id']
        self.room_group_name = f'chat_{self.theme_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Load previous messages
        messages = await self.get_previous_messages(self.theme_id)
        grouped_messages = self.group_messages_by_date(messages)
        
        for date, msgs in grouped_messages.items():
            await self.send(text_data=json.dumps({
                'date': date,
                'messages': msgs,
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = self.scope["user"]

        theme = await self.get_theme(self.theme_id)
        user_courses = await self.get_user_courses(sender)

        if not await self.user_in_courses(user_courses, theme):
            await self.close()
            return

        receiver = await self.get_receiver(user_courses, theme, sender)

        msg = await self.create_message(theme, sender, receiver, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'time': msg.timestamp.strftime('%H:%M:%S'),  # Добавляем время отправки
            }
        )
   
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        time = event['time']  # Получаем время отправки

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'time': time,  # Передаем время отправки
        }))

    @database_sync_to_async
    def get_theme(self, theme_id):
        return Themes.objects.get(id=theme_id)

    @database_sync_to_async
    def get_user_courses(self, user):
        mentor = Mentors.objects.filter(mentor=user).first()
        return list(Courses_Of_User.objects.filter(student=user) | Courses_Of_User.objects.filter(teacher=mentor))

    @database_sync_to_async
    def user_in_courses(self, user_courses, theme):
        return any(course.courses == theme.napravlenie for course in user_courses)

    @database_sync_to_async
    def get_receiver(self, user_courses, theme, sender):
        for course in user_courses:
            if course.courses == theme.napravlenie:
                if course.student == sender:
                    return course.teacher.mentor
                return course.student
        return None

    @database_sync_to_async
    def create_message(self, theme, sender, receiver, message):
        return Message.objects.create(theme=theme, sender=sender, receiver=receiver, content=message)

    @database_sync_to_async
    def get_previous_messages(self, theme_id):
        theme = Themes.objects.get(id=theme_id)
        return list(Message.objects.filter(theme=theme).order_by('timestamp').values('content', 'sender__username', 'timestamp'))

    def group_messages_by_date(self, messages):
        grouped_messages = {}
        for message in messages:
            date = message['timestamp'].strftime('%Y-%m-%d')
            time = message['timestamp'].strftime('%H:%M:%S')
            if date not in grouped_messages:
                grouped_messages[date] = []
            grouped_messages[date].append({
                'message': message['content'],
                'sender': message['sender__username'],
                'time': time,
            })
        return grouped_messages

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        await self.send(text_data=json.dumps({
            'message': 'New message received'
        }))
