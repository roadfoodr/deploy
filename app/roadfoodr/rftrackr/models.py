from django.db import models

# Create your models here.
class Users(models.Model):
	user_id = models.AutoField(primary_key=True)
	name_first = models.CharField(max_length=40)
	name_last = models.CharField(max_length=40)
	pub_date = models.DateTimeField('date published')

class Roadfoods(models.Model):
	rf_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=60)

class Visits(models.Model):
	user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
	rf_id = models.ForeignKey(Roadfoods, on_delete=models.CASCADE)
	visit_date = models.DateTimeField('date visited')

