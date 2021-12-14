from inspect import getsource
import matplotlib.pyplot as plt
from typing import Callable
e = 2.71828182845


class Tetration:
    __slots__ = ('f', 'start', 'end', 'n', 'data')

    def __init__(self, f: Callable[[float, float], float], start: float = 0.1, end: float = None, n: int = 60):
        self.f = f
        self.start = start
        self.end = e**(1/e) - 1e-10 if end is None else end
        self.n = n
        self.data: list[list[float, ], ]

    def __repr__(self):
        lines = getsource(self.f).splitlines()
        return f'{lines[0][4:-1]} = {lines[-1][11:]}'

    @staticmethod
    def linmap(value: float, actual_bounds: tuple[float, float], desired_bounds: tuple[float, float]) -> float:
        return desired_bounds[0] + (value - actual_bounds[0]) * (desired_bounds[1] - desired_bounds[0]) / (
                    actual_bounds[1] - actual_bounds[0])

    @staticmethod
    def pow(a: float, b: float) -> float:
        return 1/(a ** (-b)) if b <= 0 else a ** b

    def calculate(self, iterations: int = 50, max_value: float = 2.719):
        data = []
        for i in range(1, self.n + 1):
            x0 = self.linmap(i, (0, self.n), (self.start, self.end))
            x = x0
            data_x: list[float, ] = [x]
            for j in range(iterations):
                x = self.f(x, x0)
                if x > max_value:
                    break
                data_x.append(x)
            data.append(data_x)
        self.data = data

    def _plot(self, show_boundary: bool = False, color: str = 'black'):
        plt.clf()
        plt.title(repr(self))
        plt.xlabel('iteration')
        plt.ylabel('x ∈ ℝ')
        if show_boundary:
            plt.axhline(y=e ** (1 / e), c='r', ls='--', lw=1)
            plt.axhline(y=e, c='r', ls='-', lw=1)
        for x in self.data:
            plt.plot(x, c=color, lw=.5, aa=True)

    def show(self, *args, **kwargs):
        self._plot(*args, **kwargs)
        plt.show()


def f(x, c):
    return c ** x


if __name__ == '__main__':
    tetration = Tetration(f)
    tetration.calculate()
    tetration.show()
