'''
    Author: Angel Davila
    Github: https://github.com/adavila0703
    University: Southern New Hampshire University
    Date: 2/12/2022
    Build time: 5 hours
'''

from enum import Enum
import os
import random
from time import sleep


class Items(Enum):
    # health potion which gives you 25 hp
    HEALTH_POTION = 1
    # increase damage for one round
    INCREASE_DAMAGE = 2
    # allows you to take no damage for one round
    UNTOUCHABLE = 3
    # gives you 3 hit combo
    THREE_HIT_COMBO = 4


class Rooms(Enum):
    """Enums representing the ares which you can travel"""
    CENTRAL_WING = 1
    NORTH_WING = 2
    WEST_WING = 3
    SOUTH_WING = 4
    EAST_WING = 5
    SOUTH_EAST_WING = 6
    NORTH_EAST_WING = 7
    DUNGEON = 8


class Const:
    """Constants to avoid so many magic numbers in the code base"""
    CANCEL_ITEM_USE = 99
    MINIMUM_HIT_POINTS = 25
    MAXIMUM_HIT_POINTS = 50
    KING_STARTING_HEALTH = 10000

    # player specific
    PLAYER_MIN_HEALTH_INCREASE = 80
    PLAYER_MAX_HEALTH_INCREASE = 120
    PLAYER_POTION_BASE = 100
    PLAYER_MIN_DAMAGE_ADDER = 25
    PLAYER_MAX_DAMAGE_ADDER = 250
    PLAYER_FINAL_HEALTH_INCREASE = 1500
    PLAYER_STARTING_HEALTH = 100
    PLAYER_STARTING_ITEMS_AMOUNT = 1
    PLAYER_NUMBER_OF_ITEMS_DROPPED = [2, 2, 3, 3, 5, 5, 7]

    # demon specific
    DEMON_MIN_HEALTH_INCREASE = 100
    DEMON_MAX_HEALTH_INCREASE = 200
    DEMON_STARTING_HEALTH = 100

    MAIN_GAME_TITLE = '''
 @@@@@@@  @@@@@@@@ @@@@@@@@@@   @@@@@@  @@@  @@@       @@@@@@ @@@       @@@@@@  @@@ @@@ @@@@@@@@ @@@@@@@ 
 @@!  @@@ @@!      @@! @@! @@! @@!  @@@ @@!@!@@@      !@@     @@!      @@!  @@@ @@! !@@ @@!      @@!  @@@
 @!@  !@! @!!!:!   @!! !!@ @!@ @!@  !@! @!@@!!@!       !@@!!  @!!      @!@!@!@!  !@!@!  @!!!:!   @!@!!@! 
 !!:  !!! !!:      !!:     !!: !!:  !!! !!:  !!!          !:! !!:      !!:  !!!   !!:   !!:      !!: :!! 
 :: :  :  : :: :::  :      :    : :. :  ::    :       ::.: :  : ::.: :  :   : :   .:    : :: :::  :   : :

Welcome to Demon Slayer!

Here are a few items to get you started, good luck!

'''


class Errors:
    VALUE_ERROR = 'Input must be a number or within a range of numbers that have been listed'

    def log_error(runtime_error: str, display_error: str) -> None:
        print(f'Error {runtime_error} - {display_error}')


class GameState:
    """Game State class which hold some game stat data"""

    def __init__(self) -> None:
        self.level = 1

    def level_up(self, level):
        self.level += level
        return None

    def get_level(self):
        return self.level


class Player:
    """Player class"""

    def __init__(self, name: str, position: int) -> None:
        self.name: str = name
        self.position: int = position
        self.health: int = Const.PLAYER_STARTING_HEALTH
        self.items: list = []
        self.damage_adder: int = 0
        self.damage_adder_bool: bool = False
        self.untouchable: bool = False
        self.level = 1
        self.three_hit_combo = False

    def __repr__(self) -> str:
        return self.name

    def raise_level(self, game_state: GameState) -> None:
        self.level = game_state.level
        return

    def get_health(self) -> int:
        return self.health

    def get_name(self) -> str:
        return self.name

    def increase_health(self, amount) -> None:
        self.health += amount
        return

    def decrease_health(self, amount) -> None:
        self.health -= amount
        return

    def get_number_of_items(self) -> int:
        return len(self.items)

    def item_drop(self, amount=1) -> None:
        """Drops a random item, default is set to 1"""
        for _ in range(0, amount):
            item_number = random.randint(1, 4)
            item = Items(item_number)
            self.items.append(item)
            print(f'\nYou received item: {self.get_item_details(item)}\n')
        return

    def get_item_details(self, item) -> str:
        """Get details of a specific item"""
        # TODO: Could move this out of the player and store it in an item class
        if item == Items.HEALTH_POTION:
            return f'Health Potion - Use this to increase your health by {Const.PLAYER_POTION_BASE * self.level}'
        elif item == Items.INCREASE_DAMAGE:
            return 'Increase Damage - Use this to amplify your damage'
        elif item == Items.UNTOUCHABLE:
            return 'Untouchable - Used this to receive 0 damage from your opponent'
        elif item == Items.THREE_HIT_COMBO:
            return 'Three Hit Combo - Used this to hit your opponent with a three hit combo!'

    def display_all_items(self) -> str:
        """Outputs all existing items listed in self.items"""
        for index, item in enumerate(self.items):
            print(f'{index} - {self.get_item_details(item)}')
        print('99 - Cancel use item')

    def get_item_number(self) -> int:
        """Returns the index number of the item to be used"""
        while True:
            try:
                item = int(input('\nSelect an item\n:'))

                if cancel := Const.CANCEL_ITEM_USE == item:
                    return cancel

                if item in range(0, len(self.items)):
                    return item

                print('Did you choose the right number?')
            except ValueError as VALUE_ERROR:
                Errors.log_error(VALUE_ERROR, Errors.VALUE_ERROR)

    def attack_or_items(self) -> None:
        """Menu to handle if you want to continue with an attack or use an item"""
        # TODO: This should probably only handle the use of an item
        # Should move the menu handling to a common function
        try:
            user_input = int(
                input('Would you like to:\n1. Attack\n2. Use item\n:'))

            if user_input == 1:
                return True

            if len(self.items) == 0:
                print('\nYou dont have any items yet, kill a demon!\n')
                return False

            self.display_all_items()

            item = self.get_item_number()

            if item == Const.CANCEL_ITEM_USE:
                return False

            self.player_item_use(self.items[item])
            self.items.pop(item)
            return True
        except ValueError as VALUE_ERROR:
            Errors.log_error(VALUE_ERROR, Errors.VALUE_ERROR)

    def player_item_use(self, item: Items):
        """Handles the use of an item"""
        if item == Items.HEALTH_POTION:
            potion_amount = Const.PLAYER_POTION_BASE * self.level
            self.increase_health(potion_amount)
            print(
                f'You have been giving {potion_amount} health.\nYour health is now {self.get_health()}\n')
        elif item == Items.INCREASE_DAMAGE:
            self.damage_adder = random.randint(
                Const.PLAYER_MIN_DAMAGE_ADDER, Const.PLAYER_MAX_DAMAGE_ADDER) * self.level
            self.damage_adder_bool = True
            print('Increase damage for one round')
        elif item == Items.UNTOUCHABLE:
            self.untouchable = True
            print('Untouchable for one round')
        elif item == Items.THREE_HIT_COMBO:
            self.three_hit_combo = True
            print('Untouchable for one round')

    def round_item_use(self, type: Items):
        """During the round we check if any of the items have to be applied"""
        if type == Items.INCREASE_DAMAGE:
            if self.damage_adder_bool:
                self.damage_adder_bool = False
                return self.damage_adder
            return 0
        elif type == Items.UNTOUCHABLE:
            if self.untouchable:
                self.untouchable = False
                return True
            return False
        elif type == Items.THREE_HIT_COMBO:
            if self.three_hit_combo:
                self.three_hit_combo = False
                return 3
            return 1

    def random_health_increase(self, level) -> None:
        """Applies a random health to the player"""
        health = random.randint(
            Const.PLAYER_MIN_HEALTH_INCREASE, Const.PLAYER_MAX_HEALTH_INCREASE) * level
        print(f'\nHealth increase by {health + 100}')
        self.increase_health(health)
        return


class Demon:
    """Class for demon"""

    def __init__(self) -> None:
        self.name = 'Demon'
        self.health = Const.DEMON_STARTING_HEALTH

    def get_name(self) -> str:
        return self.name

    def get_health(self) -> int:
        return self.health

    def increase_health(self, amount) -> None:
        self.health += amount
        return

    def decrease_health(self, amount) -> None:
        self.health -= amount
        return


class King:
    """Class for the King"""

    def __init__(self) -> None:
        self.name = 'King'
        self.health = Const.KING_STARTING_HEALTH

    def get_name(self) -> str:
        return self.name

    def get_health(self) -> int:
        return self.health

    def increase_health(self, amount) -> None:
        self.health += amount
        return

    def decrease_health(self, amount) -> None:
        self.health -= amount
        return


def player_attack(player: Player, villain: object, level: int, num_of_hits: int) -> None:
    for num in range(0, num_of_hits):
        critical_strike = [0, 0, random.randint(
            1, 5) * level, random.randint(5, 10) * level]
        hit = random.randint(Const.MINIMUM_HIT_POINTS *
                             level, Const.MAXIMUM_HIT_POINTS * level)

        # damage increase shouldn't be able to be used if three hit combo is also being used
        damage_increase = player.round_item_use(Items.INCREASE_DAMAGE)
        hit += damage_increase
        hit += critical_strike[num]

        print(level)

        print(
            f'\n{player.get_name()} is attacking the {villain.get_name()} for {hit}\n')
        villain.decrease_health(hit)


def villain_attack(player: Player, villain: object, level: int) -> None:
    hit = random.randint(Const.MINIMUM_HIT_POINTS *
                         level, Const.MAXIMUM_HIT_POINTS * level)

    untouchable = player.round_item_use(Items.UNTOUCHABLE)

    if untouchable:
        hit = 0

    print(f'\n{villain.get_name()} is attacking the {player.get_name()} for {hit}\n')
    player.decrease_health(hit)


def initiate_fight_loop(villain: object, player: Player, game_state: GameState) -> None:
    """This is the main fighting loop"""
    # TODO: This could use a refactor
    while True:
        os.system('cls')
        level = game_state.get_level()
        print(
            f'\n{player.get_name()} Health: {player.get_health()}\n{villain.get_name()} Health: {villain.get_health()}\n')

        if player.get_number_of_items() > 0:
            # may not have to return a message if there are no items to be used since we wont have to use the menu if the length is 0
            move = player.attack_or_items()

            if not move:
                sleep(2)
                continue

        combo = player.round_item_use(Items.THREE_HIT_COMBO)

        player_attack(player, villain, game_state.level, combo)

        if villain.health <= 0:
            if villain.name == 'King':
                print('You won the game! Congrats!')
                exit()
            print(f'\nYou won the fight!\n')

            player.increase_health(150)
            player.random_health_increase(level)
            game_level_up(game_state, player)

            # drops increase by the game state level
            player.item_drop(
                Const.PLAYER_NUMBER_OF_ITEMS_DROPPED[game_state.level])
            return

        villain_attack(player, villain, game_state.level)

        if player.get_health() <= 0:
            print('You died...')
            exit()

        # game state level increases by 5 each round of attack or item use when facing the King
        if villain.get_name() == 'King':
            game_level_up(game_state, player, 5)

        sleep(2)


def get_room(room: Rooms) -> str:
    """Returns the room name in string format"""
    if room == Rooms.CENTRAL_WING:
        return 'Central Wing'
    elif room == Rooms.NORTH_WING:
        return 'North Wing'
    elif room == Rooms.WEST_WING:
        return 'West Wing'
    elif room == Rooms.SOUTH_WING:
        return 'South Wing'
    elif room == Rooms.EAST_WING:
        return 'East Wing'
    elif room == Rooms.SOUTH_EAST_WING:
        return 'South East Wing'
    elif room == Rooms.NORTH_EAST_WING:
        return 'North East Wing'
    elif room == Rooms.DUNGEON:
        return 'Dungeon'


def display_room_possibilities(current_room: Rooms, *args):
    """Output room possibilities from the incoming tuple"""
    print(f'\nYou are in {get_room(current_room)}, and can move to:\n')
    for room in args[0]:
        print(f'{room.value}: {get_room(room)}')


def possible_room_locations(player: Player) -> Rooms:
    """Returns all possible room locations you can move to depending on which room you are currently in"""
    new_room = None
    room_possibilities = None

    if player.position == Rooms.CENTRAL_WING:
        room_possibilities = [Rooms.CENTRAL_WING, Rooms.NORTH_WING, Rooms.WEST_WING,
                              Rooms.SOUTH_WING, Rooms.EAST_WING]
    elif player.position == Rooms.NORTH_WING:
        room_possibilities = [Rooms.DUNGEON, Rooms.CENTRAL_WING]
    elif player.position == Rooms.WEST_WING:
        room_possibilities = [Rooms.CENTRAL_WING]
    elif player.position == Rooms.SOUTH_WING:
        room_possibilities = [Rooms.CENTRAL_WING, Rooms.SOUTH_EAST_WING]
    elif player.position == Rooms.EAST_WING:
        room_possibilities = [Rooms.CENTRAL_WING, Rooms.NORTH_EAST_WING]
    elif player.position == Rooms.NORTH_EAST_WING:
        room_possibilities = [Rooms.EAST_WING]
    elif player.position == Rooms.SOUTH_EAST_WING:
        room_possibilities = [Rooms.SOUTH_WING]
    elif player.position == Rooms.DUNGEON:
        room_possibilities = [Rooms.NORTH_WING]

    display_room_possibilities(player.position, room_possibilities)
    new_room = movement(room_possibilities)

    player.position = new_room
    return new_room


def movement(*args) -> Rooms:
    """Handles movement between rooms"""
    while True:
        try:
            room = Rooms(int(input("\nChoose a room: ")))
            if room not in args[0]:
                print('\nRoom not available try again...\n')
                continue
            return room

        except ValueError as VALUE_ERROR:
            Errors.log_error(VALUE_ERROR, Errors.VALUE_ERROR)


def check_if_demon_is_alive(demons: dict, player_position: Rooms) -> bool:
    """Run a check to see if there are any demons still alive"""
    for demon in demons:
        demon_room = Rooms(int(demon))
        demon_object: Demon = demons[demon]
        if demon_room == player_position and demon_object.health >= 100:
            return True, demon_object

    if player_position != Rooms.DUNGEON:
        print(f'\nYou killed the demon in {get_room(player_position)}\n')

    return False, None


def demons_get_stronger(demons: dict, level: int) -> None:
    """Search for demons who are still alive and increase their health"""
    health = random.randint(Const.DEMON_MIN_HEALTH_INCREASE,
                            Const.DEMON_MAX_HEALTH_INCREASE) * level
    for demon in demons:
        obj = demons[demon]
        if obj.health > 0:
            obj.health += health
    print(f'Demons grow stronger! Living demons gained {health} health')
    return


def king_caution(check) -> bool:
    """Logic to check if you want to face the king before killing the rest of the demons"""
    # behavior to ignore this logic if all the demons have been killed
    if not check:
        return True

    while True:
        answer = input(
            '\nYou have not killed all the demons, are you sure you want to enter the Dungeon and face the king? (y or n)\n:')

        if answer == 'y':
            print('Okay good luck!')
            return True

        if answer == 'n':
            print('Probably a good idea...')
            return False

        print('Not a valid answer, try again...')
        continue


def game_level_up(game_state: GameState, player: Player, level=1) -> None:
    """Raises the game state level"""
    # TODO: there is some duplication here, we could probably store a single level in the game state and inherit
    game_state.level_up(level)
    player.raise_level(game_state)


def main():
    """Main game loop"""
    player = Player('Angel', Rooms.CENTRAL_WING)
    demons = {
        '1': Demon(),
        '2': Demon(),
        '3': Demon(),
        '4': Demon(),
        '5': Demon(),
        '6': Demon(),
        '7': Demon(),
    }
    king = King()
    game_state = GameState()

    print(Const.MAIN_GAME_TITLE)

    player.item_drop(Const.PLAYER_NUMBER_OF_ITEMS_DROPPED[game_state.level])

    print('Loading game...')
    sleep(7)

    # first go before entering the main loop
    check, demon = check_if_demon_is_alive(demons, player.position)
    if check:
        initiate_fight_loop(demon, player, game_state)
        demons_get_stronger(demons, game_state.level)

    # games main loop
    while True:
        player_position = possible_room_locations(player)

        check, demon = check_if_demon_is_alive(demons, player_position)
        if check:
            initiate_fight_loop(demon, player, game_state)
            demons_get_stronger(demons, game_state.level)

        elif player_position == Rooms.DUNGEON:
            if king_caution(check):
                player.increase_health(Const.PLAYER_FINAL_HEALTH_INCREASE)
                initiate_fight_loop(king, player, game_state)
            player.position = Rooms.NORTH_WING


if __name__ == '__main__':
    main()
