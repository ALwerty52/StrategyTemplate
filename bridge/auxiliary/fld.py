"""
Модуль описания структуры Field для хранения информации об объектах на поле (роботы и мяч)
"""

from math import cos, pi
from typing import Optional

from bridge import const, drawing
from bridge.auxiliary import aux, entity, rbt


class Goal:
    """
    Структура, описывающая ключевые точки ворот
    """

    def __init__(self, goal_dx: float, goal_dy: float, pen_dx: float, pen_dy: float) -> None:
        """
        Location of goalkeeper area points (goal on top, down and up - bars):


                                       ┌───────────────────────────────┐
               center_down             │            center             │              center_up
        ────────────◉──────────────────◉───────────────◉───────────────◉──────────────────◉──────────────
                    │                down                            up                   │
                    │                                                                     │
                    │                                                                     │
                    │                                                                     │
                    │                                                                     │          ────> eye_up
                    │                                                                     │
                    │                                                                     │
                    │                                                                     │
                    │                                 frw                                 │
                    ◉──────────────────────────────────◉──────────────────────────────────◉
                 frw_down                                                              frw_up
                                                       ||
                                                       ||
                                                       \/ eye_frw
        """
        # Абсолютный центр
        self.center = aux.Point(goal_dx, 0)

        # Относительные вектора
        self.eye_forw = aux.Point(-aux.sign(goal_dx), 0)
        self.eye_up = aux.Point(0, aux.sign(goal_dy))

        self.vec_up = aux.Point(0, goal_dy / 2)
        self.vec_pen = aux.Point(-pen_dx, 0)
        self.vec_pen_up = aux.Point(0, pen_dy / 2)

        # Абсолютные вектора
        self.up = self.center + self.vec_up
        self.down = self.center - self.vec_up
        self.frw = self.center + self.vec_pen
        self.frw_up = self.frw + self.vec_pen_up
        self.frw_down = self.frw - self.vec_pen_up

        self.center_up = self.center + self.vec_pen_up
        self.center_down = self.center - self.vec_pen_up

        # Оболочка штрафной зоны
        self.hull = [
            aux.FIELD_INF * self.eye_forw.x,
            self.center_up,
            self.frw_up,
            self.frw_down,
            self.center_down,
        ]

        self.big_hull = [
            aux.FIELD_INF * self.eye_forw.x,
            self.center_up + self.eye_up * const.ROBOT_R * 1.5,
            self.frw_up + (self.eye_forw + self.eye_up) * const.ROBOT_R * 1.5,
            self.frw_down + (self.eye_forw - self.eye_up) * const.ROBOT_R * 1.5,
            self.center_down - self.eye_up * const.ROBOT_R * 1.5,
        ]

        stop_delta = 500
        self.stop_hull = [
            aux.FIELD_INF * self.eye_forw.x,
            self.center_up + self.eye_up * stop_delta,
            self.frw_up + (self.eye_forw + self.eye_up) * stop_delta,
            self.frw_down + (self.eye_forw - self.eye_up) * stop_delta,
            self.center_down - self.eye_up * stop_delta,
        ]

        self.big_stop_hull = [
            aux.FIELD_INF * self.eye_forw.x,
            self.center_up + self.eye_up * (stop_delta + const.ROBOT_R * 1.5),
            self.frw_up + (self.eye_forw + self.eye_up) * (stop_delta + const.ROBOT_R * 1.5),
            self.frw_down + (self.eye_forw - self.eye_up) * (stop_delta + const.ROBOT_R * 1.5),
            self.center_down - self.eye_up * (stop_delta + const.ROBOT_R * 1.5),
        ]


class Field:
    """
    Класс, хранящий информацию о всех объектах на поле и ключевых точках
    """

    def __init__(self, color: const.Color) -> None:
        """
        Конструктор
        Инициализирует все нулями

        TODO Сделать инициализацию реальными параметрами для корректного
        определения скоростей и ускорений в первые секунды
        """
        self.game_state: const.State = const.State.STOP
        self.active_team: const.Color = const.Color.ALL
        self.last_update = 0.0
        self.robot_with_ball: Optional[rbt.Robot] = None

        self.field_image = drawing.Image(drawing.ImageTopic.FIELD)
        self.strategy_image = drawing.Image(drawing.ImageTopic.STRATEGY)
        self.router_image = drawing.Image(drawing.ImageTopic.ROUTER)
        self.path_image = drawing.Image(drawing.ImageTopic.PATH_GENERATION)

        self.ally_color = color
        if self.ally_color == const.COLOR:
            self.gk_id = const.GK
            self.enemy_gk_id = const.ENEMY_GK
        else:
            self.gk_id = const.ENEMY_GK
            self.enemy_gk_id = const.GK

        if self.ally_color == const.Color.BLUE:
            self.polarity = const.POLARITY * -1
        else:
            self.polarity = const.POLARITY

        self.ball = entity.Entity(aux.GRAVEYARD_POS, 0, const.BALL_R, 0.2)
        self.b_team = [
            rbt.Robot(
                aux.GRAVEYARD_POS,
                0,
                const.ROBOT_R,
                const.Color.BLUE,
                i,
            )
            for i in range(const.TEAM_ROBOTS_MAX_COUNT)
        ]
        self.y_team = [
            rbt.Robot(
                aux.GRAVEYARD_POS,
                0,
                const.ROBOT_R,
                const.Color.YELLOW,
                i,
            )
            for i in range(const.TEAM_ROBOTS_MAX_COUNT)
        ]
        self.all_bots = [*self.b_team, *self.y_team]
        self.ally_goal = Goal(
            const.GOAL_DX * self.polarity,
            const.GOAL_DY * self.polarity,
            const.GOAL_PEN_DX * self.polarity,
            const.GOAL_PEN_DY * self.polarity,
        )
        self.enemy_goal = Goal(
            -const.GOAL_DX * self.polarity,
            -const.GOAL_DY * self.polarity,
            -const.GOAL_PEN_DX * self.polarity,
            -const.GOAL_PEN_DY * self.polarity,
        )

        if const.SELF_PLAY:
            self.enemy_goal = self.ally_goal

        if self.ally_color == const.Color.BLUE:
            self.allies = [*self.b_team]
            self.enemies = [*self.y_team]
        elif self.ally_color == const.Color.YELLOW:
            self.allies = [*self.y_team]
            self.enemies = [*self.b_team]

        self.hull = [
            aux.Point(const.FIELD_DX, const.FIELD_DY),
            aux.Point(const.FIELD_DX, -const.FIELD_DY),
            aux.Point(-const.FIELD_DX, -const.FIELD_DY),
            aux.Point(-const.FIELD_DX, const.FIELD_DY),
        ]

        self._active_allies: list[rbt.Robot] = []
        self._active_enemies: list[rbt.Robot] = []

        self.ball_history: list[Optional[aux.Point]] = [None] * round(0.1 / const.Ts)
        self.ball_history_idx = 0
        self.ball_start_point: aux.Point = self.ball.get_pos()

        self.ball_real_update_time = 0.0

    def clear_images(self) -> None:
        """clear old data from images"""
        self.strategy_image.clear()
        self.router_image.clear()
        self.path_image.clear()

    def active_allies(self, include_gk: bool = False) -> list[rbt.Robot]:
        """return allies on field"""
        robots = self._active_allies
        if include_gk and self.allies[self.gk_id].is_used():
            robots.append(self.allies[self.gk_id])
        return robots

    def active_enemies(self, include_gk: bool = False) -> list[rbt.Robot]:
        """return enemies on field"""
        robots = self._active_enemies
        if include_gk and self.enemies[self.enemy_gk_id].is_used():
            robots.append(self.enemies[self.enemy_gk_id])
        return robots

    def update_field(self, new_field: "LiteField") -> None:
        """update with data from new_field"""
        self.game_state = new_field.game_state
        self.active_team = new_field.active_team

        if new_field.robot_with_ball is None:
            self.robot_with_ball = None
        elif new_field.robot_with_ball[0] == const.Color.BLUE:
            self.robot_with_ball = self.b_team[new_field.robot_with_ball[1]]
        else:
            self.robot_with_ball = self.y_team[new_field.robot_with_ball[1]]

        self.last_update = new_field.last_update

        self.ball = new_field.ball
        self.ball_start_point = new_field.ball_start_point

        for robot in self.all_bots:
            robot.used(0)
        for lite_robot in new_field.blue_team:
            self.b_team[lite_robot.r_id].update_(lite_robot)
        for lite_robot in new_field.yellow_team:
            self.y_team[lite_robot.r_id].update_(lite_robot)

        self.update_active_allies([robot for robot in self.allies if robot.is_used()])
        self.update_active_enemies([robot for robot in self.enemies if robot.is_used()])

    def update_ball(self, pos: aux.Point, t: float) -> None:
        """update ball position"""
        self.ball.update(pos, 0, t)

    def update_ball_history(self) -> None:
        """updates the list with the latest ball positions"""
        old_ball = self.ball_history[self.ball_history_idx]
        if old_ball is None:
            self.ball_start_point = self.ball.get_pos() - self.ball.get_vel()
        else:
            self.ball_start_point = old_ball

        self.ball_history[self.ball_history_idx] = self.ball.get_pos()
        self.ball_history_idx += 1
        self.ball_history_idx %= len(self.ball_history)

        if self.robot_with_ball is not None:
            length = len(self.ball_history)
            self.ball_history = [self.robot_with_ball.get_pos() for _ in range(length)]

    def _is_ball_in(self, robo: rbt.Robot) -> bool:
        """
        Определить, находится ли мяч внутри дрибблера
        """
        return (robo.get_pos() - self.ball.get_pos()).mag() < const.BALL_GRABBED_DIST and abs(
            aux.wind_down_angle((self.ball.get_pos() - robo.get_pos()).arg() - robo.get_angle())
        ) < const.BALL_GRABBED_ANGLE

    def is_ball_in(self, robo: rbt.Robot) -> bool:
        """
        Определить, находится ли мяч внутри дрибблера
        """
        return robo == self.robot_with_ball

    def update_blu_robot(self, idx: int, pos: aux.Point, angle: float, t: float) -> None:
        """
        Обновить положение робота синей команды
        !!! Вызывать один раз за итерацию с постоянной частотой !!!
        """
        self.b_team[idx].update(pos, angle, t)

    def update_yel_robot(self, idx: int, pos: aux.Point, angle: float, t: float) -> None:
        """
        Обновить положение робота желтой команды
        !!! Вызывать один раз за итерацию с постоянной частотой !!!
        """
        self.y_team[idx].update(pos, angle, t)

    def update_active_enemies(self, active_enemies: list[rbt.Robot]) -> None:
        """Обновляет список активных роботов-союзников"""
        self._active_enemies = active_enemies

    def update_active_allies(self, active_allies: list[rbt.Robot]) -> None:
        """Обновляет список активных роботов-противников"""
        self._active_allies = active_allies

    def get_blu_team(self) -> list[rbt.Robot]:
        """
        Получить массив роботов синей команды

        @return Массив entity.Entity[]
        """
        return self.b_team

    def get_yel_team(self) -> list[rbt.Robot]:
        """
        Получить массив роботов желтой команды

        @return Массив entity.Entity[]
        """
        return self.y_team

    def is_ball_stop_near_goal(self) -> bool:
        """
        Определить, остановился ли мяч в штрафной зоне
        """
        return aux.is_point_inside_poly(self.ball.get_pos(), self.ally_goal.hull) and not self.is_ball_moves()

    def is_ball_moves(self) -> bool:
        """
        Определить, движется ли мяч
        """
        return self.ball.get_vel().mag() > const.INTERCEPT_SPEED

    def is_ball_moves_to_point(self, point: aux.Point, align: float = pi / 2) -> bool:
        """
        Определить, движется ли мяч в сторону точки
        """
        vec_to_point = point - self.ball.get_pos()
        return (
            self.ball.get_vel().mag() * (cos(vec_to_point.arg() - self.ball.get_vel().arg()) ** 5)
            > const.INTERCEPT_SPEED * 5
            and self.robot_with_ball is None
            and abs(vec_to_point.arg() - self.ball.get_vel().arg()) < align
        )

    def is_ball_moves_to_goal(self) -> bool:
        """
        Определить, движется ли мяч в сторону ворот
        """
        if self.ball_start_point is None:
            return False

        inter = aux.get_line_intersection(
            self.ally_goal.center_up,
            self.ally_goal.center_down,
            self.ball_start_point,
            self.ball.get_pos(),
            "SR",
        )
        return inter is not None and self.is_ball_moves()

    def is_ball_moves_to_enemy_goal(self) -> bool:
        """
        Определить, движется ли мяч в сторону ворот
        """
        if self.ball_start_point is None:
            return False

        inter = aux.get_line_intersection(
            self.enemy_goal.up,
            self.enemy_goal.down,
            self.ball_start_point,
            self.ball.get_pos(),
            "SR",
        )
        return inter is not None and self.is_ball_moves()


def find_nearest_robot(point: aux.Point, team: list[rbt.Robot], avoid: Optional[list[int]] = None) -> rbt.Robot:
    """
    Найти ближайший робот из массива team к точке point, игнорируя точки avoid
    """
    if avoid is None:
        avoid = []
    robo_id = 0
    min_dist = 10e10

    if len(team) == 0:
        return rbt.Robot(aux.GRAVEYARD_POS, 0, 0, const.Color.ALL, 0)

    for i, player in enumerate(team):
        if player.r_id in avoid or not player.is_used():
            continue
        if aux.dist(point, player.get_pos()) < min_dist:
            min_dist = aux.dist(point, player.get_pos())
            robo_id = i

    return team[robo_id]


def find_nearest_robots(
    point: aux.Point,
    team: list[rbt.Robot],
    num: Optional[int] = None,
    avoid: Optional[list[int]] = None,
) -> list[rbt.Robot]:
    """
    Найти num роботов из team, ближайших к точке point
    """
    if num is None:
        num = len(team)
    if avoid is None:
        avoid = []

    robot_dist: list[tuple[rbt.Robot, float]] = []

    for robot in team:  # in [field.enemies, field.allies]
        dist = (robot.get_pos() - point).mag()
        if robot.is_used():
            robot_dist.append((robot, dist))

    sorted_robot_dist = sorted(robot_dist, key=lambda x: x[1])

    sorted_robots: list[rbt.Robot] = [rbt_dst[0] for rbt_dst in sorted_robot_dist]

    return sorted_robots[:num]


class LiteField:
    """Lite class, to moving information about robots and ball between processes"""

    def __init__(self, field: Field) -> None:
        self.game_state: const.State = field.game_state
        self.active_team: const.Color = field.active_team
        self.last_update = field.last_update
        self.robot_with_ball: Optional[tuple[const.Color, int]]
        if field.robot_with_ball is None:
            self.robot_with_ball = None
        else:
            self.robot_with_ball = (field.robot_with_ball.color, field.robot_with_ball.r_id)

        self.ball: entity.Entity = field.ball
        self.ball_start_point: aux.Point = field.ball_start_point

        self.blue_team = [rbt.LiteRobot(robot) for robot in field.b_team if robot.is_used()]
        self.yellow_team = [rbt.LiteRobot(robot) for robot in field.y_team if robot.is_used()]
