from datetime import date, timedelta

from NewsPaper import settings
from news.models import Category, Posts, SubscribersUsers
from celery import shared_task
import time

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")

@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)


@shared_task
def last_post_week():
    start = date.today() - timedelta(7)
    finish = date.today()
    category = Category.objects.all()
    for cat in category:
        list_post = Posts.objects.filter(date__range=(start, finish), categories=cat.pk)
        print(list_post)
        subscrs_email = []
        print(cat)
        for usr in User.objects.all():
            user_email = SubscribersUsers.objects.filter(id_category=cat.pk, id_user=usr.pk)
            if user_email:
                subscrs_email.append(usr.email)
        print(subscrs_email)

        if list_post:
            html_content = render_to_string('week_post.html', {'posts': list_post, 'category': cat.name})

        msg = EmailMultiAlternatives(
            subject='Новости за неделю',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=subscrs_email
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task
def send_email(pk_, id_cat):
    post = Posts.objects.get(id=pk_)
    emails = User.objects.filter(category__id__in=id_cat).values('email').distinct()
    emails_list = [item['email'] for item in emails]
    html_content = render_to_string(
        'new_post_email.html',
        {
            'Post': post
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'{post.title}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=emails_list
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

#'celery -A NewsPaper worker -E -l INFO'

