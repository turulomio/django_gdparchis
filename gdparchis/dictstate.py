from django.utils import timezone
from gdparchis import models
from json import dumps

class dState:
    def __init__(self, state, request):
        self._s=state
        self.request=request
        
    def square(self, square_id):
        return self.request.squares4[square_id]
        
    def route(self, player_id):
        return self.request.routes4[player_id]
        
    def cp_route(self):
        return self.route(self._s["current"])
        
    def player(self, player_id):
         return self._s["players"][player_id]
        
    def cp(self):
        return self._s["players"][self._s["current"]]

    def cp_is(self, player_id):
        return self._s["current"]==player_id
        
    def cp_is_dice_waiting(self):
        return self.cp()["dice_waiting"]
        
    def cp_set_dice_waiting(self, value):
        self.cp()["dice_waiting"]=value
        
    def cp_add_a_throw(self, value):
        self.cp()["throws"].append(value)
        
    def cp_extra_moves(self):
        return self.cp()["extra_moves"]
        
    def cp_has_extra_moves(self, value):
        return len(self.cp_extra_moves())>0
        
    def player_has_all_pieces_out_of_home(self,  player_id):
        for piece in self.pieces(player_id):
            if piece["route_position"]==0:
                return False
        return True
        
    def player_has_some_piece_waiting(self,  player_id):
        for piece in self.pieces(player_id):
            if piece["waiting"]>0:
                return True
        return False
        
    def state(self):
        return self._s
        
    def pieces(self, player_id):
        return self._s["players"][player_id]["pieces"]
  
    def cp_pieces(self):
        return self._s["players"][self._s["current"]]["pieces"]
        
    def piece(self,  player_id,  piece_id):
        return self.player(player_id)["pieces"][piece_id]
        
    def piece_square(self, player_id,  piece_id):
        """
            Returns a square_id
        """
        piece=self.piece(player_id,  piece_id)
        return self.square(self.route(player_id)["route"][piece["route_position"]])
        
    def piece_is_waiting(self,  player_id,  piece_id):
        return self.piece(player_id, piece_id)["waiting"]>0
    
    def piece_squares_to_move_after_throw(self, player_id, piece_id,  throw):
        piece=self.piece(player_id,  piece_id)
        if piece["route_position"]==0:
            if throw==5: #Salir de casa
                return 1
            else:
                return 0
        else: # Fuera de casa
            if throw==6 and self.player_has_all_pieces_out_of_home(player_id):
                return 7
            else:
                #Falta logica barreras
                return throw

    def change_waitings_after_dice_throw(self,  player_id, throw):
        self.cp_set_dice_waiting(False)
        self.cp_add_a_throw(throw)
        for piece in self.cp_pieces():
            piece["waiting"]=self.piece_squares_to_move_after_throw(player_id, piece["id"], throw )
            
    def save(self):
        state=models.State()
        state.game_id=self._s["game_id"]
        state.datetime=timezone.now()
        state.state=dumps(self._s)
        state.save()
        
    def square_get_free_position(self, square_id):
        """
            REturns None if there isn't free position
        """
        square=self.square(square_id)
        square
        
        return 0
            
    def process_piece_click(self, player_id,  piece_id):
        """
            En este punto no hay que hacer validaciones, solo se mueve
        """
        piece=self.piece(player_id,  piece_id)
        piece["route_position"]=piece["route_position"]+piece["waiting"]
        piece_square=self.piece_square(player_id,  piece_id)
        piece["square_position"]=self.square_get_free_position(piece_square["id"])
        # Sets waiting 0
        for piece in self.pieces(player_id):
            piece["waiting"]=0
        
        
