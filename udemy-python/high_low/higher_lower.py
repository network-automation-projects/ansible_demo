import random
from game_data import data
from art import logo, vs

# Optional: Function to clear the console (works on Mac)
def clear_screen():
    print("\033c", end="")

def get_random_account():
    # TODO: Return a random dict from data
    return random.choice(data)
    pass

def format_data(account):
    # TODO: Return formatted string like "Name, a description, from country"
    return f"{account['name']}, a {account['description']}, from {account['country']}"
    pass

def check_answer(guess, a_followers, b_followers):
    if a_followers > b_followers: 
        correct_answer = 'a' 
    else:
        correct_answer = 'b'

    if guess == correct_answer:
        return True
    else:
        return False

def game():
    # TODO: Print logo
    print(logo)
    score = 0
    game_over = False
    account_a = get_random_account()  # Start with random A
    while not game_over:
        account_b = get_random_account()  # Get B, ensure != A
        # TODO: Handle if A == B
        if account_a == account_b:
            account_b = get_random_account()
        # TODO: Print formatted A, vs, formatted B
        print(f"Compare A: {format_data(account_a)}")
        print(vs)
        print(f"Against B: {format_data(account_b)}")
        guess = input("Who has more followers? Type 'A' or 'B': ").lower()
        
        a_count = account_a["follower_count"]
        b_count = account_b["follower_count"]
        
        if check_answer(guess, a_count, b_count):
            score += 1
            # TODO: Print success message with score
            print(f"You're Right! " + str(score))
            # TODO: Set A to B for next round
            account_a = account_b
            # Optional: Clear screen
            clear_screen()
        else:
            game_over = True
            # TODO: Print game over with final score
            print(f"Game Over \n Final Score: {score}")

# Run the game
game()