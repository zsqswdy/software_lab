# Generated by Django 5.0.6 on 2024-06-05 14:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=10, verbose_name="科室名字")),
                ("parentid", models.IntegerField(verbose_name="上级科室id")),
                ("address", models.CharField(max_length=30, verbose_name="科室地址")),
            ],
            options={
                "verbose_name": "科室",
                "verbose_name_plural": "科室列表",
            },
        ),
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("phone", models.CharField(max_length=11, verbose_name="患者电话")),
                ("password", models.CharField(max_length=30, verbose_name="患者密码")),
                ("name", models.CharField(max_length=10, verbose_name="患者姓名")),
                ("sex", models.CharField(max_length=1, verbose_name="患者性别")),
                ("age", models.CharField(max_length=3, verbose_name="患者年龄")),
            ],
            options={
                "verbose_name": "患者",
                "verbose_name_plural": "患者列表",
            },
        ),
        migrations.CreateModel(
            name="Doctor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("phone", models.CharField(max_length=11, verbose_name="医生电话")),
                ("password", models.CharField(max_length=30, verbose_name="医生密码")),
                ("name", models.CharField(max_length=10, verbose_name="医生姓名")),
                ("sex", models.CharField(max_length=1, verbose_name="医生性别")),
                ("age", models.CharField(max_length=3, verbose_name="医生年龄")),
                (
                    "img",
                    models.ImageField(upload_to="doctorimages/", verbose_name="医生照片"),
                ),
                ("level", models.CharField(max_length=10, verbose_name="职位等级")),
                ("description", models.CharField(max_length=50, verbose_name="详细描述")),
                ("registration_price", models.IntegerField(verbose_name="挂号价格")),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hospital_registration_system.department",
                    ),
                ),
            ],
            options={
                "verbose_name": "医生",
                "verbose_name_plural": "医生列表",
            },
        ),
        migrations.CreateModel(
            name="Register",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("patient_name", models.CharField(max_length=10, verbose_name="患者姓名")),
                ("doctor_name", models.CharField(max_length=10, verbose_name="医生姓名")),
                ("registration_time", models.DateTimeField(verbose_name="挂号时间")),
                ("consultation_hours", models.DateTimeField(verbose_name="会诊时间")),
                ("illness", models.CharField(max_length=50, verbose_name="病情概要")),
                ("address", models.CharField(max_length=30, verbose_name="会诊地址")),
                (
                    "isdelete",
                    models.BooleanField(default=False, verbose_name="挂号是否已经删除"),
                ),
                ("out_trade_num", models.UUIDField(verbose_name="商户订单号")),
                (
                    "status",
                    models.CharField(default="待支付", max_length=10, verbose_name="状态"),
                ),
                (
                    "payway",
                    models.CharField(
                        default="alipay", max_length=10, verbose_name="支付方式"
                    ),
                ),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="hospital_registration_system.doctor"
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="hospital_registration_system.patient"
                    ),
                ),
            ],
            options={
                "verbose_name": "挂号单",
                "verbose_name_plural": "挂号单列表",
            },
        ),
        migrations.CreateModel(
            name="TimeNumber",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("eight", models.PositiveSmallIntegerField(verbose_name="八点可预约人数")),
                ("nine", models.PositiveSmallIntegerField(verbose_name="九点可预约人数")),
                ("ten", models.PositiveSmallIntegerField(verbose_name="十点可预约人数")),
                ("eleven", models.PositiveSmallIntegerField(verbose_name="十一点可预约人数")),
                ("fourteen", models.PositiveSmallIntegerField(verbose_name="十四点可预约人数")),
                ("fifteen", models.PositiveSmallIntegerField(verbose_name="十五点可预约人数")),
                ("sixteen", models.PositiveSmallIntegerField(verbose_name="十六点可预约人数")),
                (
                    "seventeen",
                    models.PositiveSmallIntegerField(verbose_name="十七点可预约人数"),
                ),
                (
                    "default_number",
                    models.PositiveSmallIntegerField(verbose_name="默认一个时间点可预约人数"),
                ),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="hospital_registration_system.doctor"
                    ),
                ),
            ],
            options={
                "verbose_name": "某时间点可预约人数",
                "verbose_name_plural": "某时间点可预约人数列表",
            },
        ),
    ]