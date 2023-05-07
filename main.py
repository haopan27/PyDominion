import random
import card_info as ci
import utils


game_end = False
human_resigned = False
victory_points = [3, 3]  # each player starts with 3 estates
adjusted_victory_points = victory_points
gardens_owned = [0, 0]
cards_owned = [10, 10]
turns = 1
cur_player = 1
piles_on_board = ci.basic_cards
piles_on_board.update(random.sample(ci.action_cards.items(), 2))  # add action cards
# piles_on_board.update(ci.special_cards)  # append items in special_cards

starting_hand = {
    1: [],
    2: []
}
for _ in range(7):
    starting_hand[1] += ["Copper"]
    starting_hand[2] += ["Copper"]
for _ in range(3):
    starting_hand[1] += ['Estate']
    starting_hand[2] += ['Estate']

random.shuffle(starting_hand[1])
random.shuffle(starting_hand[2])
cards_in_hand = {
    1: starting_hand[1][:5],
    2: starting_hand[2][:5]
}
cards_discarded = {
    1: [],
    2: []
}
cards_to_draw = {
    1: starting_hand[1][5:],
    2: starting_hand[2][5:]
}

human_starts = True if random.randint(1, 100) < 50 else False
player1_name, player2_name = "", ""
if human_starts:
    player1_name, player2_name = "Human player", "Computer player"
    print("The starting player is Human")
else:
    player1_name, player2_name = "Computer player", "Human player"
    print("The starting player is Computer")
print("................................")

while not game_end:
    cur_player_name = "Human player" if cur_player == 1 and human_starts or cur_player == 2 and not human_starts \
        else "Computer player"

    # Action phase
    num_actions = 0
    num_buys = 1  # certain action cards modify num_buys
    available_coins = 0  # certain action cards modify available_coins

    performed_actions = []  # store used action cards which will get transferred to the discard pile later
    available_actions = []
    for c in cards_in_hand[cur_player]:
        if c in ci.action_cards:
            if num_actions == 0:
                num_actions = 1
            available_actions += [c]

    opp_player = utils.get_opp_player(cur_player)
    while num_actions > 0 and len(available_actions):
        desired_action = "None"
        if cur_player_name == "Human player":
            print("Action phase || your hand: {}".format(", ".join(cards_in_hand[cur_player])))
            utils.print_colored("Available action(s): {}".format(", ".join(available_actions)), "cyan")
            desired_action = input(
                "You have {} action(s), "
                "please input the next action you wish to perform: ".format(num_actions))

            if desired_action == "Resign":
                game_end, human_resigned = True, True
                break
        else:
            pass

        if desired_action == "None" or desired_action not in piles_on_board\
                or desired_action not in cards_in_hand[cur_player] \
                or desired_action not in available_actions:
            break
        else:
            available_actions.remove(desired_action)
            cards_in_hand[cur_player].remove(desired_action)
            num_actions -= 1
            performed_actions += [desired_action]
            utils.print_colored("{} played {}".format(cur_player_name, desired_action))

            # resolve action
            if desired_action == "Chapel":
                num_trash = 4
                while num_trash > 0:
                    card_to_trash = input(
                        "Trash a card from your hand: {} x ".format(", ".join(cards_in_hand[cur_player])))
                    if card_to_trash not in cards_in_hand[cur_player]:
                        break

                    if card_to_trash in ci.vps:
                        victory_points[cur_player - 1] -= ci.vps[card_to_trash]

                    if card_to_trash == "Gardens":
                        gardens_owned[cur_player - 1] -= 1

                    cards_owned[cur_player - 1] -= 1
                    cards_in_hand[cur_player].remove(card_to_trash)
                    num_trash -= 1
            elif desired_action == "Woodcutter":
                num_buys += 1
                available_coins += 2
            elif desired_action == "Village":
                num_actions += 2
                utils.draw_cards(cards_to_draw, cards_in_hand, cards_discarded, cur_player, 1, True)
            elif desired_action == "Smithy":
                utils.draw_cards(cards_to_draw, cards_in_hand, cards_discarded, cur_player, 3, True)
                # ^^draw and append cards to current hand
            elif desired_action == "Moneylender":
                if "Copper" in cards_in_hand[cur_player]:
                    trash_a_copper = input("Trash a copper from your hand?")
                    if trash_a_copper == "Yes":
                        cards_in_hand[cur_player].remove("Copper")
                        available_coins += 3
            elif desired_action == "Witch":
                utils.draw_cards(cards_to_draw, cards_in_hand, cards_discarded, cur_player, 2, True)
                if piles_on_board["Curse"] > 0:
                    cards_discarded[opp_player] += ["Curse"]
                    victory_points[opp_player - 1] -= 1
                    piles_on_board["Curse"] -= 1
            elif desired_action == "Laboratory":
                utils.draw_cards(cards_to_draw, cards_in_hand, cards_discarded, cur_player, 2, True)
                num_actions += 1
            elif desired_action == "Market":
                utils.draw_cards(cards_to_draw, cards_in_hand, cards_discarded, cur_player, 1, True)
                num_actions += 1
                num_buys += 1
                available_coins += 1
            elif desired_action == "Festival":
                num_actions += 2
                num_buys += 1
                available_coins += 2
            elif desired_action == "Sentry":
                num_actions += 1
                utils.draw_cards(cards_to_draw, cards_in_hand, cards_discarded, cur_player, 1, True)

                cards_to_look = []
                num_cards_to_draw = len(cards_to_draw[cur_player])
                if num_cards_to_draw < 2:
                    cards_to_look += cards_to_draw[cur_player]
                    random.shuffle(cards_discarded[cur_player])
                    cards_to_draw[cur_player] = cards_discarded[cur_player]
                    cards_discarded[cur_player] = []
                    cards_to_look += cards_to_draw[cur_player][:2 - num_cards_to_draw]
                else:
                    cards_to_look += cards_to_draw[cur_player][:2]

                cards_to_draw_rem_copy = cards_to_draw[cur_player][2:]

                num_trash = 2
                while num_trash > 0:
                    card_to_trash = input(
                        "Trash a card from top 2 of your deck: {} x ".format(", ".join(cards_to_look)))

                    if card_to_trash not in cards_to_look:
                        break

                    if card_to_trash in ci.vps:
                        victory_points[cur_player - 1] -= ci.vps[card_to_trash]

                    if card_to_trash == "Gardens":
                        gardens_owned[cur_player - 1] -= 1

                    cards_owned[cur_player - 1] -= 1
                    cards_to_look.remove(card_to_trash)
                    num_trash -= 1

                num_discard = len(cards_to_look)
                while num_discard > 0:
                    card_to_discard = input("Discard a card: {} x ".format(", ".join(cards_to_look)))

                    if num_discard == 2 and card_to_discard == "Both":
                        cards_discarded[cur_player] += cards_to_look
                        cards_to_look = []
                        num_discard -= 2
                        break

                    if card_to_discard not in cards_to_look:
                        break

                    cards_to_look.remove(card_to_discard)
                    cards_discarded[cur_player] += [card_to_discard]
                    num_discard -= 1

                if num_discard == 2:
                    do_swap = input("Would you like to swap the two cards {}(top, bottom)?".format(cards_to_look))
                    if do_swap:
                        cards_to_look = cards_to_look[::-1]

                # Put back cards onto the top of the deck
                cards_to_draw[cur_player] = cards_to_look + cards_to_draw_rem_copy

    if human_resigned:
        break

    # Buy phase
    desired_item = "None"

    for c in cards_in_hand[cur_player]:
        if c in ci.values:
            available_coins += ci.values[c]

    while num_buys > 0:
        if cur_player_name == "Human player":  # if this is human player
            print("Buy phase || your hand: {}".format(", ".join(cards_in_hand[cur_player])))
            utils.print_colored("Available items(quantity) | ", "cyan", False)
            for k, v in piles_on_board.items():
                utils.print_colored(k + "(" + str(v) + ") | ", "cyan", False)
            print()

            desired_item = input(
                "You have {} coins and {} buy(s), "
                "please input the next item you wish to buy: ".format(available_coins, num_buys))

            if desired_item == "Resign":
                game_end, human_resigned = True, True
                break
        else:  # if this is computer player
            desired_item = utils.get_desired_item(available_coins)

        if desired_item in piles_on_board and piles_on_board[desired_item] > 0\
                and available_coins >= ci.costs[desired_item]:
            # ^^make sure piles_on_board is a subset of ci.costs
            utils.print_colored(cur_player_name + " bought " + desired_item)

            available_coins -= ci.costs[desired_item]
            num_buys -= 1
            cards_discarded[cur_player] += [desired_item]
            if desired_item in ci.vps:
                victory_points[cur_player - 1] += ci.vps[desired_item]

            if desired_item == "Gardens":
                gardens_owned[cur_player - 1] += 1

            cards_owned[cur_player - 1] += 1
            piles_on_board[desired_item] -= 1
        else:
            break

    adjusted_victory_points = [victory_points[i] + cards_owned[i] // 10 * gardens_owned[i] for i in range(2)]

    print("After turn {}: {} (starting) has \033[92m\033[4m{}\033[0m VPs || {} has \033[92m\033[4m{}\033[0m VPs"
          .format(turns, player1_name, adjusted_victory_points[0], player2_name, adjusted_victory_points[1]))

    # check if game ends
    if piles_on_board["Province"] == 0:
        game_end = True
    else:
        empty_piles = 0
        for k, v in piles_on_board.items():
            if v == 0:
                empty_piles += 1

            if empty_piles >= 3:
                game_end = True
                break

    if game_end:
        break

    # cleaning up
    cards_discarded[cur_player] += cards_in_hand[cur_player]
    cards_discarded[cur_player] += performed_actions
    utils.draw_cards(cards_to_draw, cards_in_hand, cards_discarded, cur_player)

    # update board info
    cur_player = 2 if cur_player == 1 else 1
    turns += 1

# on game end:
if human_resigned:
    utils.print_colored("Human resigned")
else:
    winner = 0  # assumes tie

    max_vp = max(adjusted_victory_points)
    min_vp = min(adjusted_victory_points)
    if max_vp > min_vp:
        winner = adjusted_victory_points.index(max(adjusted_victory_points)) + 1
    elif max_vp == min_vp:
        if turns % 2 == 1 and cur_player == 1:
            winner = 2

    winner_name = "None"
    if winner == 1:
        winner_name = player1_name
    elif winner == 2:
        winner_name = player2_name
    utils.print_colored("The winner is: " + winner_name)
