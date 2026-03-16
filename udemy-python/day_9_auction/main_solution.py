"""
SECRET AUCTION PROJECT (Day 9 – Dictionaries)
Solution version.
"""

import os


def clear_screen() -> None:
    """Clear the terminal so the next bidder cannot see previous bids."""
    os.system("cls" if os.name == "nt" else "clear")


def find_highest_bidder(bidding_dictionary: dict[str, int]) -> None:
    """
    Loop through all bidders, find the highest bid, and print the winner.
    """
    highest_bid = 0
    winner = ""

    for bidder_name, bid_amount in bidding_dictionary.items():
        if bid_amount > highest_bid:
            highest_bid = bid_amount
            winner = bidder_name

    print(f"The winner is {winner} with a bid of ${highest_bid}")


def secret_auction() -> None:
    print("Welcome to the secret auction program.")

    all_bids: dict[str, int] = {}
    bidding_finished = False

    while not bidding_finished:
        name = input("What is your name?: ")
        bid = int(input("What is your bid?: $"))
        all_bids[name] = bid

        should_continue = input(
            "Are there any other bidders? Type 'yes' or 'no': "
        ).strip().lower()

        if should_continue == "no":
            bidding_finished = True
            find_highest_bidder(all_bids)
        else:
            clear_screen()


if __name__ == "__main__":
    secret_auction()
