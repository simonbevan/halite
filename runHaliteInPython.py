import subprocess
import random
import logging
logging.basicConfig(filename=str("game_out") + '.log', level=logging.DEBUG)

for i in range(10000):
    for size in range(20, 50, 5):

        bs = str(size) + " " + str(size)
        np = random.randint(2,6)
        enemy = ['python3 BrutalBevster.py', 'python3 SneakyBevster.py']
        p2 = enemy[random.randint(0, 1)]
        p3 = enemy[random.randint(0, 1)]
        p4 = enemy[random.randint(0, 1)]
        p5 = enemy[random.randint(0, 1)]
        p6 = enemy[random.randint(0, 1)]
        if np==2:
            out = subprocess.check_output(['./halite', '-q','-d', bs, 'python3 MyBot.py',p2])
        elif np==3:
            out = subprocess.check_output(['./halite', '-q', '-d', bs, 'python3 MyBot.py', p2,p3])
        elif np==4:
            out = subprocess.check_output(['./halite', '-q', '-d', bs, 'python3 MyBot.py', p2,p3,p4])
        elif np==5:
            out = subprocess.check_output(['./halite', '-q', '-d', bs, 'python3 MyBot.py', p2,p3,p4,p5])
        else:
            out = subprocess.check_output(['./halite', '-q', '-d', bs, 'python3 MyBot.py', p2,p3,p4,p5,p6])

        logging.debug(out)


            #print(out)

#-d "50 50" "python3 MyBot.py" "python3 SneakyBevster.py" "python3 BrutalBevster.py"