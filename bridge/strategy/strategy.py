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
        self.neymar = Attaker_Neymar()

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
        if field.ally_color == const.Color.BLUE:
            self.neymar.choose_point_to_goal(field, actions)


                
                    
                
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

                

                
    
            
            
            


            
                    

        
            
            

        
        
            
            




        

