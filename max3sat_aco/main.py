from ACO import ACO

aco = ACO()
best_ant, time = aco.initialize()

print(aco.graph)

print(str(best_ant))
print(f'Finished in {time}s')