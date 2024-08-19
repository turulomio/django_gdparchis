from django.db import transaction
from django.utils import timezone
from gdparchis import models
from json import dumps
from rest_framework import serializers
from uuid import uuid4
#from django.utils.translation import gettext as _


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Game
        fields = ('url', 'id', 'max_players', 'datetime', 'uuid')

    @transaction.atomic
    def create(self, validated_data):
        print(validated_data)
        validated_data["datetime"]=timezone.now()
        validated_data["uuid"]=str(uuid4())
        created=serializers.HyperlinkedModelSerializer.create(self,  validated_data)
        created.save()
        
        #Creates a new state
        
        dict={}	
        dict["game_id"]=created.id
        dict["max_players"]=created.max_players
        dict["current"]=0
        dict["fake_dice"]=[]
        dict["game_uuid"]=created.uuid
        dict["players"]=[]
        for player_id in range(4):
            dict_p={}
            dict_p["id"]=player_id
            dict_p["playername"]=""
            dict_p["plays"]=True
            dict_p["ia"]=False if player_id==0 else True
            dict_p["dice_waiting"]=True if player_id==0 else False
            dict_p["throws"]=[]
            dict_p["extra_moves"]=[]
            dict_p["pieces"]=[]
            for piece_id in range(4):
                dict_piece={}
                dict_piece["id"]=piece_id
                dict_piece["route_position"]=0
                dict_piece["square_position"]=0
                dict_piece["waiting"]=False
                dict_p["pieces"].append(dict_piece)
            dict["players"].append(dict_p)
        
        state=models.State()
        state.datetime=created.datetime
        state.state=dumps(dict)
        state.game=created
        state.save()
        return created
    

class StateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.State
        fields = ('url', 'id', 'datetime', 'state', 'game')
