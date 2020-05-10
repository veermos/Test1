from django.db import models
# from account.models import Account

class Fees(models.Model):
    BankA_CHOICES = (
        ('11111111111111', '11111111111111'),
        ('22222222222222', '22222222222222'),
        ('33333333333333', '33333333333333'),
        ('44444444444444', '44444444444444'),
        ('55555555555555', '55555555555555'),
        ('نقدي بالمدرسة', 'نقدي بالمدرسة'),
    )

    KIND_CHOICES = (
        ('دراسية', 'دراسية'),
        ('باص', 'باص'),
    )

    SCHOOL_CHOICES = (
        (None, ""),
        ('بنين', 'بنين'),
        ('بنات', 'بنات'),
    )

    payment_date = models.DateField(null=True, blank=True)
    bank_account = models.CharField(max_length=16, choices=BankA_CHOICES)
    value = models.PositiveSmallIntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    kind = models.CharField(max_length=6, choices=KIND_CHOICES)
    school = models.CharField( max_length=4, choices=SCHOOL_CHOICES, blank=True)
    student = models.ForeignKey(to='account.Student', on_delete=models.CASCADE)


    def __str__(self):
        return self.student.username
