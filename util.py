from typing import List


def intcode(data: List[int]) -> int:
    """
    >>> intcode([1,0,0,0,99])
    2

    >>> intcode([2,3,0,3,99])
    2

    >>> intcode([2,2,2,0,99])
    4

    >>> intcode([2,4,4,5,99,0])
    2

    >>> intcode([1,1,1,4,99,5,6,0,99])
    30
    """

    instruction_pointer = 0

    while data[instruction_pointer] != 99:

        if data[instruction_pointer] == 1:

            from_1 = data[instruction_pointer + 1]
            from_2 = data[instruction_pointer + 2]
            target = data[instruction_pointer + 3]
            data[target] = data[from_1] + data[from_2]

        elif data[instruction_pointer] == 2:
            from_1 = data[instruction_pointer + 1]
            from_2 = data[instruction_pointer + 2]
            target = data[instruction_pointer + 3]
            data[target] = data[from_1] * data[from_2]

        else:
            print(f"unknown opcode [{data[instruction_pointer]}], "
                  f"instruction pointer at [{instruction_pointer}]")

        instruction_pointer += 4
    return data[0]
