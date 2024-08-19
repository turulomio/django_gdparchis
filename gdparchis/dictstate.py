class dState:
    def __init__(self, state, request):
        self._s=state
        self.request=request
        
    def square(self, square_id):
        return self.request.squares4[square_id]
        
    def route(self, player_id):
        return self.request.route4[player_id]
        
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
        
