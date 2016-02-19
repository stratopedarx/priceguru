# -*- coding: utf-8 -*-
import random
from datetime import timedelta, date
from core.api.models import OriginalItem, ItemPrice, Partner, PartnerSource, ItemGroup, UserItem
from core.user.models import User
from django.core.management import BaseCommand
from django.utils.timezone import now
import calendar


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--yes-iam-sure", "-yes-iam", nargs="?", required=True,
                            help="If you not sure -> don't call this command")

    def handle(self, *args, **options):
        # get or create test partner object
        partner, is_created = Partner.objects.get_or_create(
            name="For Example",
            package='example'
        )

        print "Partner created:" if is_created else "Partner got from database:", partner

        # get or create test partnersource object
        partner_source, is_created = PartnerSource.objects.get_or_create(
            partner=partner,
            domain='example.com',
            scraper_name='example',
        )
        print "PartnerSource created:" if is_created else "PartnerSource got from database:", partner_source

        # get or create test OriginalItems (count=10)
        is_created = False
        if not partner_source.originalitem_set.exists():
            original_items = list(OriginalItem.objects.bulk_create(
                [OriginalItem(
                    source=partner_source,
                    url="http://example.com/%d/" % i,
                    article='Article %d' % i,
                    title='Example item #%d' % i,
                    details="Details for Example item #%d" % i)
                 for i in xrange(1, 6)]))
            is_created = True

        original_items = list(partner_source.originalitem_set.all())
        for i in original_items:
            print "OriginalItem got from database:" if not is_created else "OriginalItem created:", i

        user = User.objects.get(username='admin')

        is_created = False
        if not ItemGroup.objects.filter(user=user, group_name__icontains='Example group #').exists():
            item_groups = [
                ItemGroup(user=user, group_name='Example group #%d' % group_id)
                for group_id in xrange(1, 5)
            ]
            ItemGroup.objects.bulk_create(item_groups)
            is_created = True
        item_groups = list(ItemGroup.objects.filter(user=user, group_name__icontains='Example group #'))
        for i in item_groups:
            print "Group got from database:" if not is_created else "Group created:", i



        for group in item_groups:
            print "Group created:" if is_created else "Group got from database:", group

        for group in item_groups:
            if not group.useritem_set.exists():
                items_to_be_created = [
                    UserItem(custom_name="Custom user item #%s" % ids,
                             group=group, item=item)
                    for ids, item in enumerate(original_items, start=1)
                ]
                user_items = UserItem.objects.bulk_create(items_to_be_created)
                for item in user_items:
                    print "Item was created in group", group, "with item", item.item

        # create random price from each OriginalItem
        price_created = ItemPrice.objects.bulk_create(
            [ItemPrice(
                item=item,
                base_price=random.randint(0, 10000),
                discount_price=random.randint(0, 10000),
                current_price=random.randint(0, 10000),
            ) for item in original_items])

        for new_price_item in price_created:
            print "ItemPrice created:", new_price_item

        print "Finished!"
