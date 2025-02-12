from ACO import ACO
from graphFunc.graph_util import plot_line_graph_polynomial_fit
from randomSearch import RandomSearch

path_to_sat = 'max3sat_aco\examples\SAT3.txt'

num_tests = 300
'''avg_performance = 0
avg_time = 0
best_random_perf = 0
rand_search = RandomSearch(path_to_sat)
for _ in range(num_tests):
    rand_search = RandomSearch(path_to_sat)
    best_ant, time = rand_search.initialize()
    avg_performance += best_ant.performance
    avg_time += time
    if best_random_perf < best_ant.performance:
        best_random_perf = best_ant.performance

print(f'Avg RandomSearch performance: {avg_performance / num_tests}')
print(f'Highest performance: {best_random_perf}')
print(f'Finished in {avg_time / num_tests}s')'''

avg_performance = 0
avg_time = 0
best_aco_perf = 0
aco = ACO(path_to_sat)
for _ in range(num_tests):
    aco = ACO(path_to_sat)
    best_ant, time = aco.initialize()
    avg_performance += best_ant.performance
    avg_time += time
    if best_aco_perf < best_ant.performance:
        best_aco_perf = best_ant.performance
        best_solution = best_ant.parameters
        best_aco = aco

print(f'Avg ACO performance: {avg_performance / num_tests}')
print(f'Highest performance: {best_aco_perf} {best_aco_perf / aco.total_clauses_num}')
print(f'Best performance: {best_solution}')
print(f'Finished in {avg_time / num_tests}s')

# Plotting graph
plot_line_graph_polynomial_fit(
    [ant.performance for ant in best_aco.ants_arr], 
    x_ticks=list(range(1, len(best_aco.ants_arr), 10)),
    graph_title='Performance de Cada Formiga através das Iterações',
    x_label='Iteração',
    y_label='Performance'
)

"""
Best results so far:
============= SAT3 ===============
Highest performance: 1398
Finished in 0.7010773099842481s
============= SAT2 ===============
Highest performance: 473
Finished in 0.4690119599865284s
============= SAT1 ===============
Highest performance: 269
Finished in 0.23906290998565966s
"""