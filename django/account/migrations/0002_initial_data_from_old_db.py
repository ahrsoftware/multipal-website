from django.conf import settings
from django.db import migrations
from palaeography import models
from ast import literal_eval
from django.contrib.auth.hashers import make_password
import os


def insert_users(apps, schema_editor):
    """
    Inserts User objects from old database
    """

    with open(os.path.join(settings.BASE_DIR, 'account', 'migrations', 'old_data', "data_users.txt"), 'r') as file:
        for object in literal_eval(file.read()):

            # Clean the name (in old db full name is stored in a single field and includes strange numbers, etc.)
            # Remove numbers
            name = ''.join([char for char in object['name'] if not char.isdigit()])
            # Replace underscores and periods with whitespace
            name = name.replace('_', ' ').replace('.', ' ')
            # Split into first name and last name (if a last name exists)
            name = name.split(' ')
            object['first_name'] = name[0].capitalize()
            if len(name) > 1:
                object['last_name'] = name[1].capitalize()
            # Delete old name data
            del object['name']

            # Set encrypted password
            object['password'] = make_password(settings.TEMP_PASSWORD_FOR_USERS_FROM_OLD_DB)

            # Save object to db
            models.User.objects.create(**object)


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial')
    ]

    operations = [
        migrations.RunPython(insert_users)
    ]
