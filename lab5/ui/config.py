from dataclasses import dataclass


@dataclass
class UIConfig:
    UPS = 5

    max_recursive = 20

    run_until_alive = 8
    mutate_amount = 2
    population_amount = 150
    redraw_every_iteration = 1
    @dataclass
    class Window:
        width: int = 1644
        height: int = 880
        field_width = 1
        field_height = .9

    @dataclass
    class Cell:
        width: int = 10
        height: int = 10
        gap: int = 2




