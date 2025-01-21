from ACO import ACO
from randomSearch import RandomSearch

aco = ACO('max3sat_aco\examples\SAT2.txt')
best_ant, time = aco.initialize()
print('=================================================')
print(aco.graph)
print('=================================================')
print(str(best_ant.performance))
print(f'Finished in {time}s')

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error

def plot_line_graph_polynomial_fit(y_values: list | np.ndarray, 
                                   x_values: list = None,
                                   max_degree=1, 
                                   graph_title='Graph with Polynomial Regression',
                                   x_label='X', 
                                   y_label='Y',
                                   x_rotation=90,
                                   fig_size=(15, 6),
                                   x_ticks=None,
                                   y_ticks=None,
                                   grid: bool = False
                                   ):
    
    def find_best_polynomial_degree(x, y, max_degree):
        best_degree = 1
        best_error = float('inf')

        for degree in range(1, max_degree + 1):
            coefficients = np.polyfit(x, y, degree)
            polynomial = np.poly1d(coefficients)
            y_pred = polynomial(x)
            error = mean_squared_error(y, y_pred)

            if error < best_error:
                best_error = error
                best_degree = degree

        return best_degree

    if x_values is None:
        x_values = np.arange(1, len(y_values) + 1)

    # Find the best polynomial degree
    best_degree = find_best_polynomial_degree(x_values, y_values, max_degree)

    # Calculate the best polynomial regression
    coefficients = np.polyfit(x_values, y_values, best_degree)
    polynomial = np.poly1d(coefficients)
    regression_y_values = polynomial(x_values)

    # Plot the original data points
    plt.figure(figsize=fig_size)
    plt.plot(x_values, y_values, marker='o', linestyle='-', color='b', label=x_label)

    # Plot the best fit regression line
    plt.plot(x_values, regression_y_values, linewidth=3, linestyle='--', color='r', label='Regression')

    # Add titles and labels
    plt.title(graph_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    if x_ticks is None:
        x_ticks = x_values

    plt.xticks(x_ticks, rotation=x_rotation)

    if y_ticks is None:
        y_min, y_max = min(y_values), max(y_values)
        y_ticks = np.linspace(y_min, y_max, 20)
    plt.yticks(y_ticks)

    plt.grid(grid)
    plt.legend()
    plt.show()

plot_line_graph_polynomial_fit([ant.performance for ant in aco.ants_arr], x_ticks=list(range(1, len(aco.ants_arr), 10)))