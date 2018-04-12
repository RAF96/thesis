import numpy
import sympy

from matplotlib import pyplot, animation

class WriterPlot:

    def __init__(self, function):
        self.fig = pyplot.figure()
        self.ax = pyplot.axes(xlim=(-2, 2), ylim=(-10, 10))
        pyplot.gca().xaxis.grid(True)
        pyplot.gca().yaxis.grid(True)
        self.line, = self.ax.plot([], [])
        self.function = None
        self.t = 0
        self.dt = 0.05
        print("WritePlot ", function)
        function_lambdify = sympy.lambdify((sympy.abc.x, sympy.abc.t), function)
        self.function = function_lambdify 
        

    def get_init(self):
        def init():
            self.line.set_data([], [])
            return self.line,
        return init


    def get_animate(self):
        def animate(i):
            x = numpy.linspace(-2, 2, 1000)
            y = self.function(x, self.t)
            self.t += self.dt
            self.line.set_data(x, y)
            return self.line,
        return animate

    def print_animation(self):
        x = animation.FuncAnimation(self.fig, self.get_animate(), init_func=self.get_init(), 
                                       frames=200, interval=20, blit=True)
        pyplot.show()
