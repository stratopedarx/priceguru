from core.api.models import ItemGroup, UserItem, OriginalItem, ItemPrice
from django.core.management.base import BaseCommand, CommandError
from core.user.models import User
from django.utils import timezone
import random


class Command(BaseCommand):
    help = 'Creates the same original item as the old (id) one only with a different price. For check service'

    def add_arguments(self, parser):

        parser.add_argument('new_item', type=int, nargs=1)

    def handle(self, *args, **options):
        if options['new_item']:
            try:
                item = OriginalItem.objects.get(id=options['new_item'][0])  # old original item
            except OriginalItem.DoesNotExist:
                raise CommandError("Select another id")
            new_item = OriginalItem.objects.create(article=item.article, title=item.title,
                                                   details=item.details, url=item.url + '1', source=item.source)
            random_base_price = random.randint(0, 10000)
            random_discount_price = random.randint(0, 10000)
            new_item_price = ItemPrice.objects.create(item=new_item, base_price=random_base_price,
                                                      discount_price=random_discount_price,
                                                      current_price=random_discount_price,
                                                      created_date=timezone.now(), currency=random_discount_price)
            # for each user who have old original item to assign a new original item
            for user in User.objects.filter(itemgroup__useritem__item__id=options['new_item'][0]):
                group = ItemGroup.objects.get(user__id=user.id)
                user_item = UserItem.objects.create(custom_name=new_item.title, item=new_item, group=group)

            self.stdout.write("Successfully created item with new id {}".format(new_item.id))
