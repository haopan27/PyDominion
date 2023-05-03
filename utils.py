import random
import card_info as ci


def print_colored(text_to_print, desired_color="red", new_line=True):
    if desired_color == "green":
        print("\033[92m{}\033[00m".format(text_to_print), end="\n" if new_line else "")
    elif desired_color == "yellow":
        print("\033[93m{}\033[00m".format(text_to_print), end="\n" if new_line else "")
    elif desired_color == "purple":
        print("\033[95m{}\033[00m".format(text_to_print), end="\n" if new_line else "")
    elif desired_color == "cyan":
        print("\033[96m{}\033[00m".format(text_to_print), end="\n" if new_line else "")
    else:
        print("\033[91m{}\033[00m" .format(text_to_print), end="\n" if new_line else "")


def draw_cards(cards_to_draw, cards_in_hand, cards_discarded, cur_player, n_to_draw=5, keep_cur_hand=False):
    n_draw_pile = len(cards_to_draw[cur_player])
    if n_draw_pile >= n_to_draw:
        if keep_cur_hand:
            cards_in_hand[cur_player] += cards_to_draw[cur_player][:n_to_draw]
        else:
            cards_in_hand[cur_player] = cards_to_draw[cur_player][:n_to_draw]
        cards_to_draw[cur_player][:n_to_draw] = []
    else:
        if keep_cur_hand:
            cards_in_hand[cur_player] += cards_to_draw[cur_player]
        else:
            cards_in_hand[cur_player] = cards_to_draw[cur_player]
        cards_to_draw[cur_player] = []
        random.shuffle(cards_discarded[cur_player])
        cards_to_draw[cur_player] = cards_discarded[cur_player]
        cards_discarded[cur_player] = []
        cards_in_hand[cur_player] += cards_to_draw[cur_player][:n_to_draw - n_draw_pile]
        cards_to_draw[cur_player][:n_to_draw - n_draw_pile] = []


def get_desired_item(available_coins):
    if 3 <= available_coins < 6:
        return "Silver"
    elif 6 <= available_coins < 8:
        return "Gold"
    elif available_coins >= 8:
        return "Province"
    return "None"


def get_opp_player(cur_player):
    return 1 if cur_player == 2 else 2


def resolve_action(cards_to_draw, cards_in_hand, cards_discarded, cur_player, opp_player,
                   desired_action, piles_on_board, victory_points):
    if desired_action == "Smithy":
        draw_cards(cards_to_draw, cards_in_hand, cards_discarded, cur_player, 3, True)  # append cards to current hand
    elif desired_action == "Chapel":
        num_trash = 4
        while num_trash > 0:
            card_to_trash = input("Trash a card from your hand: {} x ".format(", ".join(cards_in_hand[cur_player])))
            if card_to_trash not in cards_in_hand[cur_player]:
                break

            if card_to_trash in ci.vps:
                victory_points[cur_player - 1] -= ci.vps[card_to_trash]

            cards_in_hand[cur_player].remove(card_to_trash)
            num_trash -= 1
    elif desired_action == "Witch":
        draw_cards(cards_to_draw, cards_in_hand, cards_discarded, cur_player, 2, True)
        if piles_on_board["Curse"] > 0:
            cards_discarded[opp_player] += ["Curse"]
            victory_points[opp_player - 1] -= 1
            piles_on_board["Curse"] -= 1
