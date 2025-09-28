import random
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_welcome():
    print('=' * 50)
    print('     Welcome to the Number Guessing Adventure!')
    print('=' * 50)
    print('Guess a number between 1 and 100 in 10 attempts. Get hints: too high/low.')
    print('Good luck!')
    print('=' * 50)
    time.sleep(2)

def generate_secret():
    return random.randint(1, 100)

def get_guess(attempt):
    while True:
        try:
            guess = int(input(f'Attempt {attempt}: Enter guess (1-100): ').strip())
            if 1 <= guess <= 100:
                return guess
            print('Enter a number between 1 and 100.')
        except ValueError:
            print('Invalid input. Enter an integer.')
        time.sleep(1)

def get_hint(guess, secret):
    if guess > secret:
        return 'Too high! Lower.'
    elif guess < secret:
        return 'Too low! Higher.'
    return 'Correct!'

def show_win(secret, attempts):
    score = max(0, 100 - (attempts * 10))
    print('\n' + '*' * 50)
    print(f'Congratulations! Secret: {secret}. Attempts: {attempts}. Score: {score}')
    print('*' * 50)
    time.sleep(2)

def show_lose(secret):
    print('\n' + '*' * 50)
    print(f'Game over! Secret was {secret}. Better luck next time!')
    print('*' * 50)
    time.sleep(2)

def play_again():
    while True:
        choice = input('\nPlay again? (y/n): ').strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        print('Enter y or n.')
        time.sleep(1)

def main():
    clear_screen()
    display_welcome()
    
    while True:
        secret = generate_secret()
        max_attempts = 10
        attempts = 0
        won = False
        
        print(f'\nSecret number generated (1-100). {max_attempts} attempts.')
        time.sleep(1)
        
        while attempts < max_attempts:
            guess = get_guess(attempts + 1)
            attempts += 1
            remaining = max_attempts - attempts
            
            hint = get_hint(guess, secret)
            print(hint)
            
            if guess == secret:
                won = True
                show_win(secret, attempts)
                break
            else:
                if remaining > 0:
                    print(f'{remaining} attempts left.')
                time.sleep(1)
        
        if not won:
            show_lose(secret)
        
        if not play_again():
            print('\nThanks for playing! Goodbye.')
            time.sleep(1)
            break
        
        clear_screen()
        display_welcome()

if __name__ == "__main__":
    main()
