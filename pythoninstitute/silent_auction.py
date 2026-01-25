"""
Silent Auction Bidding System

This program collects bids from multiple users and determines the winner
based on the highest bid amount.
"""

import os
import art

# Dictionary to store all bids
# Key: bidder name (string)
# Value: bid amount (float)
bids = {}


def clear_screen():
    """
    Clear the terminal screen.
    Works on both Windows and Unix-based systems.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def collect_bid():
    """
    Collect a single bid from a user.
    
    Returns:
        tuple: (bidder_name, bid_amount) or (None, None) if invalid input
    """
    # Ask for name input
    bidder_name = input("What is your name? ").strip()
    
    # Ask for bid price
    bid_amount_input = input("What is your bid? $").strip()
    
    # Validate and convert bid amount to float
    try:
        bid_amount = float(bid_amount_input)
        if bid_amount < 0:
            print("Bid amount must be positive. Please try again.")
            return None, None
        return bidder_name, bid_amount
    except ValueError:
        print("Invalid bid amount. Please enter a number.")
        return None, None


def find_winner():
    """
    Find the highest bid in the dictionary and return the winner.
    
    Returns:
        tuple: (winner_name, winning_bid) or (None, None) if no bids
    """
    if not bids:
        return None, None
    
    # Find the highest bid amount
    winning_bid = max(bids.values())
    
    # Find the bidder(s) with the winning bid
    # (in case of ties, we'll take the first one)
    winner_name = None
    for name, bid in bids.items():
        if bid == winning_bid:
            winner_name = name
            break
    
    return winner_name, winning_bid


def main():
    """
    Main function that runs the silent auction bidding system.
    """
    # Show logo from art.py
    art.show_logo()
    
    # Flag to control the bidding loop
    more_bidders = True
    
    # Loop to collect bids from multiple users
    while more_bidders:
        # Collect a bid from the current user
        bidder_name, bid_amount = collect_bid()
        
        # Only add to dictionary if input was valid
        if bidder_name and bid_amount is not None:
            # Add name and bid into dictionary as key and value
            bids[bidder_name] = bid_amount
            print(f"\n✓ Bid recorded: {bidder_name} bid ${bid_amount:.2f}\n")
        else:
            print("Bid not recorded. Please try again.\n")
        
        # Ask if there are other users who want to bid
        continue_bidding = input("Are there any other bidders? Type 'yes' or 'no': ").strip().lower()
        
        if continue_bidding == 'yes':
            # Clear the screen for the next bidder
            clear_screen()
            # Show logo again for the next bidder
            art.show_logo()
        else:
            # No more bidders, exit the loop
            more_bidders = False
    
    # Clear screen before showing results
    clear_screen()
    
    # Find the highest bid in the dictionary and declare them as the winner
    winner_name, winning_bid = find_winner()
    
    # Display the winner
    if winner_name:
        print("\n" + "="*50)
        print("🎉 AUCTION RESULTS 🎉")
        print("="*50)
        print(f"\nThe winner is {winner_name} with a bid of ${winning_bid:.2f}!")
        print("\n" + "="*50)
    else:
        print("\nNo bids were placed in this auction.")


if __name__ == "__main__":
    main()

