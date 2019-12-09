from threading import Thread
from typing import List, Tuple
from queue import SimpleQueue as Queue

Memory = List[int]


class IntCode(Thread):

    @property
    def opcode(self) -> int:
        padded_instruction = f"{self.memory[self.instruction_pointer]:05}"
        return int(padded_instruction[3:5])

    @property
    def modes(self) -> Tuple[int, int, int]:
        padded_instruction = f"{self.memory[self.instruction_pointer]:05}"
        mode_3 = int(padded_instruction[0])
        mode_2 = int(padded_instruction[1])
        mode_1 = int(padded_instruction[2])
        return mode_1, mode_2, mode_3

    def __init__(self,
                 memory: Memory,
                 input_queue: Queue,
                 output_queue: Queue):
        Thread.__init__(self)

        self.memory = memory
        self.instruction_pointer = 0
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.halted = False

    def read(self, parameter_number: int) -> int:
        parameter_pointer = self.instruction_pointer + parameter_number

        param = self.memory[parameter_pointer]
        mode = self.modes[parameter_number - 1]

        if mode == 0:
            return self.memory[param]

        if mode == 1:
            return param

        raise Exception(f"unknown mode: [{mode}]")

    def write(self, parameter_number: int, value: int) -> None:

        parameter_pointer = self.instruction_pointer + parameter_number
        param = self.memory[parameter_pointer]

        self.memory[param] = value

    # pylint: disable=R0912,R0914,R0915,C0301
    def run(self) -> None:

        while True:

            opcode = self.opcode

            if opcode == 1:
                value_1 = self.read(1)
                value_2 = self.read(2)

                self.write(3, value_1 + value_2)

                instruction_pointer_shift = 4

            elif opcode == 2:
                value_1 = self.read(1)
                value_2 = self.read(2)

                self.write(3, value_1 * value_2)

                instruction_pointer_shift = 4

            elif opcode == 3:

                value_1 = self.input_queue.get(block=True)

                self.write(1, value_1)

                instruction_pointer_shift = 2

            elif opcode == 4:
                value_1 = self.read(1)

                self.output_queue.put(value_1)

                instruction_pointer_shift = 2

            elif opcode == 5:
                condition = self.read(1)
                if condition != 0:
                    self.instruction_pointer = self.read(2)
                    instruction_pointer_shift = 0
                else:
                    instruction_pointer_shift = 3

            elif opcode == 6:
                condition = self.read(1)
                if condition == 0:
                    self.instruction_pointer = self.read(2)
                    instruction_pointer_shift = 0
                else:
                    instruction_pointer_shift = 3

            elif opcode == 7:
                value_1 = self.read(1)
                value_2 = self.read(2)

                if value_1 < value_2:
                    target_value = 1
                else:
                    target_value = 0

                self.write(3, target_value)

                instruction_pointer_shift = 4

            elif opcode == 8:
                value_1 = self.read(1)
                value_2 = self.read(2)

                if value_1 == value_2:
                    target_value = 1
                else:
                    target_value = 0

                self.write(3, target_value)

                instruction_pointer_shift = 4

            elif opcode == 99:
                self.halted = True
                return

            else:
                raise Exception(f"unknown opcode [{opcode}]")

            self.instruction_pointer += instruction_pointer_shift
