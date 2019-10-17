from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name_first = models.CharField(max_length=40)
    name_last = models.CharField(max_length=40)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return f'User {self.user_id}: {self.name_first} {self.name_last}'

class Roadfood(models.Model):
    rf_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)

    def __str__(self):
        return f'Roadfood {self.rf_id}: {self.name}'

class Visit(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rf_id = models.ForeignKey(Roadfood, on_delete=models.CASCADE)
    visit_date = models.DateTimeField('date visited')

