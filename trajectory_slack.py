"""
    Modelisation of the trajectory of a slackliner.
"""
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from scipy.optimize import minimize_scalar

def main(xc, l_spot=50, l_slack=51, 
        poids=750, elasticity=0.01,
        NB_ITERATION=5):
    """
    xc : where to put the slackliner (0 < xc < l_spot)
        can (and should) be a numpy array.
    l_spot = 50 # in meters : distance between anchors
    l_slack = 51 # in meters : length of the webbing rigged
    poids = 750 # in N
    elasticity = 0.1 # how may elasticity under 10kN? (default 10%)
    NB_ITERATION = 10 # iteration of "without elasticity + new line length"
    """
    assert(poids > 0)
    assert(l_spot < l_slack)
    assert(elasticity >= 0)
    assert(np.amin(xc) > 0)
    assert(np.amax(xc) < l_spot)

    elasticity /= 10000 # SI

    def cost_parametric_function(y, x, l_slack_gd):
        l_slack_gauche, l_slack_droite = l_slack_gd
        return (sqrt(x*x + y*y) + sqrt((x-l_spot)**2 + y*y) - \
                l_slack_gauche - l_slack_droite)**2

    def len_line(x, y):
        """ 
        returns the length of both left and right parts of the line
        """
        assert(0 <= x and x <= l_spot)
        assert(y <= 0)

        def len_left(x, y):
            """ 
            returns the length of the left part of the line
            """
            return sqrt(x*x + y*y)

        def len_right(x, y):
            return len_left(l_spot-x, y)

        return np.array((len_left(x, y), len_right(x, y)))

    def len_line_rest(x):
        """ 
        returns the length of both left and right parts of the line
        if there were no elasticity
        """
        assert(0 <= x and x <= l_spot)

        def len_left_rest(x):
            """ 
            returns the length of the left part of the line
            if there were no elasticity
            """
            return x * l_slack / l_spot

        def len_right_rest(x):
            return len_left_rest(l_spot-x)

        return np.array((len_left_rest(x), len_right_rest(x)))

    def find_my_height(x):
        """ find the corresponding y for 0 <= x <= l_spot"""
        assert(0 <= x and x <= l_spot)

        force = np.array((0, 0))
        l_slack_gd = len_line_rest(x)
        for _ in range(NB_ITERATION):
            y = -abs(minimize_scalar(cost_parametric_function,
                args=(x, l_slack_gd)).x)

            sin_angles = -y / len_line(x, y)

            # ratio is f_left/f_right
            ratio = sin_angles[1]/sin_angles[0] * \
                    l_slack_gd[1]/l_slack_gd[0]

            f_right = poids / (1 + ratio)

            force = np.array((f_right * ratio, f_right))

            l_slack_gd = len_line_rest(x) * (1 + force * elasticity)
        return y

    # compute find_my_height(xc), xc may be a np array or a float
    vector_fmh = np.vectorize(find_my_height)
    return vector_fmh(xc)

if __name__ == "__main__":
    l_spot = 50
    xc = np.arange(0.1, l_spot-0.1, 0.1)
    yc = main(xc, l_spot=50, l_slack=51,
            poids=750, elasticity=0.01,
            NB_ITERATION=5)
    print("Sag is", abs(min(yc)), "meters.")
    plt.plot(xc, yc, "b")
    plt.axis("equal")
    plt.show()
