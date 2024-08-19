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

    def is_cp(self, player_id):
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
        
    def state(self):
        return self._s
        
    def piece_squares_to_move(self, player_id, piece_id,  throw):
        if self.cp_has_extra_moves():
            return self.cp_extra_moves()[0]
        
