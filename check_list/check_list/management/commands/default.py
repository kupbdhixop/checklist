from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from check_list.models import Checklist, Task

class Command(BaseCommand):
    help = 'default users to use'

    def handle(self, *args, **options):
        """
        create default bob and alice users with some checklists"
        """

	bob, created = User.objects.get_or_create(username='bob', email='bob@bob.com')
	bob.set_password('bob')
        bob.save()

        if created:
            cl = Checklist.objects.create(name="Todo", description="various items todo", owner=bob)
            task1 = Task.objects.create(description="wash the dishes", owner=bob, checklist=cl)
            task2 = Task.objects.create(description="party hard", owner=bob, checklist=cl)

	alice, created = User.objects.get_or_create(username='alice', email='alice')
	alice.set_password('alice')
        alice.save()

        if created:
            cl = Checklist.objects.create(name="Todo", description="various items todo", owner=alice)
            task1 = Task.objects.create(description="take out the garbage", owner=alice, checklist=cl)
            task2 = Task.objects.create(description="mow the lawn", owner=alice, checklist=cl)

        print('default data created. starting server.')
