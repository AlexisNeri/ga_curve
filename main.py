import lib

# List of dictionaries
FATHERS = []
SONS = []
SURVIVORS = []
# Float list
ERROR = []
# Int list
GENERATION = []


if __name__ == '__main__':
    print('Generating default curve points')
    default_x, default_y = lib.generate_default_curve_points()
    print('Generating new chromosomes')
    for chromosome in range(1000):
        FATHERS.append(lib.generate_chromosome())
    for generation in range(100):
        print('Generation #{}'.format(generation))
        for tournament in range(100):
            print('Tournament #{}'.format(tournament))
            SURVIVORS.append(lib.tournament(FATHERS.copy()))

        print('Plot curve and error from best individual from this generation')
        best_in_generation = lib.find_best_in_generation(SURVIVORS.copy())
        new_x, new_y = lib.generate_new_curve_points(best_in_generation)
        GENERATION.append(generation)
        ERROR.append(best_in_generation[-1])
        lib.plot_results(default_x, default_y, new_y, GENERATION, ERROR, generation)

        print('Substituting individuals')
        SONS = lib.reproduction(SURVIVORS.copy())
        FATHERS.clear()
        FATHERS = SONS.copy()
        SONS.clear()
        SURVIVORS.clear()
