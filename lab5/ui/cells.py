from lab5.ui.config import UIConfig
from lab5.ui.utils import coords_from_num


class Cell:
    color = '#101010'
    added_command = 4


class Bot(Cell):
    normal_color = "#2b31a6"
    mutated_color = '#eb8934'
    iteration_hp_lost = 1
    added_command = 1
    last_number = 0

    def __init__(self, genome, is_mutated=False):
        Bot.last_number += 1
        self.num = Bot.last_number
        self.color = self.mutated_color if is_mutated else self.normal_color
        self.health = 25
        self.genome = genome
        self._current_command = 0
        self._angle = 0

    def __repr__(self):
        return str(self.num)

    def __str__(self):
        return str(self.num)

    @property
    def current_command(self):
        return self._current_command

    @current_command.setter
    def current_command(self, value):
        self._current_command = value % 64

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value % 8

    def update(self, grid: list, i: int, j: int, field,  recursive_step=0):
        if recursive_step > UIConfig.max_recursive:
            # print("recursive block")
            return
        #
        # if recursive_step == 0:
        #     print(f'[Bot {self.num}] begin')
        #
        # print(f'step: {recursive_step}', end='   ')

        command = self.genome[self.current_command]

        x, y = coords_from_num((command + self.angle) % 8)
        cell = grid[i + x][j + y]

        if command < 8:  # Moving
            if isinstance(cell, Bot):
                self.current_command += Bot.added_command

            elif isinstance(cell, Food):
                self.health += cell.added_food
                grid[i + x][j + y] = self
                grid[i][j] = Cell()
                self.current_command += Food.added_command
                field.food_consumed += Food.added_food
                field.spawn_food()
                # print(f'move to [{x}, {y}]')

            elif isinstance(cell, Wall):
                self.current_command += Wall.added_command

            elif isinstance(cell, Cell):
                grid[i + x][j + y] = self
                grid[i][j] = Cell()
                self.current_command += Cell.added_command
                # print(f'move to [{x}, {y}]')


        elif command < 16:  # Looking
            self.current_command += cell.added_command
            # print(f'look to [{x}, {y}]')
            self.update(grid, i, j, field, recursive_step+1)

        elif command < 24:  # PickUp
            if isinstance(cell, Food):
                self.health += cell.added_food
                field.food_consumed += Food.added_food
                grid[i + x][j + y] = Cell()
                field.spawn_food()
                # print(f'pick up from [{x}, {y}]')

            self.current_command += cell.added_command

        elif command < 32:
            self.angle = self.angle + command % 8
            self.current_command += 1
            # print(f'turn by {(command % 8) * 45} degrees')
            self.update(grid, i, j, field, recursive_step + 1)

        else:               # Genome moving
            # print(f'go from {self.current_command} to {(self.current_command + command) % 64}')
            self.current_command = self.current_command + command
            self.update(grid, i, j, field, recursive_step + 1)


        if recursive_step == 0:
            self.health -= self.iteration_hp_lost
            if self.health < 0:
                grid[i][j] = Cell()
                return self


class Food(Cell):
    color = "#2da62b"
    added_command = 3
    added_food = 35


class Wall(Cell):
    added_command = 1
    color = "#505050"
