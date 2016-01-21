import sys
import re
from random import randint

pattern = (
		r"^(?:(?:\[([1-9][0-9]{1,2}|[2-9])"		#match.group(1) 2-999 valid
		"/([1-9][0-9]{0,2})"					#match.group(2) 1-999 valid
		"([\+\-])?\])"							#match.group(3) + or - valid
		"|([1-9][0-9]{0,2}))?"					#match.group(4) 1-999 valid
		"d([1-9][0-9]{1,2}|[2-9])"				#match.group(5) 2-999 valid
		"(?:([\+\-])"							#match.group(6) + or - valid
		"([1-9][0-9]{0,2}))?"					#match.group(7) 1-999 valid
		)
result = []
final = 0
dice = 1
sides = 2
keep = 0
discarding_roll = False

def msgError():
	print "Exactly one argument expected."
	print "Please provide an argument of the form XdY+Z or [A/B(+/-)]dY+Z"
	print "XdY+Z is a standard roll"
	print "[A/B+]dY+Z is a discarding roll, A dice are rolled and B are kept"
	print "\tX = the number of dice to roll"
	print "\tA = number of dice to roll for a discarding roll"
	print "\tB = the number of dice to keep, must be less than A"
	print "\t(+/-) = if '+' highest rolls kept, if '-' then lowest, default is +"
	print "\tdY = the number of sides per die, minimum 2"
	print "\t+Z = (optional)any bonuses or penalties to be added/subtracted"
	print "\t\tIf applying a penalty '-' can be substituted for '+'"
	print "\t\tAll numbers must be between 1 and 999"
	
	sys.exit()

def rollDie(num_sides):
	roll_result = randint(1,num_sides)
	return roll_result
	
def discardRoll(result_list,num_to_keep,keep_hi_bool):
	temp = sorted(result_list)
	out_val = 0
	if keep_hi_bool:
		out_val = sum(temp[-num_to_keep:])
	else:
		out_val = sum(temp[num_to_keep:])
	return out_val
	
if len(sys.argv) != 2:
	msgError()
	
match = re.search(pattern, sys.argv[1])

#full_grp							#match.group(0) full match or None if no match
discard_roll_grp = match.group(1)	#match.group(1) # of die for discard roll (2-999)
discard_keep_grp = match.group(2)	#match.group(2) # of die to keep from discard roll
discard_hi_low_grp = match.group(3)	#match.group(3) + keep high rolls, - keep low rolls
standard_roll_grp = match.group(4)	#match.group(4) # of die for regular roll (2-999)
sides_grp = match.group(5)			#match.group(5) number of sides, at least 2
bonus_add_sub = match.group(6)		#match.group(6) addition or subtraction
bonus_value = match.group(7)		#match.group(7) bonus or penalty

if match:
	if discard_roll_grp:
		dice = int(discard_roll_grp)
		keep = int(discard_keep_grp)
		discarding_roll = True
		if keep > dice:
			msgError()		
	elif standard_roll_grp:
		dice = int(standard_roll_grp)
		
	sides = int(sides_grp)
	
	for i in range(dice):
		result.append(rollDie(sides))
	
	if discarding_roll:
		if discard_hi_low_grp:
			if str(discard_hi_low_grp) == "+":
				keep_hi = True
			elif str(discard_hi_low_grp) == "-":
				keep_hi = False
			else:
				msgError()
		else:
			keep_hi = True
			
		final = discardRoll(result,keep,keep_hi)
	else:
		final = sum(result)
		
	
	if bonus_add_sub and bonus_value:
		bonus = int(bonus_value)
		if str(bonus_add_sub) == "+":
			final = final + bonus
		elif str(bonus_add_sub) == "-":
			final = final - bonus
		else:
			msgError()
	
	print "  ".join(str(roll) for roll in result)
	print "You rolled " + str(final) + "."
	
else:
	msgError()