"""
#Built in example:
import mdptoolbox.example
P, R = mdptoolbox.example.forest()
vi = mdptoolbox.mdp.ValueIteration(P, R, 0.9)
vi.run()
print("P:  {}".format(P))
print("R:  {}".format(R))
#print(dir(P))
#print(dir(R))
#print(dir(vi))
print(vi.policy) # result is (0, 0, 0)
"""
import mdptoolbox
from numpy import array

transitions = array([
    [1, 1, 1],
    [2, 1, 1]
])

reward = array([
    [1, 10],
    [2, 8],
])

discount = 1

epsilon = 100

max_iter = 100

skip_check = False

test_mdp = mdptoolbox.mdp.MDP(transitions=transitions,
                              reward=reward,
                              discount=discount,
                              epsilon=epsilon,
                              max_iter=max_iter)