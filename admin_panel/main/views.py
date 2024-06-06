from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BroadcastForm
from .models import User
from aiogram import Bot
import asyncio

import config


bot = Bot(token=config.BOT_TOKEN)


async def send_message(user_ids, text):
    for user in user_ids:
        await bot.send_message(user.user_id, text)
        await asyncio.sleep(0.075)


def broadcast_view(request):
    if request.method == 'POST':
        form = BroadcastForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            users = User.objects.all()
            # users = User.objects.filter(username='salamaIeykum')
            
            # for user in users:

            asyncio.run(send_message(users, message))
            messages.success(request, 'Broadcast sent successfully!')
            return redirect('broadcast')
    else:
        form = BroadcastForm()
    return render(request, 'broadcast.html', {'form': form})


def admin_home(request):
    return render(request, 'admin_home.html')


def users_list(request):
    users = User.objects.all()
    return render(request, 'users_list.html', {'users': users})