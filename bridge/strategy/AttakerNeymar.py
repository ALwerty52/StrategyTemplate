# !v DEBUG ONLY
import math  # type: ignore
from time import time  # type: ignore
from typing import Optional
from bridge import const
from bridge.auxiliary import aux, fld, rbt  # type: ignore
from bridge.const import State as GameStates
from bridge.router.base_actions import Action, Actions, KickActions, get_pass_voltage  # type: ignore

class Attaker_Neymar:
    def __init__(self, ) -> None:
        self.idxgk: int = 1
        self.idxR: int = 0
        self.idxN: int = 2
        self.passto = 0

    def pass_Ronaldo(self, field: fld.Field, actions: list[Optional[Action]]) -> None:
        actions[self.idxN] = KickActions.KickNeymar(field.allies[self.idxR].get_pos(), get_pass_voltage(aux.dist(field.allies[self.idxN].get_pos(), field.allies[self.idxR].get_pos())), True)

    def Grab_Ronaldo(self, field: fld.Field, actions: list[Optional[Action]]) -> None:
        angelR = (field.allies[self.idxR].get_pos() - field.allies[self.idxN].get_pos()).arg()
        actions[self.idxN] = Actions.GoToPoint(aux.closest_point_on_line(field.allies[self.idxR].get_pos(), field.ball.get_pos(), field.allies[self.idxN].get_pos(), "R"), angelR)
    
    def run_Neymar(self, field: fld.Field, actions: list[Optional[Action]]) -> None:
        #self.pass_Ronaldo(field, actions)
        self.pass_Ronaldo(field, actions)
        

