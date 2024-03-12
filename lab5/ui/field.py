import math
import random
from pprint import pprint

import pygame
import time

import pygame_gui

from config import UIConfig
from utils import forced_ups, coords_from_num
from cells import Cell, Bot, Food, Wall
from saveload import save_to, load_from


class Field:
    def __init__(self):
        pygame.init()

        self.canvas = pygame.display.set_mode((
            UIConfig.Window.width,
            UIConfig.Window.height
        ))

        self.i = 0
        self.grid: list[list[Cell]] = []
        self.bots = []
        self.ui_manager = pygame_gui.UIManager((UIConfig.Window.width, UIConfig.Window.height))
        self.clock = pygame.time.Clock()

        self.iteration = 0
        self.food_consumed = 0
        self.max_food_consumed = 0
        self.food_consumed_sum = 0
        self.food_consumed_average = 0

        # Create a text field
        text_rect = pygame.Rect(10, 795, 400, 80)
        self.text_label = pygame_gui.elements.UITextBox(relative_rect=text_rect,
                                                      manager=self.ui_manager,
                                                      html_text="<p>Aboba</p>")

        pygame.display.set_caption('Genetics')

    @forced_ups(UIConfig.UPS)
    def update(self):

        if len(self.bots) > UIConfig.run_until_alive and self.grid != []:
            self.update_cells()
        else:
            self.fill_grid()

        return self._redraw()

    def _redraw(self):

        if self.iteration % UIConfig.redraw_every_iteration == 0:
            self.canvas.fill('#000000')
            time_delta = self.clock.tick(60) / 1000.0
            self.ui_manager.draw_ui(self.canvas)

            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    cell = self.grid[i][j]
                    y = (UIConfig.Cell.height + UIConfig.Cell.gap) * i
                    x = (UIConfig.Cell.width + UIConfig.Cell.gap) * j

                    pygame.draw.rect(self.canvas, cell.color, (x, y, UIConfig.Cell.width, UIConfig.Cell.height))

            self.text_label.set_text(f'<p>iteration: {self.iteration} food_consumed: {self.food_consumed}</p>'
                                     f'<p>max food consumed: {self.max_food_consumed} UPS: {UIConfig.UPS}</p>')

            self.ui_manager.update(time_delta)
            pygame.display.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('quit')
                return True
            self.ui_manager.process_events(event)



    def update_cells(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if isinstance(self.grid[i][j], Bot) and len(self.bots) > UIConfig.run_until_alive:
                    bot: Bot = self.grid[i][j]
                    res = bot.update(self.grid, i, j, self)
                    if res in self.bots:
                        index = self.bots.index(res)
                        del self.bots[index]

    def fill_grid(self):
        self.food_consumed_sum += self.food_consumed

        if self.iteration % (UIConfig.redraw_every_iteration) == 0:
            self.food_consumed_average = self.food_consumed_sum / (UIConfig.redraw_every_iteration)
            self.food_consumed_sum = 0
            print(f"{self.iteration=}, {self.max_food_consumed=} {self.food_consumed_average=:.2f}")

        self.iteration += 1

        if self.food_consumed > self.max_food_consumed:
            self.max_food_consumed = self.food_consumed
        self.food_consumed = 0

        bots = self.get_bots_population()

        self.bots = []
        self.grid = []
        height_cells_count = math.floor(
            UIConfig.Window.height / (UIConfig.Cell.height + UIConfig.Cell.gap) * UIConfig.Window.field_height)
        width_cells_count = math.floor(
            UIConfig.Window.width / (UIConfig.Cell.width + UIConfig.Cell.gap) * UIConfig.Window.field_width)

        for i in range(height_cells_count):
            row = []
            for j in range(width_cells_count):
                if i == 0 or i == height_cells_count - 1:
                    row.append(Wall())
                elif j == 0 or j == width_cells_count - 1:
                    row.append(Wall())
                else:
                    cell = random.choices([Wall(), Food(), Cell()], [10, 20, 200], k=1)[0]
                    row.append(cell)
            self.grid.append(row)

        for el in bots:
            x, y = 2, 2

            while type(self.grid[y][x]) != Cell:
                x = random.randint(1, width_cells_count - 1)
                y = random.randint(1, height_cells_count - 1)

            self.grid[y][x] = el
            self.bots.append(el)


    def get_bots_population(self):
        current_bots = [*self.bots]

        if not current_bots:
            for i in range(UIConfig.population_amount):
                current_bots.append(
                    Bot([random.randint(0, 63) for i in range(64)])
                )
            return current_bots
        else:
            mutated = [
                current_bots.pop(random.randint(0, len(current_bots) - 1))
                for _ in range(UIConfig.mutate_amount)
            ]
            for el in mutated:
                # print("before", el.genome)
                el.genome[random.randint(0, 0)] = random.randint(0, 63)
                # print("after ", el.genome)

            bots = [*current_bots, *mutated]

            res = []
            for i in range(UIConfig.population_amount):
                bot = bots[i % len(bots)]
                new_bot = Bot([*bot.genome], bot in mutated)
                # new_bot.num = bots[i % len(bots)].num
                # new_bot.current_command = bots[i % len(bots)].current_command
                res.append(new_bot)

            # print(set(tuple(el.genome) for el in res))
            return res

    def spawn_food(self):
        x, y = 0, 0

        while type(self.grid[y][x]) != Cell:
            x = random.randint(1, len(self.grid[y]) - 1)
            y = random.randint(1, len(self.grid) - 1)

        self.grid[y][x] = Food()


if __name__ == "__main__":
    field = Field()
    try:
        data = load_from('backups/bots6.pickle')
        field.bots = [*data['bots']]
        field.iteration = data['iteration']
        field.max_food_consumed = data['max_food_consumed']

        print('Bots have been loaded')
    except TypeError:
        field.bots = load_from('backups/bots.pickle')
    except Exception as ex:
        print(ex)

    print(len({tuple(el.genome) for el in field.bots}))

    while not field.update():
        # print(len(field.bots))
        ...

    backup_name = f"backups/bots6.pickle"
    print(f'{backup_name=}')
    save_to(backup_name, {
        "bots": field.bots,
        "iteration": field.iteration,
        "max_food_consumed": field.max_food_consumed,
    })

    print(len(field.bots))
    print(len({tuple(el.genome) for el in field.bots}))



