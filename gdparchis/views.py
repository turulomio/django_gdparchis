from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from gdparchis import models
from gdparchis.reusing.responses_json import json_success_response
from gdparchis.reusing.request_casting import RequestBool, RequestInteger,  RequestString,  all_args_are_not_empty

from rest_framework.views import APIView

class Installation(APIView):
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

class Game(APIView):
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
        
        human_won=RequestInteger(request, "human_won")
        game_uuid=RequestString(request, "game_uuid")
        faked=RequestBool(request, "faked", False)
                
        try:
            game=models.Game.objects.get(uuid=game_uuid)
        except:
            return json_success_response(False,  _("I can't update your game due to it doesn't exist"))

        
        if all_args_are_not_empty(human_won, game_uuid, faked):
            if game.faked or game.ends is not None:
                return json_success_response(False,  _("You are cheating"))
                
            
            game.faked=faked
            game.ends=timezone.now()
            game.human_won=human_won
            game.save()
            if faked:
                return json_success_response(False,  _("You are cheating"))
            else:
                return json_success_response(True,  _("Your game was updated"))
                
