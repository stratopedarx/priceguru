# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL("""
        BEGIN;
CREATE OR REPLACE FUNCTION get_currency_ratio(text, text) RETURNS FLOAT AS $$
DECLARE result FLOAT;
BEGIN
        SELECT ratio INTO result FROM currency_currencyratio WHERE from_currency=$1 AND to_currency=$2;
        RETURN result;
END;
$$ LANGUAGE plpgsql;
COMMIT;""",
                          """
BEGIN;
DROP FUNCTION get_currency_ratio(text, text);
COMMIT;
                          """"")
    ]
