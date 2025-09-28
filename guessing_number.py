import random
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_welcome_message():
    print('=' * 50)
    print('     Welcome to the Number Guessing Adventure!')
    print('=' * 50)
    print('In this exciting game, a secret number between 1 and 100 has been chosen.')
    print('You will have 10 attempts to guess it correctly.')
    print('After each guess, you will receive hints: too high or too low.')
    print('Good luck, brave guesser! May your intuition guide you.')
    print('=' * 50)
    time.sleep(3)

def generate_secret_number():
    return random.randint(1, 100)

def get_user_guess(attempt):
    while True:
        try:
            guess_input = input(f'Attempt {attempt}: Enter your guess (1-100): ')
            guess = int(guess_input.strip())
            if 1 <= guess <= 100:
                return guess
            else:
                print('Please enter a number between 1 and 100.')
                time.sleep(1)
        except ValueError:
            print('Invalid input. Please enter a valid integer.')
            time.sleep(1)

def provide_hint(guess, secret):
    if guess > secret:
        return 'Too high! The secret number is lower.'
    elif guess < secret:
        return 'Too low! The secret number is higher.'
    else:
        return 'Perfect match!'

def display_game_over_win(secret, attempts_used):
    print('\n' + '*' * 50)
    print('     Congratulations! You have triumphed!')
    print(f'     The secret number was {secret}.')
    print(f'     You guessed it in {attempts_used} attempts.')
    print(f'     Your score: {max(0, 100 - (attempts_used * 10))}')
    print('*' * 50)
    time.sleep(2)

def display_game_over_lose(secret):
    print('\n' + '*' * 50)
    print('     Oh no! The game has ended.')
    print(f'     The secret number was {secret}.')
    print('     Better luck next time!')
    print('*' * 50)
    time.sleep(2)

def play_again():
    while True:
        choice = input('\nWould you like to play again? (y/n): ').strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print('Please enter y for yes or n for no.')
            time.sleep(1)

def main():
    clear_screen()
    display_welcome_message()
    
    while True:
        secret_number = generate_secret_number()
        max_attempts = 10
        attempts = 0
        
        print(f'\nA secret number has been generated between 1 and 100.')
        print(f'You have {max_attempts} attempts to guess it.')
        time.sleep(2)
        
        won = False
        
        while attempts < max_attempts:
            user_guess = get_user_guess(attempts + 1)
            attempts += 1
            remaining = max_attempts - attempts
            
            hint = provide_hint(user_guess, secret_number)
            print(f'{hint}')
            
            if user_guess == secret_number:
                won = True
                display_game_over_win(secret_number, attempts)
                break
            else:
                if remaining > 0:
                    print(f'{remaining} attempts remaining.')
                time.sleep(1)
        
        if not won:
            display_game_over_lose(secret_number)
        
        if not play_again():
            print('\nThank you for playing! Goodbye.')
            time.sleep(2)
            break
        
        clear_screen()
        display_welcome_message()

if __name__ == "__main__":
    main()
