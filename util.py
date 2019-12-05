from typing import List, Tuple


def parse_instruction(instruction: int) -> Tuple[Tuple[int, int, int], int]:
    padded_instruction = f"{instruction:05}"

    mode_3 = int(padded_instruction[0])
    mode_2 = int(padded_instruction[1])
    mode_1 = int(padded_instruction[2])
    opcode = int(padded_instruction[3:5])

    return (mode_1, mode_2, mode_3), opcode


def read(data: List[int],
         instruction_pointer: int,
         parameter_number,
         modes: Tuple[int, int, int]) -> int:
    parameter_pointer = instruction_pointer + parameter_number
    param = data[parameter_pointer]

    mode = modes[parameter_number - 1]

    if mode == 0:
        return data[param]

    if mode == 1:
        return param

    print(f"unknown mode: [{mode}]")
    return -1


def write(data: List[int], instruction_pointer: int, parameter_number: int, value: int) -> None:
    parameter_pointer = instruction_pointer + parameter_number
    param = data[parameter_pointer]

    data[param] = value


# pylint: disable=R0912,R0914,R0915
# pylint does not like to many branches, local vars and statements. I don't care.
def intcode(data: List[int], inputs=None, instruction_pointer: int = 0) -> Tuple[int, List[int]]:
    """
    >>> intcode([1,0,0,0,99])
    (2, [])

    >>> intcode([2,3,0,3,99])
    (2, [])

    >>> intcode([2,2,2,0,99])
    (4, [])

    >>> intcode([2,4,4,5,99,0])
    (2, [])

    >>> intcode([1,1,1,4,99,5,6,0,99])
    (30, [])

    >>> intcode([3,9,8,9,10,9,4,9,99,-1,8], [8])
    (3, [1])

    >>> intcode([3,9,8,9,10,9,4,9,99,-1,8], [7])
    (3, [0])

    # less than 8, position
    >>> intcode([3,9,7,9,10,9,4,9,99,-1,8], [7])
    (3, [1])
    >>> intcode([3,9,7,9,10,9,4,9,99,-1,8], [9])
    (3, [0])

    # equal to 8, immediate
    >>> intcode([3,3,1108,-1,8,3,4,3,99], [8])
    (3, [1])
    >>> intcode([3,3,1108,-1,8,3,4,3,99], [7])
    (3, [0])

    # less than 8, immediate
    >>> intcode([3,3,1107,-1,8,3,4,3,99], [7])
    (3, [1])
    >>> intcode([3,3,1107,-1,8,3,4,3,99], [9])
    (3, [0])

    # jump, position
    >>> intcode([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [1])
    (3, [1])
    >>> intcode([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [0])
    (3, [0])

    # jump, immediate
    >>> intcode([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [1])
    (3, [1])
    >>> intcode([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [0])
    (3, [0])

    """

    if inputs is None:
        inputs = []
    outputs: List[int] = []

    while True:

        modes, opcode = parse_instruction(data[instruction_pointer])

        if opcode == 1:
            from_1 = read(data, instruction_pointer, 1, modes)
            from_2 = read(data, instruction_pointer, 2, modes)

            write(data, instruction_pointer, 3, from_1 + from_2)

            instruction_pointer_shift = 4

        elif opcode == 2:
            from_1 = read(data, instruction_pointer, 1, modes)
            from_2 = read(data, instruction_pointer, 2, modes)

            write(data, instruction_pointer, 3, from_1 * from_2)

            instruction_pointer_shift = 4

        elif opcode == 3:
            if len(inputs) == 0:
                raise Exception("ran out of inputs")

            from_1 = inputs[0]
            inputs = inputs[1:]

            write(data, instruction_pointer, 1, from_1)

            instruction_pointer_shift = 2

        elif opcode == 4:
            from_1 = read(data, instruction_pointer, 1, modes)

            outputs.append(from_1)

            instruction_pointer_shift = 2

        elif opcode == 5:
            condition = read(data, instruction_pointer, 1, modes)
            if condition != 0:
                new_instruction_pointer = read(data, instruction_pointer, 2, modes)
                instruction_pointer = new_instruction_pointer
                instruction_pointer_shift = 0
            else:
                instruction_pointer_shift = 3

        elif opcode == 6:
            condition = read(data, instruction_pointer, 1, modes)
            if condition == 0:
                new_instruction_pointer = read(data, instruction_pointer, 2, modes)
                instruction_pointer = new_instruction_pointer
                instruction_pointer_shift = 0
            else:
                instruction_pointer_shift = 3

        elif opcode == 7:
            value_1 = read(data, instruction_pointer, 1, modes)
            value_2 = read(data, instruction_pointer, 2, modes)

            if value_1 < value_2:
                target_value = 1
            else:
                target_value = 0

            write(data, instruction_pointer, 3, target_value)

            instruction_pointer_shift = 4

        elif opcode == 8:
            value_1 = read(data, instruction_pointer, 1, modes)
            value_2 = read(data, instruction_pointer, 2, modes)

            if value_1 == value_2:
                target_value = 1
            else:
                target_value = 0

            write(data, instruction_pointer, 3, target_value)

            instruction_pointer_shift = 4

        elif opcode == 99:
            return data[0], outputs

        else:
            raise Exception(f"unknown opcode [{opcode}]")

        instruction_pointer += instruction_pointer_shift
