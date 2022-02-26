from wordle_bot import wordle_bot, fromBase3
import numpy as np


bot = wordle_bot()

# setting up the bot
bot.setup()

while True:
	print("Suggestions:\n", bot.getTop(), "\n")
	word = input("Word you typed?\n> ")
	if(len(word) != 5):
		print("\nPlease type a valid word of length 5.")
		continue

	pattern = input("\nPattern of the word?\n> ")
	if(len(pattern) != 5):
		print("\nPlease type a valid pattern of length 5.")
		continue

	pattern = fromBase3(pattern)
	if(pattern > 242 or pattern < 0):
		print("\nPlease type a pattern in the appropriate range.")
		continue

	frame = (bot.patterns[pattern], word)
	filtered = bot.filter(frame)
	print(f'\n[RES] These are all the words that fit the frame {frame}:\n{filtered}')

	inp = int(input("\nDo you wish to filter the wordlist based on the frame? (Yes : 1, No : 0)\n> "))
	if(inp == 1):
		bot.words = filtered
		bot.filtered = bot.calcWordsEntropy()
	print()