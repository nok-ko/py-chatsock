import random

print(random.randint(3,6))

# random.randint()

def process_message(msg):

	# first two words matter, the rest doesn't
	words = msg.strip().split(' ', 2)
	# '!roll' alone shouldn't work
	if words[0] != '!roll':
		return
	
	if len(words) <= 1:
		return
	
	cmd = words[0]
	# words[1] is guaranteed to exist because of the if
	if 'd' in words[1]:
		dice = words[1].split('d') 
		dice_amt = dice[0]
		try:
			dice_sides = int(dice[1])
		except ValueError:
			print('Error!')
			return
		result = random.randint(1, int(dice[1]))
		print(f"Rolling... {result}!")





# bots/dice.py
# class DiceBot ...

# > !roll 1d4
# Rolling... 3!

# > !roll 3d12
# Rolling... 8 + 3 + 1 = 12!

# > !roll 0d0
# Error!

# > !roll -3d-2
# Error!

# > !roll -32
# Error!

# > !roll d
# Error!

# > !roll d12
# > Rolling... 11!

