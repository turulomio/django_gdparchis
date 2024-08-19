from django.db import models
from json import loads
from gdparchis import dictstate

class InstallationStatistic(models.Model):
    datetime = models.DateTimeField(blank=False, null=False)
    uuid= models.UUIDField(blank=False, null=False)
    ip=models.CharField(max_length=50, blank=False, null=False)
    so=models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'installations_statistics'
        
        
class GameStatistic(models.Model):
    starts = models.DateTimeField(blank=False, null=False)
    ends = models.DateTimeField(blank=True, null=True)
    uuid= models.UUIDField(blank=True, null=False)
    installation = models.ForeignKey("InstallationStatistic", on_delete=models.CASCADE, blank=False, null=False)
    max_players=models.IntegerField(blank=False, null=False)
    num_players=models.IntegerField(blank=False, null=False)
    human_won=models.BooleanField(null=True)
    version=models.CharField(max_length=50, blank=False, null=False)
    faked=models.BooleanField(default=False, null=False)

    class Meta:
        managed = True
        db_table = 'games_statistics'
        
        
class Game(models.Model):    
    uuid= models.UUIDField(blank=True, null=False)
    datetime=models.DateTimeField(blank=True, null=False)
    max_players=models.IntegerField(blank=False, null=False)
    class Meta:
        managed = True
        db_table = 'games'
        
    def last_state(self, request):
        try:
            return dictstate.dState(loads(State.objects.filter(game=self).order_by("-datetime")[0].state, request))
        except:
            return None

class State(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE, blank=False, null=False)
    datetime=models.DateTimeField(blank=False, null=False)
    state=models.TextField(blank=False, null=False)    
    
    class Meta:
        managed = True
        db_table = 'states'
