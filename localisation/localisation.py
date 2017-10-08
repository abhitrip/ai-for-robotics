# The function localise takes the following arguments:
#
# colours:
#        2D list, each entry either 'R' (for red cell) or 'G' (for green cell)
#
# measurements:
#        list of measurements taken by the robot, each entry either 'R' or 'G'
#
# motions:
#        list of actions taken by the robot, each entry of the form [dy,dx],
#        where dx refers to the change in the x-direction (positive meaning
#        movement to the right) and dy refers to the change in the y-direction
#        (positive meaning movement downward)
#        NOTE: the *first* coordinate is change in y; the *second* coordinate is
#              change in x
#
# sensor_right:
#        float between 0 and 1, giving the probability that any given
#        measurement is correct; the probability that the measurement is
#        incorrect is 1-sensor_right
#
# p_move:
#        float between 0 and 1, giving the probability that any given movement
#        command takes place; the probability that the movement command fails
#        (and the robot remains still) is 1-p_move; the robot will NOT overshoot
#        its destination in this exercise
#
# The function should RETURN (not just show or print) a 2D list (of the same
# dimensions as colors) that gives the probabilities that the robot occupies
# each cell in the world.
#
# Compute the probabilities by assuming the robot initially has a uniform
# probability of being in any cell.
#
# Also assume that at each step, the robot:
# 1) first makes a movement,
# 2) then takes a measurement.
#
# Motion:
#  [0,0] - stay
#  [0,1] - right
#  [0,-1] - left
#  [1,0] - down
#  [-1,0] - up

def localise(colours, measurements, motions, sensor_right, p_move):
    num_measurements = len(measurements)
    r,c =  len(colours), len(colours[0])
    pinit = 1./r*c
    p = [[pinit for i in range(c)] for j in range(c)]
    for i in range(num_measurements):
        meas, motion = measurements[i], motions[i]
        p = move2D(p, motion, p_move)
        p = sense2D(p, meas, colours, sensor_right)
        
    return p

def sense2D(p, Z, colours, sensor_right):
    r, c = len(p), len(p[0])
    q = [[0 for i in range(c)] for j in range(r)]
    pHit = sensor_right
    pMiss = 1-sensor_right
    sum_q = 0.
    for i in range(r):
        for j in range(c):
            hit = (colours[i][j]==Z)
            q[i][j] = p[i][j]*(hit*pHit+(1-hit)*pMiss)
            sum_q += q[i][j]
    for i in range(r):
        for j in range(c):
            q[i][j]/=sum_q
    return q

def move2D(p, U, p_move):
    r, c = len(p), len(p[0])
    ur, uc = U[0], U[1]
    p_remain = 1 - p_move
    if U[0]==0 and U[1]==0: return p
    q = [[0 for i in range(c)] for j in range(r)]
    for i in range(r):
        for j in range(c):          
            s = (1-p_move)*p[i][j]
            s += p_move*p[(i-ur)%r][(j-uc)%c]
            q[i][j] = s
    return q




def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x),r)) + ']' for r in p]
    print '[' + ',\n '.join(rows) + ']'

def test_case1():
    colours = [['G', 'G', 'G'],
            ['G', 'R', 'G'],
            ['G', 'G', 'G']]
    measurements = ['R']

    motions = [[0,0]]
    sensor_right = 1.0

    p_move = 1.0
    correct_answer = (
    [[0.0, 0.0, 0.0],
     [0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0]])
    pLocalise = localise(colours, measurements, motions, sensor_right, p_move)
    show(pLocalise)
    show(correct_answer)

def test_case2():
    colours = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
    measurements = ['R']
    motions = [[0,0]]
    sensor_right = 1.0
    p_move = 1.0
    correct_answer = (
    [[0.0, 0.0, 0.0],
     [0.0, 0.5, 0.5],
    [0.0, 0.0, 0.0]])
    sensor_right = 1.0
    pLocalise = localise(colours, measurements, motions, sensor_right, p_move)
    show(pLocalise)
    show(correct_answer)


def test_case3():
    colours = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
    measurements = ['R']
    motions = [[0,0]]
    sensor_right = 0.8
    p_move = 1.0
    correct_answer = (
    [[0.06666666666, 0.06666666666, 0.06666666666],
     [0.06666666666, 0.26666666666, 0.26666666666],
    [0.06666666666, 0.06666666666, 0.06666666666]])
    pLocalise = localise(colours, measurements, motions, sensor_right, p_move)
    show(pLocalise)
    show(correct_answer)

def test_case4():
    colours = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
    measurements = ['R', 'R']
    motions = [[0,0], [0,1]]
    sensor_right = 0.8
    p_move = 1.0
    correct_answer = (
    [[0.03333333333, 0.03333333333, 0.03333333333],
     [0.13333333333, 0.13333333333, 0.53333333333],
    [0.03333333333, 0.03333333333, 0.03333333333]])
    pLocalise = localise(colours, measurements, motions, sensor_right, p_move)
    show(pLocalise)
    show(correct_answer)

def test_case5():
    colours = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
    measurements = ['R', 'R']
    motions = [[0,0], [0,1]]
    sensor_right = 1.0
    p_move = 1.0
    pLocalise = localise(colours, measurements, motions, sensor_right, p_move)
    correct_answer = (
    [[0.0, 0.0, 0.0],
     [0.0, 0.0, 1.0],
    [0.0, 0.0, 0.0]])
    show(pLocalise)
    show(correct_answer)

def test_case6():
    colours = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
    measurements = ['R', 'R']
    motions = [[0,0], [0,1]]
    sensor_right = 0.8
    p_move = 0.5
    correct_answer = (
    [[0.0289855072, 0.0289855072, 0.0289855072],
     [0.0724637681, 0.2898550724, 0.4637681159],
    [0.0289855072, 0.0289855072, 0.0289855072]])
    pLocalise = localise(colours, measurements, motions, sensor_right, p_move)
    show(pLocalise)
    show(correct_answer)

def test_case7():
    colours = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
    measurements = ['R', 'R']
    motions = [[0,0], [0,1]]
    sensor_right = 1.0
    p_move = 0.5
    correct_answer = (
    [[0.0, 0.0, 0.0],
     [0.0, 0.33333333, 0.66666666],
    [0.0, 0.0, 0.0]])
    pLocalise = localise(colours, measurements, motions, sensor_right, p_move)
    show(pLocalise)
    show(correct_answer)
    
test_case1()