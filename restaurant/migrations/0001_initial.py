# Generated by Django 4.1 on 2022-09-02 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuisines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ext_id', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ext_id', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=200)),
                ('zomato_id', models.IntegerField()),
                ('address', models.TextField()),
                ('latitude', models.FloatField(blank=True, default=None, null=True)),
                ('longitude', models.FloatField(blank=True, default=None, null=True)),
                ('image_url', models.URLField(blank=True, max_length=250, null=True)),
                ('do_online_delivery', models.BooleanField(default=False)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utils.city')),
                ('cuisines', models.ManyToManyField(related_name='cuisines', to='restaurant.cuisines')),
            ],
        ),
    ]
