from django.db import models

class Installation(models.Model):
    datetime = models.DateTimeField(blank=False, null=False)
    uuid= models.UUIDField(blank=False, null=False)
    ip=models.CharField(max_length=50, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'installations'
        
        
class Games(models.Model):
    starts = models.DateTimeField(blank=False, null=False)
    ends = models.DateTimeField()
    uuid= models.UUIDField(blank=False, null=False)
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE, blank=False, null=False)
    max_players=models.IntegerField(blank=False, null=False)
    num_players=models.IntegerField(blank=False, null=False)
    human_won=models.BooleanField()
    version=models.CharField(max_length=50, blank=False, null=False)
    class Meta:
        managed = True
        db_table = 'games'
