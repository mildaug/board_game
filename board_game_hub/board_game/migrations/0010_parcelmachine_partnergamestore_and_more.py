# Generated by Django 4.2.2 on 2023-07-03 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board_game', '0009_gameborrowrequest_pick_up_place'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParcelMachine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('city', models.CharField(max_length=100, verbose_name='city')),
            ],
            options={
                'verbose_name': 'parcel machine',
                'verbose_name_plural': 'parcel machines',
                'ordering': ['city'],
            },
        ),
        migrations.CreateModel(
            name='PartnerGameStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('city', models.CharField(max_length=100, verbose_name='city')),
            ],
            options={
                'verbose_name': 'partner game store',
                'verbose_name_plural': 'partner game stores',
                'ordering': ['city'],
            },
        ),
        migrations.AddField(
            model_name='gameborrowrequest',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='gameborrowrequest',
            name='pick_up_place',
            field=models.CharField(blank=True, choices=[('partner_game_store', 'Partner game store'), ('send_via_post', 'Send via post'), ('parcel_machine', 'Parcel machine')], max_length=20, null=True, verbose_name='pick-up place'),
        ),
        migrations.AddField(
            model_name='gameborrowrequest',
            name='parcel_machine',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='board_game.parcelmachine'),
        ),
        migrations.AddField(
            model_name='gameborrowrequest',
            name='partner_game_store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='board_game.partnergamestore'),
        ),
    ]