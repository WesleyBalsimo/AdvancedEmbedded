#dice game
#player A rolls 3d12 Player B rolls 4d8
#player A wins on ties

from random import randint
#randint example
#d8 = randint(1, 8)
#d12 = randint(1, 12)

def roll_dice(num_rolls, sides):
    total = 0
    for _ in range(num_rolls):
        total += randint(1, sides)
    return total

#montecarlo simulation
num_a_wins = 0
num_b_wins = 0
length = 10000
for _ in range(length):
    heat = 5
    for _ in range(heat):
        a_score = roll_dice(3, 12)
        b_score = roll_dice(4, 8)

        if a_score >= b_score:
            #print("Player A wins with a score of", a_score, "against Player B's score of", b_score)
            num_a_wins += 1
        else:
            #print("Player B wins with a score of", b_score, "against Player A's score of", a_score)
            num_b_wins += 1
        if num_a_wins >= 3:
            break
        if num_b_wins >= 3:
            break
    num_a_wins = 0
    num_b_wins = 0

print("Player A wins:", num_a_wins)
print("Player B wins:", num_b_wins)

#check to see if for loop adds up
sum = num_a_wins + num_b_wins
print("Total games played:", sum)