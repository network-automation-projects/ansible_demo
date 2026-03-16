"""
SECRET AUCTION PROJECT (Day 9 – Dictionaries)
Guided Prompts + Code Stubs

Use this file to complete the Secret Auction project
WITHOUT watching the solution video again.

Instructions:
- Read each step.
- Replace TODO items with real code.
- Run the program frequently while building it.
"""

# ============================================================
# STEP 1 — Create storage for bids
# ============================================================

"""
PROMPT
------
Create an empty dictionary called bids.

The dictionary should store:

name -> bid amount

Example structure when finished:

{
    "Alice": 150,
    "Bob": 200
}
"""

bids = {
}


# ============================================================
# STEP 2 — Function to determine the winner
# ============================================================

"""
PROMPT
------
Write a function called find_highest_bidder.

The function should:

1. Accept the bids dictionary as a parameter
2. Loop through all bidders
3. Track the highest bid
4. Track the winning bidder
5. Print the winner and their bid

Example final output:

The winner is Alice with a bid of $240
"""


def find_highest_bidder(bidding_dictionary):

    # TODO-2: create variable to track highest bid
    highest_bid = 0

    # TODO-3: create variable to track winner
    winner = ""

    # TODO-4: loop through dictionary
    for bid in bidding_dictionary:
        # TODO-5: get bid amount
        bid_amt = bid["amount"]
        # TODO-6: if bid is higher than highest_bid
        if bid_amt > highest_bid:
            # update highest_bid and winner
            highest_bid = bid_amt
            winner = bid["bidder"]
    # TODO-7: print final result
    print(f"Winner is {winner} with bid of ${highest_bid}")

    


# ============================================================
# STEP 3 — Collect bidder information
# ============================================================

"""
PROMPT
------
Ask the user for:

1. Their name
2. Their bid amount

Convert the bid to an integer.

Store the result in the bids dictionary.
"""


def get_nameandbid():

    # TODO-8
    name = input("What is your name?: ")

    # TODO-9
    bid = int(input("What is your bid?: $"))

    # TODO-10
    # store in dictionary
    bids[name] = bid


# ============================================================
# STEP 4 — Repeat for multiple bidders
# ============================================================

"""
PROMPT
------
The program should continue collecting bids until
no more bidders remain.

After each bidder ask:

"Are there any other bidders? Type 'yes' or 'no'."

If yes -> continue loop
If no -> determine winner
"""

# TODO-11
auction_finished = False

# TODO-12
# start loop while auction not finished

    # TODO-13
    # collect name and bid

    # TODO-14
    # store bid in dictionary

    # TODO-15
    # ask if there are more bidders

    # if "no" -> end loop and call find_highest_bidder


# ============================================================
# STEP 5 — Optional screen clearing
# ============================================================

"""
PROMPT
------
In the course version, the screen clears so the
next bidder cannot see the previous bid.

Optional implementation:
"""

# import os
# def clear_screen():
#     os.system('cls' if os.name == 'nt' else 'clear')


# ============================================================
# COMPLETE PROGRAM SHELL
# ============================================================

"""
If you prefer, build the entire project inside this function.
Fill in the TODO sections.
"""


def secret_auction():

    print("Welcome to the secret auction program.")

    all_bids = {}
    bidding_finished = False

    while not bidding_finished:

        # TODO-A
        name = ""

        # TODO-B
        bid = 0

        # TODO-C
        # store bid in dictionary

        # TODO-D
        should_continue = ""

        if should_continue == "no":
            bidding_finished = True
            find_highest_bidder(all_bids)

        else:
            # Optional: clear screen
            pass


# Uncomment when ready to run
# secret_auction()


# ============================================================
# SELF‑CHECK LIST
# ============================================================

"""
Make sure your program:

[ ] Uses a dictionary
[ ] Collects name and bid
[ ] Allows multiple bidders
[ ] Finds the highest bid
[ ] Prints the winner

Bonus:

[ ] Clears the screen between bidders
"""
