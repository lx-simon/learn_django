# Generated by Django 4.2 on 2024-01-23 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='admin',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app01.admin', verbose_name='管理员'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='oid',
            field=models.CharField(default=None, max_length=64, verbose_name='订单号'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.IntegerField(default=None, verbose_name='价格'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.SmallIntegerField(choices=[(2, '已支付'), (1, '待支付')], default=1, verbose_name='状态'),
        ),
        migrations.AddField(
            model_name='order',
            name='title',
            field=models.CharField(default=None, max_length=32, verbose_name='名称'),
            preserve_default=False,
        ),
    ]
