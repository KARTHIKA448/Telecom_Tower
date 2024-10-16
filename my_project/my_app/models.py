from django.db import models

# Create your models here.
class Tower(models.Model):
    name = models.CharField(max_length = 100)
    location = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/',blank=True, null = True)

    def __str__(self):
        return self.name


class GeneratorData(models.Model):
    time = models.DateTimeField()
    end_of_hour = models.DateTimeField()
    uncertainty_period = models.DateTimeField()
    grid_r_ph_volt = models.FloatField()
    gset_r_ph_volt = models.FloatField()
    gen_status = models.CharField(max_length=50)
    generator_status = models.IntegerField()
    bat_volt = models.FloatField()
    fuel_ltr = models.FloatField()
    fuel_status = models.CharField(max_length=50)
    fuel_percent = models.IntegerField()
    sensor_open = models.IntegerField()
    sensor_status = models.CharField(max_length=50)
    cabin_door_lock = models.IntegerField()
    cabin_door_status = models.CharField(max_length=50)
    clean_duct_lock = models.IntegerField()
    clean_duct_status = models.CharField(max_length=50)
    fuel_cap_lock = models.IntegerField()
    fuel_cap_status = models.CharField(max_length=50)
    message = models.TextField()

    def __str___(self):
        return self.Time

