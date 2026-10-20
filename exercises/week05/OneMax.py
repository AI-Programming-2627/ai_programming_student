import pygad
import numpy as np

# Define the fitness function
def fitness_func(solution, solution_idx):
    return sum(solution)

# Define the parameters for the genetic algorithm
num_generations = 40
num_parents_mating = 10
sol_per_pop = 300
num_genes = 100

# Create an initial population
initial_population = np.random.randint(2, size=(sol_per_pop, num_genes))

# Create an instance of the GA
ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_func,
                       sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       initial_population=initial_population,
                       mutation_percent_genes=5)

# Run the genetic algorithm
ga_instance.run()

# Get the best solution
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Best solution is: %s\nwith fitness: %s" % (solution, solution_fitness))

# Plot the fitness values
ga_instance.plot_fitness()