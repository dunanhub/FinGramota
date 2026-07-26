from django.db import migrations


BANKS = [
    ('Alatau City Bank', 'https://alataucitybank.kz/'),
    ('Altyn Bank', 'https://altynbank.kz/'),
    ('Bank CenterCredit', 'https://www.bcc.kz/'),
    ('Bank RBK', 'https://www.bankrbk.kz/'),
    ('Bereke Bank', 'https://berekebank.kz/'),
    ('BNK Commercial Bank', 'https://bnkcommercialbank.kz/'),
    ('Eurasian Bank', 'https://eubank.kz/ru'),
    ('ForteBank', 'https://forte.kz/'),
    ('Freedom Bank Kazakhstan', 'https://www.freedombank.kz/'),
    ('Halyk Bank', 'https://www.halykbank.kz/'),
    ('Home Credit Bank', 'https://home.kz/'),
    ('Kaspi Bank', 'https://kaspi.kz/'),
    ('Kazakhstan-Ziraat International Bank', 'https://www.kzibank.kz'),
    ('KMF Bank', 'https://kmf.kz/'),
    ('Nurbank', 'https://www.nurbank.kz/'),
    ('Otbasy Bank', 'https://www.hcsbk.kz/'),
    ('VTB Bank Kazakhstan', 'https://www.vtb-bank.kz/'),
    ('Zaman-Bank', 'https://www.zamanbank.kz/'),
]


def seed_banks(apps, _schema_editor):
    Bank = apps.get_model('marketplace', 'Bank')
    for name, official_url in BANKS:
        Bank.objects.update_or_create(
            name=name,
            defaults={'official_url': official_url},
        )


def remove_seeded_banks(apps, _schema_editor):
    Bank = apps.get_model('marketplace', 'Bank')
    Bank.objects.filter(name__in=[name for name, _url in BANKS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_banks, remove_seeded_banks),
    ]
