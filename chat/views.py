from django.shortcuts import render
import string    
import random

def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    S = 10  # number of characters in the string.  
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
    name=str(ran) #Generated radom string but we can use session to store user name
    print(name)
    return render(request, 'chat/room.html', {
        'room_name': room_name,'username':name
    })

from rest_framework.views import APIView
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import random
from .models import UserStatus


class UserStatusAPI(APIView):
    def get(self, request,user_name):
        obj=UserStatus.objects.get(name=user_name)
        name=obj.name
        status=obj.status
        data={"name":name,"status":status}
        channel_layer = get_channel_layer()
        print(user_name)
        #Send Data to chennel 
        async_to_sync(channel_layer.group_send)(
            user_name,
            {
                'type': 'websocket.send',
                'message': data
            }
        )
        return Response([])