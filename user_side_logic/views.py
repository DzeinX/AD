from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from AD import settings

from.models import User


def main_page(request):
    if request.method == "GET":
        context = {}
        return render(request, "user_side_logic/main_page.html", context)

    if request.method == "POST":
        email = request.POST["email"].strip()
        user_name = request.POST["first-name"].strip()
        user_message = request.POST["user-message"].strip()

        if not (email and user_message and user_name) or '@' not in email:
            msg = "Вы не заполнили некоторые поля, заполните их и мы сможем с вами связаться!"
            messages.add_message(request, messages.WARNING, msg)
            return redirect(reverse('main_page') + '#contacts')

        try:
            send_message(request, user_name, user_message, email)  # Отправка сообщения нам
            send_message_to_user(request, email)  # Отправка сообщения пользователю
            msg = "Сообщение успешно отправлено. Мы вам напишем в ближайшее время!"
            messages.add_message(request, messages.SUCCESS, msg)
        except Exception as e:
            msg = "По техническим причинам сообщение не удалось отправить. Возможно была указана не правильная почта. " \
                  "Просим прощения за предоставленные неудобства"
            messages.add_message(request, messages.ERROR, msg)

        return redirect(reverse('main_page') + '#contacts')

    return redirect('main_page')


def send_message(request, user_name, message, user_mail, sent_to=None):
    if sent_to is None:
        sent_to = ['ProVad2017@yandex.ru']  # TODO: Указать почты, на которые будут приходить письма от пользователей
    send_mail(
        f"Новое сообщение от {user_name} - пользователя сайта Рекламы!",
        "Почта пользователя: " + user_mail + f"<br>Сообщение пользователя {user_name}: " + message,
        settings.EMAIL_HOST_USER,
        sent_to,
        fail_silently=False,
    )


def send_message_to_user(request, sent_to, message=''):
    contacts_footer = f"Так же вы можете связаться с нами сами: <br>1) Телефон: +7 *** *** ** **<br>2) Почта: " \
                      f"<a href='mailto:#'>****@mail.ru</a><br><br> Или по ссылкам: <a href='#'>telegram</a> или <a " \
                      f"href='#'>whatsapp</a>"
    if message:
        message += "<br>" + contacts_footer

    send_mail(
        f"Спасибо что написали нам. Мы ответим вам в ближайшее время!",
        message if message else contacts_footer,
        settings.EMAIL_HOST_USER,
        [sent_to],
        fail_silently=False,
    )


def login_page(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user_login = User.objects.filter(email=username, password=password).first()

        if user_login is not None:
            login(request, user_login)
            user = User.objects.filter(username=user_login).first()
            if user is not None:
                user.student = True
                user.save()
            return redirect('main_page')
        else:
            messages.error(request, 'Неверный логин или пароль')
            return redirect('login_page')
    else:
        if request.user.is_authenticated:
            return redirect('main_page')
        else:
            return render(request, "user_side_logic/login.html", {})


def logout_page(request):
    logout(request)
    return redirect('login_page')
