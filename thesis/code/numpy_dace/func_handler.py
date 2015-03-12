## The goal of this program is to create a class which can hold the objective function
## for each egoist object.

## hmm. I might be over-engineering here. For now, the ego class will just have a function, no handler.
## That function is just assumed to be something with an applyTo that takes arguments of the shape of egoist.X[i]



# test function for 1d optimization: sum of an n-dimensional sine wave, which creates a bunch of local minima, and an n-dimensional parabola, creating a global minimum near (minimum_coord,minimum_coord,...,minimum_coord)
def sin_plus_quad(period=1,minimum_coord=5):
    def func(x):
        height=0
        for component in x:
            height+=(component-minimumcoord)**2 + sin(component*2*Math.pi/period)
        return height


def fun_test(x):
    local_min_component = Math.sin

