# Generated by Django 5.0.4 on 2024-05-08 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_produto_cb7_dtemis_alter_produto_cb7_dtfims_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='LINE',
            field=models.IntegerField(default=0),
        ),
    ]