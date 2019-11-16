from django.db import models
from django.utils.timezone import now


# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name_first = models.CharField(max_length=40)
    name_last = models.CharField(max_length=40)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        # python version 3.5 is being used
        return 'User {}: {} {}'.format(
            self.user_id, self.name_first, self.name_last)

class Roadfood(models.Model):
    rf_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    lat = models.FloatField(default=0.0)
    long = models.FloatField(default=0.0)

    def __str__(self):
        return 'Roadfood {}: {}'.format(self.rf_id, self.name)

class Visit(models.Model):
    visit_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rf_id = models.ForeignKey(Roadfood, on_delete=models.CASCADE)
    visit_date = models.DateTimeField('date visited', default=now)

    def __str__(self):
        return 'Visit {}: User {}, Roadfood {}'.format(
            self.visit_id, self.user_id, self.rf_id)

