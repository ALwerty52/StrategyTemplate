"""
Class with strategy actions
"""

from bridge import const
from bridge.auxiliary import aux
from bridge.router.action import Action, ActionDomain, ActionValues
from bridge.router.base_actions import Actions


class StrategyActions:
    """Class with strategy actions"""

    class CatchBall(Action):
        """Catch ball or avoid it, if it is moving to goal"""

        def use_behavior_of(self, domain: ActionDomain, current_action: ActionValues) -> list[Action]:
            can_enemy_catch_ball = False
            eye_angle = aux.angle_to_point(domain.field.ball.get_pos(), domain.field.ball_start_point)

            ball_vec = domain.field.ball.get_pos() - domain.field.ball_start_point
            for enemy in domain.field.active_enemies(True):
                pnt = aux.closest_point_on_line(
                    domain.field.ball.get_pos(),
                    domain.field.ball.get_pos() + ball_vec,
                    enemy.get_pos(),
                    "R",
                )
                if aux.dist(pnt, enemy.get_pos()) < 2 * const.ROBOT_R:
                    can_enemy_catch_ball = True
                    break

            if (
                domain.field.is_ball_moves_to_enemy_goal()
                and domain.field.ball.get_vel().mag() > 500
                and not can_enemy_catch_ball
            ):
                # avoid the ball, because it may be a goal
                vec = domain.robot.get_pos() - aux.closest_point_on_line(
                    domain.field.ball_start_point, domain.field.ball.get_pos(), domain.robot.get_pos()
                )
                return [Actions.GoToPointIgnore(domain.robot.get_pos() + vec.unity() * 500, eye_angle)]

            target = aux.closest_point_on_line(
                domain.field.ball_start_point,
                domain.field.ball.get_pos(),
                domain.robot.get_pos(),
                "R",
            )
            domain.field.strategy_image.draw_line(target, domain.robot.get_pos(), (255, 127, 0), 2)
            domain.field.strategy_image.draw_dot(target, (128, 128, 255), const.ROBOT_R)

            return [Actions.GoToPointIgnore(target, eye_angle)]
