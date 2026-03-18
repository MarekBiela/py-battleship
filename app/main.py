class Deck:
    def __init__(self, is_alive: bool = True) -> None:
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        coordinates = {}
        if start[0] == end[0]:
            for i in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                coordinates[(start[0], i)] = Deck()
        if start[1] == end[1]:
            for i in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                coordinates[(i, start[1])] = Deck()
        self.coordinates = coordinates
        self.is_drowned = is_drowned

    def fire(self, row: int, column: int) -> None:
        self.coordinates[(row, column)].is_alive = False
        if all(deck.is_alive is False for deck in self.coordinates.values()):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        field_dict = {}
        ship_dict = {}
        for i in range(len(ships)):
            ship_dict[i] = Ship(ships[i][0], ships[i][1])
            for coordinates in ship_dict[i].coordinates:
                field_dict[coordinates] = ship_dict[i]
        self._validate_field(ship_dict, field_dict)
        self.field = field_dict

    def fire(self, location: tuple) -> str:
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    if (
                        self.field[(row, column)]
                        .coordinates[(row, column)]
                        .is_alive
                    ):
                        character = u"\u25A1"
                    elif self.field[(row, column)].is_drowned:
                        character = "x"
                    else:
                        character = "*"
                else:
                    character = "~"
                print(character, end="   ")
            print()

    def _validate_field(self, ship_dict: dict, field_dict: dict) -> None:
        if len(ship_dict) != 10:
            raise ValueError()
        count_dict = {}
        for ship in ship_dict.values():
            count_dict[len(ship.coordinates)] = (
                count_dict.get(len(ship.coordinates), 0) + 1
            )
        if any(
                [count_dict.get(1, 0) != 4,
                 count_dict.get(2, 0) != 3,
                 count_dict.get(3, 0) != 2,
                 count_dict.get(4, 0) != 1]
        ):
            raise ValueError()
        for ship in ship_dict.values():
            for coordinates in ship.coordinates:
                points_around = [
                    (coordinates[0] + 1, coordinates[1]),
                    (coordinates[0] - 1, coordinates[1]),
                    (coordinates[0] + 1, coordinates[1] + 1),
                    (coordinates[0] - 1, coordinates[1] + 1),
                    (coordinates[0] + 1, coordinates[1] - 1),
                    (coordinates[0] - 1, coordinates[1] - 1),
                    (coordinates[0], coordinates[1] + 1),
                    (coordinates[0], coordinates[1] - 1)
                ]
                for point in points_around:
                    if point in field_dict and point not in ship.coordinates:
                        raise ValueError
