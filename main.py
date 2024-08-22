import random

# Define card types and point values
LEFT = '<'
RIGHT = '>'
WRONG = 'X'

CARD_TYPES = [LEFT, RIGHT, WRONG]
POINTS = {
    ('<', 'leftmost'): 5,
    ('<', 'chained'): 2,
    ('<', 'elsewhere'): 1,
    ('>', 'rightmost'): 5,
    ('>', 'chained'): 3,
    ('>', 'elsewhere'): 1
}

# Deck creation and shuffling
def create_deck():
    return [LEFT] * 12 + [RIGHT] * 12 + [WRONG] * 12

def shuffle_deck(deck):
    random.shuffle(deck)
    return deck

# Deal cards to players
def deal_cards(deck, num_cards=5):
    return [deck.pop() for _ in range(num_cards)]

# Print the cards in hand and in the middle
def print_game_state(player_hand, middle_cards):
    print("Your hand:", player_hand)
    print("Middle cards:", middle_cards)

# Function to evaluate the score
def calculate_score(arrangement):
    arrangement = twoWrongsMakeARight(arrangement)
    score = 0
    for idx, card in enumerate(arrangement):
        points = 0
        if card == LEFT:
            if idx == 0:
                points = POINTS[(LEFT, 'leftmost')]
                print(LEFT, 'leftmost', points, 'pts')
            elif arrangement[idx - 1] == LEFT:
                points = POINTS[(LEFT, 'chained')]
                print(LEFT, 'chained', points, 'pts')
            else:
                points = POINTS[(LEFT, 'elsewhere')]
                print(LEFT, 'alone', points, 'pts')
        elif card == RIGHT:
            if idx == len(arrangement) - 1:
                points = POINTS[(RIGHT, 'rightmost')]
                print(RIGHT, 'rightmost', points, 'pts')
            elif arrangement[idx + 1] == RIGHT:
                points = POINTS[(RIGHT, 'chained')]
                print(RIGHT, 'chained', points, 'pts')
            else:
                points += POINTS[(RIGHT, 'elsewhere')]
                print(RIGHT, 'alone', points, 'pts')
        score += points
    return score

def twoWrongsMakeARight(arrangement):
    new_arrangement = []
    for idx, card in enumerate(arrangement):
        if card == WRONG:
            if((idx == 0 and arrangement[idx + 1] == WRONG) 
               or (idx < len(arrangement) - 1 and arrangement[idx + 1]) == WRONG):
                new_arrangement.append(RIGHT)
        else:
            new_arrangement.append(card)
    if(len(arrangement) != len(new_arrangement)):
        print("Two wrongs make a right:", new_arrangement)
    return new_arrangement        

def is_valid_arrangement(arrangement, hand, middle_cards):
    # Flatten the middle cards and hand
    available_cards = middle_cards + hand
    # Check if arrangement contains only available cards and has correct length
    return sorted(arrangement) == sorted(available_cards) and len(arrangement) == 7

def get_player_arrangement(player_hand, middle_cards):
    player_arrangement = input("Enter your arrangement of 7 cards (e.g., '< < X > > <'): ").upper().split()
    
    if(not is_valid_arrangement(player_arrangement, player_hand, middle_cards)):
        print("Invalid arrangement. Try again.")
        return get_player_arrangement(player_hand, middle_cards)
    
    cursor_idx = 0
    for card in middle_cards:
       if card not in player_arrangement[cursor_idx:]:
           print("Invalid arrangement. Order of middle cards was not preserved!")
           return get_player_arrangement(player_hand, middle_cards)
       cursor_idx = player_arrangement.index(card, cursor_idx)

    return player_arrangement
    X
# Game setup
def setup_game():
    deck = shuffle_deck(create_deck())
    player_hand = deal_cards(deck)
    middle_cards = [deck.pop(), deck.pop()]
    return deck, player_hand, middle_cards

# Simulate a round of play
def play_round(player_hand, middle_cards):
    print_game_state(player_hand, middle_cards)
    
    # Player discards one card
    discard = input("Discard one card from your hand: ").upper()
    if discard not in player_hand:
        print("Invalid card. Try again.")
        return play_round(player_hand, middle_cards)
    player_hand.remove(discard)
    
    # Place an additional card in the middle
    middle_cards.append(deck.pop())

    print_game_state(player_hand, middle_cards)
    
    # Get player arrangement
    player_arrangement = get_player_arrangement(player_hand, middle_cards)
    
    # Compute score
    score = calculate_score(player_arrangement)
    print("Your score:", score)
    
    # Dummy computer move for simplicity
    computer_arrangement = middle_cards + [LEFT] * 3  # Simple example
    computer_score = calculate_score(computer_arrangement)
    print("Computer score:", computer_score)
    
    return score, computer_score

# Main game loop
def main():
    num_rounds = 5
    total_player_score = 0
    total_computer_score = 0
    
    for round_num in range(num_rounds):
        print(f"Round {round_num + 1}")
        global deck
        deck, player_hand, middle_cards = setup_game()
        player_score, computer_score = play_round(player_hand, middle_cards)
        total_player_score += player_score
        total_computer_score += computer_score
    
    print(f"Final Scores: Player {total_player_score}, Computer {total_computer_score}")
    if total_player_score > total_computer_score:
        print("You win!")
    elif total_player_score < total_computer_score:
        print("Computer wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    main()