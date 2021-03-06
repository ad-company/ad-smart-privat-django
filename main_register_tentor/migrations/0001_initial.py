# Generated by Django 2.1.7 on 2020-08-05 06:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main_register_tentor.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=250)),
                ('year', models.IntegerField()),
                ('paid', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paid_tentor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Paid',
            },
        ),
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('SD 1-5', 'SD 1-5'), ('SD 1-5+', 'SD 1-5+'), ('SD 6', 'SD 6'), ('SD 6+', 'SD 6+'), ('SMP 7-8', 'SMP 7-8'), ('SMP 7-8+', 'SMP 7-8+'), ('SMP 9', 'SMP 9'), ('SMP 9+', 'SMP 9+'), ('SMA 10-11', 'SMA 10-11'), ('SMA 10-11+', 'SMA 10-11+'), ('SMA 12', 'SMA 12'), ('SMA 12+', 'SMA 12+')], max_length=250)),
                ('mode', models.CharField(choices=[('online (remote)', 'Online'), ('offline', 'Offline')], max_length=250)),
                ('price', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Fee',
            },
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('bank_name', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('bank_id', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Bank',
            },
        ),
        migrations.CreateModel(
            name='Tentors',
            fields=[
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=250)),
                ('gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=2)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=250)),
                ('account_name', models.CharField(max_length=250)),
                ('account_id', models.CharField(max_length=20)),
                ('bank_other', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('university', models.CharField(max_length=150)),
                ('major', models.CharField(max_length=100)),
                ('number_id', models.CharField(default='00', max_length=100)),
                ('id_pic', models.ImageField(blank=True, default='uploads/user-no-image.png', null=True, upload_to=main_register_tentor.models.photo_id, verbose_name='img')),
                ('profile_pic', models.ImageField(blank=True, default='uploads/user-no-image.png', null=True, upload_to=main_register_tentor.models.photo_profile, verbose_name='img')),
                ('user_type', models.CharField(default='tentor', editable=False, max_length=100)),
                ('status', models.BooleanField(default=False, editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_register_tentor.Bank')),
            ],
            options={
                'verbose_name_plural': 'Tentor',
            },
        ),
    ]
