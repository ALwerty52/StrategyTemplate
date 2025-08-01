"""
Модуль стратегии игры
"""

from time import time
from typing import Optional

import attr
from strategy_bridge.bus import DataBus, DataReader, DataWriter
from strategy_bridge.processors import BaseProcessor
from strategy_bridge.utils.debugger import debugger

from bridge import const, drawing
from bridge.auxiliary import fld
from bridge.router.action import Action
from bridge.strategy import strategy


class RobotCommand:
    """Command to control robot"""

    def __init__(self, r_id: int, color: const.Color, action: Action) -> None:
        self.r_id: int = r_id
        self.color: const.Color = color
        self.action: Action = action


@attr.s(auto_attribs=True)
class SSLController(BaseProcessor):
    """
    Процессор стратегии SSL
    """

    processing_pause: float = const.Ts
    reduce_pause_on_process_time: bool = True
    max_commands_to_persist: int = 20

    ally_color: const.Color = const.Color.BLUE

    cur_time = time()
    delta_t = 0.0

    count_halt_cmd = 0

    def initialize(self, data_bus: DataBus) -> None:
        """
        Инициализировать контроллер
        """
        super().initialize(data_bus)
        self.field_reader = DataReader(data_bus, const.FIELD_TOPIC)

        self.robot_control_writer = DataWriter(data_bus, const.CONTROL_TOPIC, 50)
        self.image_writer = DataWriter(data_bus, const.IMAGE_TOPIC, 20)

        self.field = fld.Field(self.ally_color)
        self.field.strategy_image.timer = drawing.FeedbackTimer(time(), 0.05, 40)

        self.strategy = strategy.Strategy()
        self.actions: list[Optional[Action]] = []

    def read_vision(self) -> None:
        """
        Прочитать новые пакеты из SSL-Vision
        """
        new_field = self.field_reader.read_last()
        if new_field is not None:
            updated_field: fld.LiteField = new_field.content
            # print(f"strategy daley{(time() - new_field.timestamp)*1000 : .2f}")
            self.field.update_field(updated_field)
        else:
            print("No new field")

    def control_loop(self) -> None:
        """
        Рассчитать стратегию, тактику и физику для роботов на поле
        """
        self.actions = self.strategy.process(self.field)

    def control_assign(self) -> None:
        """Send commands to robots"""
        for robot in self.field.active_allies(True):
            cur_action = self.actions[robot.r_id]
            if cur_action is not None:
                message = RobotCommand(robot.r_id, robot.color, cur_action)

                self.robot_control_writer.write(message)

    def send_image(self) -> None:
        """Send commands to drawer processor"""
        self.field.strategy_image.timer.end(time())
        if self.field.ally_color == const.COLOR:
            self.image_writer.write(self.field.strategy_image)
        self.field.clear_images()

    @debugger
    def process(self) -> None:
        """
        Выполнить цикл процессора
        """
        self.field.strategy_image.timer.start(time())

        self.read_vision()
        self.control_loop()

        self.control_assign()
        self.send_image()
