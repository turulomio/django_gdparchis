from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from gdparchis import models
from gdparchis.reusing.responses_json import json_success_response, json_data_response
from gdparchis.reusing.request_casting import RequestBool, RequestInteger,  RequestString,  all_args_are_not_empty

from rest_framework.views import APIView

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
            return json_success_response(False,  _("I can't register your game due to your installation hasn't been registered"))
        
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

def StatisticsGlobal(request):
        days30=timezone.now()-timedelta(days=30)
        installations={
                "Total installations": models.Installation.objects.count(), 
                "Number of installations in the last 30 days": models.Installation.objects.filter(datetime__gte=days30).count(), 
                "Installation that played in the last 30 days": models.Game.objects.filter(starts__gte=days30).values("installation_id").distinct().count(), 
                "Installations which are in the last version 20181125": 0, 
        }
        
        games={
            "Total games played": models.Game.objects.count(), 
            "Games played in the last 30 days": models.Game.objects.filter(starts__gte=days30).count(), 
            "Games per installation": 0, 
            "Games finished": models.Game.objects.filter(ends__isnull=False).count(), 
            "Finished games won by humans": models.Game.objects.filter(human_won=True).count(), 
        }
        
        modes=[]
        for mode in  [3, 4, 6, 8]:
            modes.append({
                "Maximum players":mode, 
                "Number of games": models.Game.objects.filter(max_players=mode).count(), 
                "Number of games finished": models.Game.objects.filter(ends__isnull=False, max_players=mode).count(), 
                "Median minutes to end a game": 0, 
                "Human victories": models.Game.objects.filter(human_won=True, max_players=mode).count(), 
            })

        top_players=[]
                
        
        r={}
        r["Installations"]=installations
        r["Games"]=games
        r["Modes"]=modes
        r["Top players"]=top_players
        return json_data_response(True,  r,  _("Global statistics"))
    
def StatisticsUser(request):
        uuid=RequestString(request, "uuid")
        r={}
        try:
            installation=models.Installation.object.get(uuid=uuid)
        except:
            return json_data_response(False, r,  _("Installation wasn't found"))

        r["Number"]=models.Game.objects.count(installation=installation)
        return json_data_response(True, r,   _("User statistics"))
