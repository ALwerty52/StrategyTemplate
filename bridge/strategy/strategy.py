"""High-level strategy code"""

# !v DEBUG ONLY
import math  # type: ignore
from time import time  # type: ignore
from typing import Optional
from bridge import const
from bridge.auxiliary import aux, fld, rbt  # type: ignore
from bridge.const import State as GameStates
from bridge.router.base_actions import Action, Actions, KickActions  # type: ignore
from bridge.strategy.AttakerNeymar import Attaker_Neymar


class Strategy:
    """Main class of strategy"""

    def __init__(
        self,
    ) -> None:
        self.we_active = False
        self.i = 0

    def process(self, field: fld.Field) -> list[Optional[Action]]:
        """Game State Management"""
        if field.game_state not in [GameStates.KICKOFF, GameStates.PENALTY]:
            if field.active_team in [const.Color.ALL, field.ally_color]:
                self.we_active = True
            else:
                self.we_active = False

        actions: list[Optional[Action]] = []
        for _ in range(const.TEAM_ROBOTS_MAX_COUNT):
            actions.append(None)

        if field.ally_color == const.COLOR:
            text = str(field.game_state) + "  we_active:" + str(self.we_active)
            field.strategy_image.print(aux.Point(600, 780), text, need_to_scale=False)
        match field.game_state:
            case GameStates.RUN:
                self.run(field, actions)
            case GameStates.TIMEOUT:
                pass
            case GameStates.HALT:
                return [None] * const.TEAM_ROBOTS_MAX_COUNT
            case GameStates.PREPARE_PENALTY:
                pass
            case GameStates.PENALTY:
                pass
            case GameStates.PREPARE_KICKOFF:
                pass
            case GameStates.KICKOFF:
                pass
            case GameStates.FREE_KICK:
                pass
            case GameStates.STOP:
                # The router will automatically prevent robots from getting too close to the ball
                self.run(field, actions)

        return actions

    def run(self, field: fld.Field, actions: list[Optional[Action]]) -> None:
        """
        ONE ITERATION of strategy
        NOTE: robots will not start acting until this function returns an array of actions,
              if an action is overwritten during the process, only the last one will be executed)

        Examples of getting coordinates:
        - field.allies[8].get_pos(): aux.Point -   coordinates  of the 8th  robot from the allies
        - field.enemies[14].get_angle(): float - rotation angle of the 14th robot from the opponents

        - field.ally_goal.center: Point - center of the ally goal
        - field.enemy_goal.hull: list[Point] - polygon around the enemy goal area


        Examples of robot control:
        - actions[2] = Actions.GoToPoint(aux.Point(1000, 500), math.pi / 2)
                The robot number 2 will go to the point (1000, 500), looking in the direction π/2 (up, along the OY axis)

        - actions[3] = Actions.Kick(field.enemy_goal.center)
                The robot number 3 will hit the ball to 'field.enemy_goal.center' (to the center of the enemy goal)

        - actions[9] = Actions.BallGrab(0.0)
                The robot number 9 grabs the ball at an angle of 0.0 (it looks to the right, along the OX axis)
        """
        # c = (aux.dist(field.enemies[0].get_pos(), field.allies[0].get_pos()))/8
        # d = aux.point_on_line(field.allies[0].get_pos(), field.enemies[0].get_pos(), c)

        # u = aux.rotate(aux.Point(500, 0), ((3.14/4)*3) + 3.14 + (time())/3)
        # actions[3] = Actions.GoToPointIgnore(field.ball.get_pos() + u, (field.ball.get_pos() - field.allies[3].get_pos()).arg())
           
        # if(self.i == 0):
        #     actions[3] = Actions.GoToPointIgnore(field.enemy_goal.frw_up, 1)
        #     if((field.allies[3].get_pos() - field.enemy_goal.frw_up).mag() < 250):
        #         self.i = 1
        # if(self.i == 1):
        #     actions[3] = Actions.GoToPointIgnore(field.enemy_goal.frw_down, 1)
        #     if((field.allies[3].get_pos() - field.enemy_goal.frw_down).mag() < 250):
        #         self.i = 2  
        # if(self.i == 2):
        #     actions[3] = Actions.GoToPointIgnore(field.ally_goal.frw_up, 1)
        #     if((field.allies[3].get_pos() - field.ally_goal.frw_up).mag() < 250):
        #         self.i = 3
        # if(self.i == 3):
        #     actions[3] = Actions.GoToPointIgnore(field.ally_goal.frw_down, 1)
        #     if((field.allies[3].get_pos() - field.ally_goal.frw_down).mag() < 250):
        #         self.i = 0
        
        # c = (field.allies[0].get_pos() - field.enemies[0].get_pos()).unity()
        # u = aux.rotate(c*100, 3.14/3 *2) + field.allies[3].get_pos()
        # if(self.i == 0):
        #     actions[3] = Actions.GoToPointIgnore(u + field.allies[3].get_pos(), 1)
        #     if((field.allies[3].get_pos() - (u + field.allies[3].get_pos())).mag() < 20):
        #         u = aux.rotate(c*100, 3.14/3 * 4) + field.allies[3].get_pos()
        #         self.i = 1
        # if(self.i == 1):
        #     actions[3] = Actions.GoToPointIgnore(u, 1)
        #     if((field.allies[3].get_pos() - (u + field.allies[3].get_pos())).mag() < 20):
        #         u = aux.rotate(u, 3.14/2 * 3)
        #         self.i = 2
        #     actions[3] = Actions.GoToPointIgnore(u, 1)
        
        # field.strategy_image.draw_line(field.ball.get_pos(), field.allies[0].get_pos())
        # field.strategy_image.draw_line(field.ball.get_pos(), field.allies[1].get_pos())
        # field.strategy_image.draw_line(field.ball.get_pos(), field.allies[2].get_pos())
        # field.strategy_image.draw_line(field.ball.get_pos(), field.allies[3].get_pos())
        # field.strategy_image.draw_line(field.ball.get_pos(), field.allies[4].get_pos())
        # field.strategy_image.draw_line(field.ball.get_pos(), field.allies[5].get_pos())
        # field.strategy_image.draw_line(field.ball.get_pos(), field.enemies[0].get_pos())
        # field.strategy_image.draw_line(field.ball.get_pos(), field.enemies[1].get_pos())
        # field.strategy_image.draw_line(field.ball.get_pos(), field.enemies[2].get_pos())
        # field.strategy_image.draw_line(field.ball.get_pos(), field.enemies[3].get_pos())
        # field.strategy_image.draw_line(field.ball.get_pos(), field.enemies[4].get_pos())
        # field.strategy_image.draw_line(field.ball.get_pos(), field.enemies[5].get_pos())

        # list = [field.ally_goal.center_down, 
        #         field.ally_goal.frw_down, 
        #         field.ally_goal.frw, 
        #         field.ally_goal.frw_up, 
        #         field.ally_goal.center_up,
        #         field.enemy_goal.center_down,
        #         field.enemy_goal.frw_down,
        #         field.enemy_goal.frw,
        #         field.enemy_goal.frw_up,
        #         field.enemy_goal.center_up,
        #         ]
        # c = aux.find_nearest_point(field.allies[3].get_pos(), list)
        # if(self.i == 0):
        #     actions[3] = Actions.GoToPointIgnore(field.ball.get_pos(), 1)
        #     field.strategy_image.draw_line(field.allies[3].get_pos(), field.ball.get_pos(), (200, 0, 0))
        #     if((field.allies[3].get_pos() - field.ball.get_pos()).mag() < 200):
        #         actions[3] = Actions.GoToPointIgnore(field.allies[3].get_pos(), 1)
        #         self.i = 1
        # if(self.i == 1):
        #     actions[3] = Actions.GoToPointIgnore(c, 1)
        #     field.strategy_image.draw_line(field.allies[3].get_pos(), c, (200, 0, 0))
        #     if((field.allies[3].get_pos() - c).mag() < 10):
        #         self.i = 0

                # self.i = 1
                # c = aux.dist(field.allies[3].get_pos(), field.ally_goal.center)
                # d = aux.dist(field.allies[3].get_pos(), field.enemy_goal.center)
                # if(self.i == 1):
                #     if(c < d):
                #         aux.find_nearest_point
                #         actions[3] = Actions.GoToPointIgnore(field.ally_goal.center, 1)
                #         if(field.allies[3].get_pos() - field.ally_goal.center).mag() < 250:
                #             actions[3] = Actions.GoToPointIgnore(field.allies[3].get_pos(), 1)
                #     else:
                #         actions[3] = Actions.GoToPointIgnore(field.enemy_goal.center, 1)
                #         if(field.allies[3].get_pos() - field.enemy_goal.center).mag() < 250:
                #             actions[3] = Actions.GoToPointIgnore(field.allies[3].get_pos(), 1)

        # c = field.enemies[0].get_angle()
        # d = (aux.rotate(aux.Point(500, 0) , c)).unity()
        
        # a = field.allies[0].get_angle()
        # b = (aux.rotate(aux.Point(500, 0) , a)).unity()

        # r = field.allies[4].get_angle()
        # g = (aux.rotate(aux.Point(500, 0) , r)).unity()
        
        # hdb = aux.get_line_intersection(d + field.enemies[0].get_pos(), d*500 + field.enemies[0].get_pos(), b + field.allies[0].get_pos(), b*500 + field.allies[0].get_pos(), "LL")
        # hdg = aux.get_line_intersection(d + field.enemies[0].get_pos(), d*500 + field.enemies[0].get_pos(), g + field.allies[4].get_pos(), g*500 + field.allies[4].get_pos(), "LL")
        # hgb = aux.get_line_intersection(g + field.allies[4].get_pos(), g*500 + field.allies[4].get_pos(), b + field.allies[0].get_pos(), b*500 + field.allies[0].get_pos(), "LL")
        
        # if hdb is not None and hdg is not None and hgb is not None:
        #     f = (hdb + hdg + hgb)/3
        #     field.strategy_image.draw_circle(hdb, (255, 255, 255), 50)
        #     field.strategy_image.draw_circle(hdg, (255, 255, 255), 50)
        #     field.strategy_image.draw_circle(hgb, (255, 255, 255), 50)
        #     field.strategy_image.draw_line(d + field.enemies[0].get_pos(), d*3000 + field.enemies[0].get_pos())
        #     field.strategy_image.draw_line(g + field.allies[4].get_pos(), g*3000 + field.allies[4].get_pos())
        #     field.strategy_image.draw_line(b + field.allies[0].get_pos(), b*3000 + field.allies[0].get_pos())
        #     field.strategy_image.draw_circle(f, (255, 255, 255), 50)
        
        # w = aux.point_on_line(field.ball.get_pos(), field.enemies[0].get_pos(), -1000)
        # l = aux.angle_to_point(field.enemies[0].get_pos(), field.ball.get_pos())
        # p = aux.angle_to_point(field.enemies[0].get_pos(), field.allies[0].get_pos())
        # y = aux.angle_to_point(field.enemies[0].get_pos(), field.allies[5].get_pos())
        # print(l, p, y)
        # r = (aux.point_on_line(field.allies[0].get_pos(), field.enemies[0].get_pos(), 300))
        # u = (aux.point_on_line(field.allies[5].get_pos(), field.enemies[0].get_pos(), 300))
        # if((y - l) > (l - p)):
        #     actions[3] = Actions.GoToPointIgnore(r , (field.ball.get_pos() - field.allies[3].get_pos()).arg())
            
        # else:
        #     actions[3] = Actions.GoToPointIgnore(u , (field.ball.get_pos() - field.allies[3].get_pos()).arg())

        # list2 = [field.enemies[0],
        #         field.enemies[2],
        #         field.enemies[3],
        #         field.enemies[4],
        #         field.enemies[5]]
        # while((field.allies[2].get_pos()- aux.Point(0,0)).mag() > 100):
        #     actions[2] = Actions.GoToPointIgnore(aux.Point(0,0), (field.ball.get_pos() - field.allies[2].get_pos()).arg())

        # field.strategy_image.draw_line(field.ball.get_pos(), field.allies[2].get_pos())
        # q = aux.dist(field.ball.get_pos(), field.allies[2].get_pos())
        # z = aux.point_on_line(field.ball.get_pos(), field.allies[2].get_pos(), q)
        # y = (field.ball.get_pos() - field.allies[2].get_pos()).unity()*50000
        # b = -1
        # for b in range(6):
        #     b+=1
        #     if(aux.dist(aux.closest_point_on_line(field.ball.get_pos(), field.allies[2].get_pos(), field.enemies[b].get_pos(), "S"), field.enemies[b].get_pos()) < 100):
        #         e = aux.get_angle_between_points(field.allies[2].get_pos(), field.ball.get_pos(), field.enemies[b].get_pos())
        #         if(e<0):
        #             # while(aux.dist(aux.closest_point_on_line(field.ball.get_pos(), field.allies[2].get_pos(), field.enemies[b].get_pos(), "S"), field.enemies[b].get_pos()) < 100):
        #             actions[2] = Actions.GoToPointIgnore(aux.rotate(y, 3.14/2), (field.ball.get_pos() - field.allies[2].get_pos()).arg())
        #             # actions[2] = Actions.GoToPointIgnore(field.allies[2].get_pos(), (field.ball.get_pos() - field.allies[2].get_pos()).arg())
        #         else:
        #             # while(aux.dist(aux.closest_point_on_line(field.ball.get_pos(), field.allies[2].get_pos(), field.enemies[b].get_pos(), "S"), field.enemies[b].get_pos()) < 100):
        #             actions[2] = Actions.GoToPointIgnore(aux.rotate(y, -3.14/2), (field.ball.get_pos() - field.allies[2].get_pos()).arg())
        #             # actions[2] = Actions.GoToPointIgnore(field.allies[2].get_pos(), (field.ball.get_pos() - field.allies[2].get_pos()).arg())
        # field.strategy_image.send_telemetry()

        # actions[0] = Actions.Kick(field.ally_goal.center)
        # actions[1] = Actions.Kick(field.enemy_goal.center)
        # actions[2] = Actions.Kick(field.allies[0].get_pos())
        # actions[3] = Actions.Kick(field.allies[1].get_pos())
        # actions[2] = Actions.Kick(field.ally_goal.center)

        # b = -1
        # p = field.enemy_goal.center_down + aux.Point(0, 500)
        # o = field.enemy_goal.center_up + aux.Point(0, -500)
        # for b in range(2):
        #     b+=1
        #     if(aux.dist(aux.closest_point_on_line(p, o, field.enemies[b].get_pos(), "S"), field.enemies[b].get_pos()) < 1000):
        #         l = aux.find_nearest_point(field.enemies[b].get_pos(), [p, o])
        #         if(l == field.enemy_goal.center_down):
        #             actions[2] = Actions.Kick(o)
        #         else:
        #             actions[2] = Actions.Kick(p)

        # field.is_ball_moves_to_goal()

        # if field.ally_color == const.Color.BLUE:
        #     # actions[2] = Actions.Kick(choose_on_goal(field, 2))
        #     # field.strategy_image.draw_poly([field.enemy_goal.frw_down, field.enemy_goal.center_down, field.enemy_goal.frw_up, field.enemy_goal.center_up])
        #     b = -1
        #     p = field.enemy_goal.center_down + aux.Point(0, 500)
        #     o = field.enemy_goal.center_up + aux.Point(0, -500)
        #     for b in range(2):
        #         b+=1
        #         if(aux.dist(aux.closest_point_on_line(p, o, field.enemies[b].get_pos(), "S"), field.enemies[b].get_pos()) < 1000):
        #             l = aux.find_nearest_point(field.enemies[b].get_pos(), [p, o])
        #             if(l == field.enemy_goal.center_down):
        #                 actions[2] = Actions.Kick(o)
        #             else:
        #                 actions[2] = Actions.Kick(p)
        # else:
        #     # actions[2] = Actions.GoToPointIgnore(field.ally_goal.center, 1)
            
        #     if(aux.is_point_inside_poly(field.allies[1].get_pos(), field.ally_goal.hull)):
        #         if(field.ball.get_vel() == 0):
        #             d = aux.angle_to_point(field.enemies[2].get_pos(), field.ball.get_pos())
        #             q = aux.rotate(aux.Point(300, 0), d).unity()
        #             w = aux.closest_point_on_line(field.enemies[2].get_pos(), field.ball.get_pos(), field.allies[1].get_pos(), "L")
                    
        #             actions[1] = Actions.GoToPoint(w, d+3.14)
                    
        #         else:
        #             n = field.ball.get_vel().arg()
        #             actions[1] = Actions.GoToPoint(aux.rotate(aux.Point(200, 0), n+3.14).unity()*100 + field.allies[1].get_pos(), 1)

                
                
                
        #     else:
                
        #         actions[1] = Actions.GoToPoint(field.ally_goal.center, 1)
        # class Attaker:
        #     def __init__(self) -> None:
        #         self.idx: int = 1
        #     def func(self) -> None:
        #         self.idx = "d"
        #     def goalkeeper(self, ball_pos: aux.Point, num: int) -> tuple[rbt.Robot, aux.Point]:
        #         pp = 0
        #         pp += 1

        #         numm: float
        #         if pp == 0:
        #             numm = 1
        #         else:
        #             numm = 1.5
        #         numm += 1

        #         return rbt.Robot(aux.Point(0, 0), 0, 0, const.Color.BLUE, 0), aux.Point(0, 0)

        # actions[2] = Attaker_Neymar.Pass_Ronaldo(field.allies[0].get_pos())
        if field.ally_color == const.Color.BLUE:
            Attaker_Neymar.run_Neymar(field, actions)


                
                    
                
# 🐥🐥🐥🐥🐥🐥🐥🐥🐥🐥🐥🐥🐥🐥🐥
# def choose_on_goal(field: fld.Field, robots: int):
#     l = 0
#     while(l == 0):
#         b = -1
#         p = field.enemy_goal.center_down + aux.Point(0, 500)
#         o = field.enemy_goal.center_up + aux.Point(0, -500)
        
#         for b in range(robots):
#             b+=1
#             if(aux.dist(aux.closest_point_on_line(p, o, field.enemies[b].get_pos(), "S"), field.enemies[b].get_pos()) < 5000):
#                 l = aux.find_nearest_point(field.enemies[b].get_pos(), [p, o])
#                 if(l == field.enemy_goal.center_down):
#                     return o
#                 elif(l == field.enemy_goal.center_up):
#                     return p

                

                
    
            
            
            


            
                    

        
            
            

        
        
            
            




        

