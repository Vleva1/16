from django.core.management.base import BaseCommand, CommandError
from news.models import Posts, Category


class Command(BaseCommand):
    help = 'Подсказка вашей команды'

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории  yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))

        try:

            category1 = Category.objects.get(name = 'sport')
            q = Posts.objects.filter(category = category1)
            for b in q:
                b.delete()
            self.stdout.write(self.style.SUCCESS(
                f'Succesfully deleted all news from category '))  # в случае неправильного подтверждения говорим, что в доступе отказано
        except Posts.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category '))
