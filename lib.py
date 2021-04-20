import math
import random
from matplotlib import pyplot as plt

DEFAULT_CHROMOSOME = (8, 25, 4, 45, 10, 17, 35)

figure, axis = plt.subplots(nrows=1, ncols=2)
figure.suptitle('Curve GA')
plt.ion()
axis[1].set_title("Error evolution")
axis[1].set_ylabel('Error')
axis[1].grid(True)


def generate_y(a, b, c, d, e, f, g, x):
    if c == 0:
        c += 1
    elif e == 0:
        e += 1

    return a * (b * math.sin(x / c) + d * math.cos(x / e)) + f * x - g


def generate_x(i):
    return i / 10


def generate_default_curve_points(default_chromosome=DEFAULT_CHROMOSOME):
    x = []
    y = []
    for i in range(1000):
        # Generating curve plot points for default chromosome
        x.append(generate_x(i))
        y.append(generate_y(default_chromosome[0], default_chromosome[1], default_chromosome[2], default_chromosome[3],
                            default_chromosome[4], default_chromosome[5], default_chromosome[6], x[-1]))
    return x, y


def generate_new_curve_points(new_chromosome):
    x = []
    y = []
    for i in range(1000):
        # Generating curve plot points for new chromosome
        x.append(generate_x(i))
        y.append(generate_y(new_chromosome[0], new_chromosome[1], new_chromosome[2], new_chromosome[3],
                            new_chromosome[4], new_chromosome[5], new_chromosome[6], x[-1]))
    return x, y


def plot_results(x, default_y, new_y, generation, error, current_generation):
    # Clean th curve plot
    axis[0].clear()
    axis[0].grid(True)
    axis[0].set_title("Curve adaptation")

    # Curve adaptation
    axis[0].plot(x, default_y, color='g', label='Default curve')
    axis[0].plot(x, new_y, color='r', label='Generated curve')
    axis[0].legend()

    # Error evolution
    axis[1].set_xlabel('Generation #{}'.format(current_generation))
    axis[1].plot(generation, error)

    plt.show()
    plt.pause(0.00001)


def find_best_in_generation(survivors):
    atl = []
    winner = []
    for chromosome in survivors:
        atl.append(chromosome[-1])

    best_in_generation = min(atl)

    for candidate in survivors:
        if best_in_generation == candidate[-1]:
            winner = candidate
    return winner


def generate_chromosome():
    chromosome = []
    for gen in range(7):
        chromosome.append(random.choice(range(256)))
    return chromosome


def reproduction(survivors):
    sons = []
    fathers, mothers = split_list(survivors)
    for chromosome in range(50):
        male_chromosome = fathers[chromosome]
        female_chromosome = mothers[chromosome]
        # Generating 2 sons per couple
        for j in range(2):
            slice_point = random.choice(range(7))

            # Adding additional randomness to the genes mixing
            randomizer = bool(random.getrandbits(1))
            if randomizer:
                subject_a = male_chromosome
                subject_b = female_chromosome
            else:
                subject_a = female_chromosome
                subject_b = male_chromosome
            son = subject_a[:slice_point]
            son.extend(subject_b[slice_point:])
            print('Generated son #{0}: {1} from fathers: {2} and {3}'.format(chromosome, son, male_chromosome,
                                                                             female_chromosome))
            sons.append(son)
    # Once reproduction has finished we called mutation to generate random mutations
    mutation(sons)
    return sons


def mutation(sons, mutation_factor=random.choice(range(1, 25))):
    for i in range(mutation_factor):
        individual = sons[random.choice(range(len(sons)))]
        # for j in range(mutation_factor):
        individual[random.choice(range(7))] = random.choice(range(256))


def tournament(fathers):
    # Obtaining default curve values
    default_x, default_y = generate_default_curve_points()
    participants = []
    aptitude_tag_list = []
    winner = []

    number_of_participants = random.choice(range(2, 33))

    print('Generating randomly {} participants\n'.format(number_of_participants))
    for i in range(number_of_participants):
        candidate_chromosome = fathers[random.choice(range(len(fathers)))]
        participants.append(candidate_chromosome)
    print('These are the participants: {}\n'.format(participants))

    # Calculating and appending curve error
    for candidate in participants:
        error = []
        candidate_x, candidate_y = generate_new_curve_points(candidate)
        for point in range(1000):
            error.append(abs(default_y[point] - candidate_y[point]))
        aptitude_tag = sum(error)
        aptitude_tag_list.append(aptitude_tag)
        if len(candidate) > 7:
            candidate[-1] = aptitude_tag
        else:
            candidate.append(aptitude_tag)

    # Getting winner chromosome
    print('Getting winner chromosome\n')
    winner_value = min(aptitude_tag_list)
    for candidate in participants:
        if winner_value == candidate[-1]:
            winner = candidate

    return winner


def split_list(a_list):
    half = len(a_list)//2
    return a_list[:half], a_list[half:]
