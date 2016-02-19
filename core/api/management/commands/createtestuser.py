from django.core.management.base import BaseCommand, CommandError
from core.user.forms.user import RegisterForm
from django.contrib.auth import authenticate
from core.api.models import ItemGroup, UserItem, OriginalItem, PartnerSource, Partner, ItemPrice
from django.utils import timezone
from scrapers.mvideo import mvideo
from scrapers.citilink import citilink
import random
import re

# from scrapers.aliexpress import aliexpress
# from scrapers.ulmart import ulmart

test_dict = dict(#mvideo_link1='http://www.mvideo.ru/products/dvd-disk-media-avatar-40054563#shopdirections',
                 #mvideo_link2='http://www.mvideo.ru/products/telefon-provodnoi-philips-m110b-51-30021573',
                 #mvideo_link3='http://www.mvideo.ru/products/planshet-apple-ipad-pro-128gb-wi-fi-cellular-silver-ml2j2ru-a-30023722',
                 #mvideo_link4='http://www.mvideo.ru/products/fotovspyshka-nikon-sb-700-10002250',
                 #mvideo_link5='http://www.mvideo.ru/products/videoproektor-multimediinyi-acer-p1500-10005039',
                 citilink_link1='http://www.citilink.ru/catalog/photo_and_video/photo_filters/685070/',
                 citilink_link2='http://www.citilink.ru/catalog/computers_and_notebooks/gift_certificates/554178/',
                 citilink_link3='http://www.citilink.ru/catalog/large_and_small_appliances/small_appliances/kettles/991346/',
                 citilink_link4='http://www.citilink.ru/catalog/mobile/notebooks/956633/'
                 )


class Command(BaseCommand):
    help = 'Creates specified number of Users with a test set of original items'

    def add_arguments(self, parser):
        parser.add_argument('user_count', nargs=1, type=int)

    def handle(self, *args, **options):

        list_original_items = []
        # dictionary with the information about the original item from 3d party side
        for key, value in test_dict.items():
            if re.match(r'mvideo', key) is not None:
                my_item = mvideo.scrape(mvideo.validate_url(value))
            elif re.match(r'citilink', key):
                my_item = citilink.scrape(citilink.validate_url(value))

            # fill the fields of models
            # check the partner in Partner, if the partner is not in database so save new partner
            if len(Partner.objects.filter(name=my_item['url'].split('/')[2])) == 0:
                partner = Partner(name=my_item['url'].split('/')[2], package=my_item['url'].split('.')[1])
                partner.save()
            else:
                partner = Partner.objects.get(name=my_item['url'].split('/')[2])

            # check the new partner in PartnerSource, if the partner is not in database so save new partner_source
            if partner.id not in [sources.partner.id for sources in PartnerSource.objects.all()]:
                partner_source = PartnerSource(partner=partner, domain=my_item['url'].split('/')[2],
                                               scraper_name=my_item['url'].split('.')[1],
                                               platform=my_item['url'].split('/')[2])
                partner_source.save()
            else:
                partner_source = PartnerSource.objects.get(partner__id=partner.id)

            # check the new original item in OriginalItem, if the original item is not in database so save origin item
            if len(OriginalItem.objects.filter(article=my_item['data']['info']['article'])) == 0:
                original_item = OriginalItem(article=my_item['data']['info']['article'],
                                             title=my_item['data']['info']['title'],
                                             details=my_item['data']['info']['details'],
                                             url=my_item['url'], source=partner_source)
                original_item.save()
                list_original_items.append(original_item)  # for fill user_item

                # fill ItemPrice with new price of original item
                item_price = ItemPrice(item=original_item, base_price=my_item['data']['price']['base_price'],
                                       discount_price=my_item['data']['price']['discount_price'],
                                       current_price=my_item['data']['price']['discount_price'],
                                       created_date=timezone.now(), currency=my_item['data']['price']['discount_price'])
                item_price.save()
                # for check
                self.stdout.write("New item price save")

        # create test_users
        user_count = options['user_count'][0]
        for i in xrange(user_count):
            try:
                form = RegisterForm({'email': 'test_user{}@mail.ru'.format(i),
                                     'username': 'test_user{}'.format(i),
                                     'password': 'password{}'.format(i)})
            except ValueError:
                raise CommandError("user already exists")

            instance = form.save()
            instance.is_active = True
            instance.set_password(form.cleaned_data['password'])
            instance.save()
            user = authenticate(username=instance.username, password=form.cleaned_data['password'])
            self.stdout.write("save new user")
            # check and create user`s item group and save in database
            if len(ItemGroup.objects.filter(user__id=user.id)) == 0:
                item_group = ItemGroup(group_name='My group', user=user)
                item_group.save()
            else:
                item_group = ItemGroup.objects.get(user__id=user.id)

            # fill the Model of UserItem save in database
            list_num = []
            for num in xrange(9):
                num = random.randint(0, len(list_original_items) - 1)
                if num not in list_num:
                    user_item = UserItem(custom_name=list_original_items[num].title, item=list_original_items[num],
                                         group=item_group)
                    user_item.save()
                    self.stdout.write("create new user item")
                list_num.append(num)

        self.stdout.write("Successfully created {} users".format(user_count))
