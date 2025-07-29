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

    def choose_point_to_goal(self, field: fld.Field, actions: list[Optional[Action]]) -> None:
        angleD = abs(aux.get_angle_between_points(field.enemies[const.ENEMY_GK].get_pos(), field.allies[self.idxN].get_pos(), field.enemy_goal.down))
        angleU = abs(aux.get_angle_between_points(field.enemies[const.ENEMY_GK].get_pos(), field.allies[self.idxN].get_pos(), field.enemy_goal.up))
        k = 100
        if angleD > angleU:
            go = field.enemy_goal.down + (field.enemy_goal.eye_up * k)
        else:
            go = field.enemy_goal.up - (field.enemy_goal.eye_up * k)
        actions[self.idxN] = Actions.Kick(go)
        print(actions[self.idxN])

    def block_passes(self, field: fld.Field, actions: list[Optional[Action]]) -> None:
        l = aux.angle_to_point(field.enemies[0].get_pos(), field.ball.get_pos())
        p = aux.angle_to_point(field.enemies[0].get_pos(), field.allies[0].get_pos())
        y = aux.angle_to_point(field.enemies[0].get_pos(), field.allies[5].get_pos())
        print(l, p, y)
        r = (aux.point_on_line(field.allies[0].get_pos(), field.enemies[0].get_pos(), 300))
        u = (aux.point_on_line(field.allies[5].get_pos(), field.enemies[0].get_pos(), 300))
        if((y - l) > (l - p)):
            actions[3] = Actions.GoToPointIgnore(r , (field.ball.get_pos() - field.allies[3].get_pos()).arg())
        else:
            actions[3] = Actions.GoToPointIgnore(u , (field.ball.get_pos() - field.allies[3].get_pos()).arg())

    def block_pass(self, field: fld.Field, actions: list[Optional[Action]]) -> None:
        actions[3] = Actions.GoToPointIgnore((aux.point_on_line(field.allies[0].get_pos(), field.enemies[0].get_pos(), 300)) , (field.ball.get_pos() - field.allies[3].get_pos()).arg())

    def opening_to_the_ball(self, field: fld.Field, actions: list[Optional[Action]]) -> None:
        y = (field.ball.get_pos() - field.allies[2].get_pos()).unity()*50000
        b = -1
        for b in range(6):
            b+=1
            if(aux.dist(aux.closest_point_on_line(field.ball.get_pos(), field.allies[2].get_pos(), field.enemies[b].get_pos(), "S"), field.enemies[b].get_pos()) < 100):
                e = aux.get_angle_between_points(field.allies[2].get_pos(), field.ball.get_pos(), field.enemies[b].get_pos())
                if(e<0):
                    while(aux.dist(aux.closest_point_on_line(field.ball.get_pos(), field.allies[2].get_pos(), field.enemies[b].get_pos(), "S"), field.enemies[b].get_pos()) < 100):
                        actions[2] = Actions.GoToPointIgnore(aux.rotate(y, 3.14/2), (field.ball.get_pos() - field.allies[2].get_pos()).arg())
                else:
                    while(aux.dist(aux.closest_point_on_line(field.ball.get_pos(), field.allies[2].get_pos(), field.enemies[b].get_pos(), "S"), field.enemies[b].get_pos()) < 100):
                        actions[2] = Actions.GoToPointIgnore(aux.rotate(y, -3.14/2), (field.ball.get_pos() - field.allies[2].get_pos()).arg())
    
    def run_Neymar(self, field: fld.Field, actions: list[Optional[Action]]) -> None:
        #self.pass_Ronaldo(field, actions)
        self.pass_Ronaldo(field, actions)
        

