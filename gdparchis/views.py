from datetime import timedelta
from django.db.models import Max, Count, F
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from gdparchis import models
from gdparchis.reusing.responses_json import json_success_response, json_data_response
from gdparchis.reusing.request_casting import RequestBool, RequestInteger,  RequestString, RequestGetString,  all_args_are_not_empty

from rest_framework.views import APIView
from statistics import median

class InstallationAPIView(APIView):
    permission_classes=[]
    
    def post(self, request):
        """
            Sets a new installation or updates it
        """
        uuid=RequestString(request, "uuid")
        so=RequestString(request, "so")
        if all_args_are_not_empty(uuid, so):
            if models.Installation.objects.filter(uuid=uuid).exists():
                return json_success_response(False,  _("Installation already exists"))
            else:
                installation=models.Installation()
                installation.datetime=timezone.now()
                installation.uuid=uuid
                installation.so=so
                installation.ip=request.META.get("REMOTE_ADDR", "")
                installation.save()
                return json_success_response(True,  _("Your installation was registered"))
        return json_success_response(False,  _("There was a problem registering your installation"))

class GameAPIView(APIView):
    permission_classes=[]
    
    ## Start of game
    def post(self, request):
        max_players=RequestInteger(request, "max_players")
        num_players=RequestInteger(request, "num_players")
        installation_uuid=RequestString(request, "installation_uuid")
        game_uuid=RequestString(request, "game_uuid")
        version=RequestString(request, "version")

        if models.Game.objects.filter(uuid=game_uuid).exists():
            return json_success_response(False,  _("Game already exists"))
        
        try:
            installation=models.Installation.objects.get(uuid=installation_uuid)
        except:
            return json_success_response(False,  _("I can't register your game due to your installation haseconds between datetimessn't been registered"))
        
        print(max_players, num_players, installation, version, game_uuid)
        if all_args_are_not_empty(max_players, num_players, installation, version, game_uuid):
            game=models.Game()
            game.starts=timezone.now()
            game.max_players=max_players
            game.num_players=num_players
            game.installation=installation
            game.uuid=game_uuid
            game.version=version
            game.save()
            return json_success_response(True,  _("Your game was registered"))
        return json_success_response(False,  _("There was a problem registering your game"))
        
    ## End of game
    def put(self, request):
        
        human_won=RequestBool(request, "human_won")
        game_uuid=RequestString(request, "game_uuid")
        faked=RequestBool(request, "faked")
              
        print(human_won, game_uuid, faked)
        try:
            game=models.Game.objects.get(uuid=game_uuid)
        except:
            return json_success_response(False,  _("I can't update your game due to it doesn't exist"))
            
        if game.ends is not None:
            return json_success_response(False,  _("This game was already closed"))
            
        if game.faked is True:
            return json_success_response(False,  _("This game was already faked. You can't edit it anymore"))
            
            
        if faked is True:
            game.faked=faked
            game.save()
            return json_success_response(True,  _("Your game has been marked as faked"))

        if human_won is not None:                    
            game.ends=timezone.now()
            game.human_won=human_won
            game.save()
            return json_success_response(True,  _("Your game was closed"))

        return json_success_response(False,  _("Something wrong with my radio"))
        
def Average(lst):
    return sum(lst) / len(lst)

def StatisticsGlobal(request):
        lastversion=models.Game.objects.aggregate(Max('version')).get('version__max',  '0.0.0')
        average_games_by_installations=Average(models.Installation.objects.annotate(Count("game")).values_list("game__count", flat=True))
    
        days30=timezone.now()-timedelta(days=30)
        installations={
                "Total installations": models.Installation.objects.count(), 
                "Number of installations in the last 30 days": models.Installation.objects.filter(datetime__gte=days30).count(), 
                "Installation that played in the last 30 days": models.Game.objects.filter(starts__gte=days30).values("installation_id").distinct().count(), 
                "Last version": lastversion, 
                "Installations which are in the last version": models.Game.objects.filter(version=lastversion).values("installation_id").distinct().count(), 
        }
        
        games={
            "Total games played": models.Game.objects.count(), 
            "Games played in the last 30 days": models.Game.objects.filter(starts__gte=days30).count(), 
            "Games per installation (average)": average_games_by_installations, 
            "Games finished": models.Game.objects.filter(ends__isnull=False).count(), 
            "Finished games won by humans": models.Game.objects.filter(human_won=True).count(), 
        }
        
        modes=[]
        for mode in  [3, 4, 6, 8]:
            
            timedeltas=list(models.Game.objects.filter(ends__isnull=False, max_players=mode).annotate(diff=F('ends')-F('starts')).values_list("diff", flat=True))
            mode_median=round(median(timedeltas).total_seconds()/60, 2) if len(timedeltas)>0 else None
            
            
            
            modes.append({
                "Maximum players":mode, 
                "Number of games": models.Game.objects.filter(max_players=mode).count(), 
                "Number of games finished": models.Game.objects.filter(ends__isnull=False, max_players=mode).count(), 
                "Median minutes to end a game": mode_median, 
                "Human victories": models.Game.objects.filter(human_won=True, max_players=mode).count(), 
            })

        qs_top_players=models.Installation.objects.annotate(Count("game")).order_by("-game__count")
        top_players=[]
        for p in qs_top_players[:10]:
            top_players.append({
                "Id":p.uuid, 
                "Number of games": p.game__count, 
                "First installation": p.datetime, 
                "Last game":p.game_set.all().aggregate(Max("starts")).get("starts__max", None), 
            })
                
        
        r={}
        r["Installations"]=installations
        r["Games"]=games
        r["Modes"]=modes
        r["Top players"]=top_players
        return json_data_response(True,  r,  _("Global statistics"))
    
def StatisticsUser(request):
        uuid_=RequestGetString(request, "uuid")
        installation=models.Installation.objects.get(uuid=uuid_)
        r={}
        try:
            installation=models.Installation.objects.get(uuid=uuid_)
        except:
            return json_data_response(False, r,  _("Installation {0} wasn't found").format(uuid_))
    
        days30=timezone.now()-timedelta(days=30)
        
        qs_top_players=models.Installation.objects.annotate(Count("game")).order_by("-game__count")
        for global_position, p in enumerate(qs_top_players):
            if p.uuid==installation.uuid:
                break
            
        games={
            "Total games played in this installation": models.Game.objects.filter(installation=installation).count(), 
            "Games played in the last 30 days in this installation": models.Game.objects.filter(installation=installation, starts__gte=days30).count(), 
            "Games finished in this installation": models.Game.objects.filter(installation=installation, ends__isnull=False).count(), 
            "Finished games won by humans in this installation": models.Game.objects.filter(installation=installation, human_won=True).count(), 
            "Global classification of users who have played the most": global_position,
        }
        
        modes=[]
        for mode in  [3, 4, 6, 8]:
            
            timedeltas=list(models.Game.objects.filter(installation=installation, ends__isnull=False, max_players=mode).annotate(diff=F('ends')-F('starts')).values_list("diff", flat=True))
            mode_median=round(median(timedeltas).total_seconds()/60, 2) if len(timedeltas)>0 else None
            
            modes.append({
                "Maximum players":mode, 
                "Number of games in this installation": models.Game.objects.filter(installation=installation, max_players=mode).count(), 
                "Number of games finished in this installation": models.Game.objects.filter(installation=installation, ends__isnull=False, max_players=mode).count(), 
                "Median minutes to end a game in this installation": mode_median, 
                "Human victories in this installation": models.Game.objects.filter(installation=installation, human_won=True, max_players=mode).count(), 
            })

                
        
        r={}
        r["Games"]=games
        r["Modes"]=modes
        return json_data_response(True,  r,  _("Installation {0} statistics").format(installation.uuid))
