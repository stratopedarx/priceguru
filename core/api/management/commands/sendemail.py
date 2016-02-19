from django.core.management.base import BaseCommand, CommandError
from core.api.models import OriginalItem, ItemPrice
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from core.user.models import User
from django.utils import timezone
import datetime


class Command(BaseCommand):
    help = 'sending mail to users whose prices was changed'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--email', '-email',
                            type=str,
                            required=False,
                            help='send mail to check')
        parser.add_argument('--id', '-id',
                            type=int,
                            nargs='+',
                            required=False,
                            help='send email to all users who signed him')
        parser.add_argument('--send_all', '-send_all',
                            required=False,
                            help='for battle server')
        parser.add_argument('--dry_run', '-dry_run',
                            required=False,
                            help='displays list of items which prices was changed and email`s users who signed on this items')

    def send_email_user(self, user, change_prices, user_email=None):

        email = get_template('api/email.html')
        data = Context({'username': user.username, 'change_prices': change_prices})
        if user_email is not None:
            subject, from_email, to = 'Hello, world', 'stratopedarx@mail.ru', user_email
        else:
            subject, from_email, to = 'Hello, world', 'stratopedarx@mail.ru', user.email
        html_email = email.render(data)
        msg = EmailMultiAlternatives(subject, html_email, from_email, [to])
        msg.attach_alternative(html_email, 'text/html')
        msg.send()

    def handle(self, *args, **options):

        if options['email']:
            try:
                user = User.objects.get(email=options['email'])
            except User.DoesNotExist:
                raise CommandError("User does not exist")
            # return the last some published items
            last_items = OriginalItem.objects.filter(
                    itemprice__created_date__gte=timezone.now() - datetime.timedelta(days=1)).order_by(
                    '-itemprice__created_date')
            # compare price last items with other
            change_prices = {}
            for item in last_items:
                if item.title in change_prices: continue
                last_item_price = ItemPrice.objects.get(item__id=item.id)  # take item_price each item
                try:
                    same_item = ItemPrice.objects.filter(item_id__title=item.title).exclude(
                            id=last_item_price.id).order_by(
                            '-created_date')[:1].get()
                except ItemPrice.DoesNotExist:
                    continue
                # compare prices
                if last_item_price.base_price != same_item.base_price:
                    new_base_price = last_item_price.base_price
                    new_discount_price = last_item_price.discount_price
                    old_base_price = same_item.base_price
                    old_discount_price = same_item.discount_price
                    item = item.title
                    change_prices[item] = (old_base_price, new_base_price, old_discount_price, new_discount_price)
            if len(change_prices) == 0:
                self.stdout.write("The prices have not changed")
            # if there is an option 'send_all' then send email, else print to stdout
            if options['send_all']:
                self.send_email_user(user, change_prices, options['email'])
                self.stdout.write("The message is successfully sent to %s" % options['email'])
            else:
                for key, value in change_prices.items():
                    self.stdout.write("The base price %s has changed from %s to %s." % (key, value[0], value[1]))
                    self.stdout.write("The discount price has changed form %s to %s." % (value[2], value[3]))
                    self.stdout.write("=" * 80)

        if options['id']:
            change_prices = {}
            try:
                original_item = OriginalItem.objects.get(id=options['id'][0])
                new_item_price = ItemPrice.objects.get(item_id__id=options['id'][0])
                old_item_price = ItemPrice.objects.filter(item_id__title=original_item.title).order_by(
                        'created_date')[:1].get()
            except OriginalItem.DoesNotExist, ItemPrice.DoesNotExist:
                raise CommandError("Select another id")

            try:
                users = User.objects.filter(itemgroup__useritem__item_id__id=options['id'][0])
            except TypeError:
                raise CommandError("No one signed for the item")

            # compare prices
            if new_item_price.base_price != old_item_price.base_price:
                change_prices[original_item.title] = (old_item_price.base_price, new_item_price.base_price,
                                                      old_item_price.discount_price, new_item_price.discount_price)
                # if there is an option 'send_all' then send email, else print to stdout
                if options['send_all']:
                    # send message for each user
                    for user in users:
                        self.send_email_user(user, change_prices)
                    self.stdout.write("The messages successfully sent to {} users.".format(len(users)))
                else:
                    for key, value in change_prices.items():
                        self.stdout.write("The base price %s has changed from %s to %s." % (key, value[0], value[1]))
                        self.stdout.write("The discount price has changed form %s to %s." % (value[2], value[3]))
                        self.stdout.write("Users signed for the item:")
                    for user in users:
                        self.stdout.write("user: %s with email %s" % (user.username, user.email))
                    print "=" * 80
            else:
                self.stdout.write("The price has not changed")

        if options['dry_run']:
            last_items = OriginalItem.objects.filter(
                    itemprice__created_date__gte=timezone.now() - datetime.timedelta(days=1)).order_by(
                    '-itemprice__created_date')
            # compare price last items with other
            change_prices = []
            for item in last_items:
                if item.title in change_prices: continue
                last_item_price = ItemPrice.objects.get(item__id=item.id)  # take item_price each item
                try:
                    same_item = ItemPrice.objects.filter(item_id__title=item.title).exclude(
                            id=last_item_price.id).order_by(
                            '-created_date')[:1].get()
                except ItemPrice.DoesNotExist:
                    continue
                # compare prices and stdout
                if last_item_price.base_price != same_item.base_price:
                    change_prices.append(item.title)  # for check
                    self.stdout.write(
                            "The price %s has changed from %s to %s->>>" % (item.title, same_item.base_price,
                                                                            last_item_price.base_price))
                    for user in User.objects.filter(itemgroup__useritem__item_id__id=item.id):
                        self.stdout.write("%s" % user.email)
                    self.stdout.write("=" * 80)
            # if prices have not changed
            if len(change_prices) == 0:
                self.stdout.write("The prices have not changed")

        self.stdout.write("Use --help")
