# -*- coding: utf-8 -*-
from core.api import functions
from core.api.decorators import autocomplete
from django.test import TestCase
from core.api.models import OriginalItem, ItemPrice, PartnerSource, Partner
from core.user.models import User
from django.test import Client
from django.core.management.base import CommandError
from django.core import mail
from django.core.management import call_command
from django.utils.six import StringIO
import random


# decorators.autocomplete
class TestAutocomplete(TestCase):
    def test_without_exception(self):
        data = TestAutocomplete.func_without_exception(None)
        self.assertEqual(data, dict(data=True, url=None))

    def test_with_exception(self):
        try:
            TestAutocomplete.func_with_exception(None)
        except AssertionError as e:
            pass
        except Exception as e:
            raise e

    @staticmethod
    @autocomplete
    def func_without_exception(url):
        return True

    @staticmethod
    @autocomplete
    def func_with_exception(url):
        raise AssertionError


# functions.clean_url
class TestCleanUrl(TestCase):
    def setUp(self):
        self.url = "http://example.com/path/;params?a=1&b=2&c=3#fragment"

    def test_clean_path(self):
        self.assertEqual(functions.clean_url(self.url, path=False),
                         "http://example.com/;params?a=1&b=2&c=3#fragment")

    def test_clean_fragment(self):
        self.assertEqual(functions.clean_url(self.url, fragment=False),
                         "http://example.com/path/;params?a=1&b=2&c=3")

    def test_clean_query(self):
        self.assertEqual(functions.clean_url(self.url, query=False),
                         "http://example.com/path/;params#fragment")

    def test_clean_params(self):
        self.assertEqual(functions.clean_url(self.url, params=False),
                         "http://example.com/path/?a=1&b=2&c=3#fragment")


# functions.clean_query
class TestCleanQuery(TestCase):
    def setUp(self):
        self.url = "http://example.com/path?a=1&b=2&c=3&d=4"

    def test_main(self):
        self.assertEqual(functions.clean_query(self.url, "a"),
                         "http://example.com/path?a=1")

        self.assertEqual(functions.clean_query(self.url, "a", "c"),
                         "http://example.com/path?a=1&c=3")

        self.assertEqual(functions.clean_query(self.url, "a", "b", "c"),
                         "http://example.com/path?a=1&b=2&c=3")

        self.assertEqual(functions.clean_query(self.url, "a", "b", "c", "d"),
                         self.url)

        # equal clean_url(url, query=False)
        self.assertEqual(functions.clean_query(self.url),
                         "http://example.com/path")
        self.assertEqual(functions.clean_query(self.url),
                         functions.clean_url(self.url, query=False))


class EmailTest(TestCase):
    def test_send_email(self):
        # Empty the test outbox
        mail.outbox = []
        # send message.
        mail.send_mail('Hello, world', 'Here is the message.',
                       'stratopedarx@mail.ru', ['sergey.lobanov2016@mail.ru'],
                       fail_silently=False)
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)
        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Hello, world')


class TestManagementCommands(TestCase):
    """
    For the management commands createtestuser.py, sendemail.py, create_new_item
    Check outputs
    """

    def setUp(self):
        self.out = StringIO()
        self.out_email1 = StringIO()
        self.out_email2 = StringIO()
        self.out_id1 = StringIO()
        self.out_id2 = StringIO()
        call_command('createtestuser', '10', stdout=self.out)  # create test users and checks the response
        self.item = OriginalItem.objects.all()
        self.client = Client()

    def test_createtestuser_output(self):
        self.assertIn('Successfully created 10 users', self.out.getvalue())
        self.assertEqual(len(User.objects.all()), 10)  # check count users
        self.assertEqual(len(OriginalItem.objects.all()),
                         len(ItemPrice.objects.all()))  # check count original items and item prices

    def test_create_new_item_output(self):
        call_command('create_new_item', '{}'.format(self.item[0].id), stdout=self.out)
        self.assertIn('Successfully created item with new id', self.out.getvalue())

    def test_sendemail_without_options(self):
        call_command('sendemail', stdout=self.out)
        call_command('sendemail', '--send_all', 'SEND_ALL', stdout=self.out)
        self.assertIn('Use --help', self.out.getvalue())

    def test_sendemail_dry_run_output(self):
        # check if the prices have not changed
        call_command('sendemail', '--dry_run', 'DRY_RUN', stdout=self.out)
        self.assertIn('The prices have not changed', self.out.getvalue())
        # check if the prices have changed
        call_command('create_new_item', '{}'.format(self.item[0].id), stdout=self.out)
        call_command('sendemail', '--dry_run', 'DRY_RUN', stdout=self.out)
        self.assertIn('The price', self.out.getvalue())

    def test_sendemail_email_without_send_all(self):
        # check if the prices have not changed
        call_command('sendemail', '--email', 'test_user0@mail.ru', stdout=self.out_email1)
        self.assertIn('The prices have not changed', self.out_email1.getvalue())
        # check if the prices have changed
        call_command('create_new_item', '{}'.format(self.item[0].id), stdout=self.out_email1)
        self.assertIn('Successfully created item with new id', self.out_email1.getvalue())
        call_command('sendemail', '--email', 'test_user0@mail.ru', stdout=self.out_email1)
        self.assertIn('The discount price has changed form', self.out_email1.getvalue())

    def test_sendemail_email_with_send_all(self):
        # check if the prices have not changed
        call_command('sendemail', '--send_all', 'SEND_ALL', '--email', 'test_user0@mail.ru', stdout=self.out_email2)
        self.assertIn('The prices have not changed', self.out_email2.getvalue())
        self.assertIn('The message is successfully sent to test_user0@mail.ru', self.out_email2.getvalue())
        # check if the prices have changed
        call_command('create_new_item', '{}'.format(self.item[0].id), stdout=self.out_email2)
        call_command('sendemail', '--send_all', 'SEND_ALL', '--email', 'test_user1@mail.ru', stdout=self.out_email2)
        self.assertIn('The message is successfully sent to test_user1@mail.ru', self.out_email2.getvalue())

    def test_sendemail_id_without_send_all(self):
        # check if the price have not changed
        call_command('sendemail', '--id', '{}'.format(self.item[0].id), stdout=self.out_id1)
        self.assertIn('The price has not changed', self.out_id1.getvalue())
        # check if the price have changed
        call_command('create_new_item', '{}'.format(self.item[0].id), stdout=self.out_id1)
        new_item = OriginalItem.objects.order_by('-itemprice__created_date')[:1].get()
        call_command('sendemail', '--id', '{}'.format(new_item.id), stdout=self.out_id1)
        self.assertIn('Users signed for the item:', self.out_id1.getvalue())

    def test_sendemail_id_with_send_all(self):
        # check if the price have not changed
        call_command('sendemail', '--send_all', 'SEND_ALL', '--id', '{}'.format(self.item[0].id), stdout=self.out_id2)
        self.assertIn('The price has not changed', self.out_id2.getvalue())
        # check if the price has changed
        call_command('create_new_item', '{}'.format(self.item[0].id), stdout=self.out_id2)
        new_item = OriginalItem.objects.order_by('-itemprice__created_date')[:1].get()
        call_command('sendemail', '--send_all', 'SEND_ALL', '--id', '{}'.format(new_item.id), stdout=self.out_id2)
        self.assertIn('The messages successfully sent to', self.out_id2.getvalue())

    def test_send_email_to_users(self):
        mail.outbox = []
        call_command('create_new_item', '{}'.format(self.item[0].id), stdout=self.out)
        new_item = OriginalItem.objects.order_by('-itemprice__created_date')[:1].get()
        call_command('sendemail', '--send_all', 'SEND_ALL', '--id', '{}'.format(new_item.id), stdout=self.out)
        user = User.objects.filter(itemgroup__useritem__item_id__id=new_item.id)
        self.assertEqual(len(mail.outbox), len(user))

    def test_client_login_logout(self):
        # login return true if the user is successfully logged in
        for i in xrange(len(User.objects.all())):
            res = self.client.login(username="test_user{}".format(i), password="password{}".format(i))
            self.assertEqual(res, True)
            self.assertEqual(self.client.logout(), None)


class TestItemsPrice(TestCase):
    """
    Tests item_price
    """

    def setUp(self):
        self.out = StringIO()
        self.item = OriginalItem.objects.all()

    def test_item_price(self):
        # create test users and checks the response
        call_command('createtestuser', '1', stdout=self.out)
        self.assertIn('Successfully created 1 users', self.out.getvalue())
        call_command('create_new_item', '{}'.format(self.item[0].id), stdout=self.out)
        # change price
        last_item = OriginalItem.objects.order_by('-itemprice__created_date')[:1].get()
        last_item_price = ItemPrice.objects.get(item_id=last_item.id)
        last_item_price.base_price = random.randrange(0, 25000)
        same_item_price = ItemPrice.objects.filter(item_id__title=last_item.title).exclude(
                id=last_item_price.id).order_by(
                '-created_date')[:1].get()
        same_item_price.base_price = random.randrange(25000, 50000)

        self.assertEqual(last_item_price.created_date != same_item_price.created_date, True)
        self.assertEqual(last_item_price.base_price < same_item_price.base_price, True)
        self.assertEqual(last_item_price.base_price > same_item_price.base_price, False)
        self.assertEqual(last_item_price.created_date > same_item_price.created_date, True)
        self.assertEqual(last_item_price.created_date < same_item_price.created_date, False)


class TestTryExcept(TestCase):
    """
    Сheck exceptions
    """

    def setUp(self):
        self.out = StringIO()

    def test_does_not_user(self):
        self.assertRaises(CommandError,
                          lambda: call_command('sendemail', '--send_all', 'SEND_ALL', '--email', 'anyuser@mail.ru'))

    def test_does_not_id(self):
        num = random.randrange(1000)
        self.assertRaises(CommandError,
                          lambda: call_command('sendemail', '--send_all', 'SEND_ALL', '--id', '{}'.format(num)))

    def test_does_not_user_with_this_item(self):
        # create any original item without users
        partner = Partner.objects.create(name="mvideo.ru", package="mvideo.ru")
        partner_source = PartnerSource.objects.create(partner=partner, domain="mvideo.ru",
                                                      scraper_name="mvideo.ru",
                                                      platform="mvideo.ru")
        original_item = OriginalItem.objects.create(article='12345',
                                                    title='Tv',
                                                    details='The big TV',
                                                    url="www.mvideo.ru", source=partner_source)

        self.assertRaises(TypeError,
                          lambda: call_command('sendemail', '--send_all', 'SEND_ALL', '--id',
                                               '{}'.format(original_item.id)))
