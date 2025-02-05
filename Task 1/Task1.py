"""
CS3080 Project - Task 1
This program will scrape a website,
https://www.ef.edu/english-resources/english-vocabulary/top-1000-words/, for the top 1000
English words. The program will take these words and put them into an Excel sheet. This Excel
sheet will then be used as input to create a hangman-like word game where the user has a limited
number of guesses to guess each letter in the random word out of the Excel sheet.
"""
import requests, bs4, openpyxl, random, textwrap

FILE = "Task1.xlsx"
INCORRECT_GUESSES = 3


class Game():

    def __init__(self):
        self.word = self.select_word(FILE)
        self.letters_guessed = []
        self.incorrect_guesses = 0
        self.guess_index = 1

    def select_word(self, file):
        wb = openpyxl.load_workbook(file)
        sheet = wb['Sheet']

        word = [cell.value for cell in sheet['A'] if cell.value is not None]

        selected_word = random.choice(word)
        return selected_word

    def display_word(self):
        for char in self.word:
            if char is not None:
                if char in self.letters_guessed:
                    print(f"{char}", end=' ')
                else:
                    print("_", end=' ')
        print()

    def guess_letter(self):
        valid = False

        while not valid:
            guess = input(f"Guess {self.guess_index} (Incorrect Guesses {self.incorrect_guesses}): ").lower()
            if len(guess) > 1:
                print("ERROR: Please input only one letter")
                continue
            if guess.isdigit():
                print("ERROR: Guess must be a letter")
                continue
            if guess in self.letters_guessed:
                print(f"You have already guessed {guess}!")
                continue
            if guess not in self.word:
                print(f"There is no {guess} in the word")
                self.incorrect_guesses += 1
                self.letters_guessed.append(guess)
                valid = True
                break
            else:
                print(f"{guess} is in the word!")
                self.letters_guessed.append(guess)
                valid = True
                break


def get_words():
    """Get the words off of the internet."""
    try:
        response = requests.get('https://www.ef.edu/english-resources/english-vocabulary/top-1000-words/')
        response.raise_for_status()
    except Exception as e:
        print(f"ERROR: {e}\nCheck Internet Connection")
        quit()

    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    div = soup.find('div', {'class': 'field-item even'})

    paragraphs = div.find_all('p')

    words = paragraphs[1].text
    words = words.split()

    return words


def create_sheet(words):
    """Create the word bank spreadsheet."""
    wb = openpyxl.Workbook()
    sheet = wb.active

    for row, word in enumerate(words, start=1):
        sheet.cell(row, 1, word)

    wb.save('Task1.xlsx')


def main_game(game):
    """Play Hangman Game."""
    print("Welcome to Nick and Devon's Hangman Game!")
    print(textwrap.fill(
        f"You will have {INCORRECT_GUESSES} guesses to reveal the hidden word selected from the top 1000 English words.",
        40))

    while game.incorrect_guesses != INCORRECT_GUESSES:
        game.display_word()
        game.guess_letter()


def main():
    """Run Main Function."""
    word_bank = get_words()
    create_sheet(word_bank)

    game = Game()

    main_game(game)


if __name__ == "__main__":
    main()