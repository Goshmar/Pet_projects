from pretty_midi import *
from music21 import converter
from random import *
from heapq import nlargest
import matplotlib.pyplot as plt

###############################
### Budnik Georgii, BS21-03 ###
###############################

### FILES ###
number_of_file = int(input("Please, enter number of selected file: "))
input_files = ['input1.mid', 'input2.mid', 'input3.mid']
input_melody = PrettyMIDI(input_files[number_of_file - 1])
output_melody = Instrument(program=instrument_name_to_program('Acoustic Grand Piano'))

### MUSIC THEORY PARAMETERS ###
MAJOR_LAYOUT = (0, 4, 7)
MINOR_LAYOUT = (0, 3, 7)
DIM_LAYOUT = (0, 3, 6)
SUS2_LAYOUT = (0, 2, 7)
SUS4_LAYOUT = (0, 5, 7)

INPUT_NOTES = [(note.pitch, input_melody.time_to_tick(note.start),
                input_melody.time_to_tick(note.end)) for note in input_melody.instruments[0].notes]

KEY = converter.parse(input_files[number_of_file - 1]).analyze('key')
KEY_OCTAVE = converter.parse(input_files[number_of_file - 1]).analyze('key').pitches[0].octave
OCTAVE_SHIFT = -2

LENGTH = input_melody.get_end_time()
TIME_OF_CHORD = input_melody.tick_to_time(input_melody.resolution)
NUMBER_OF_CHORDS = int(input_melody.time_to_tick(LENGTH) // input_melody.resolution)
INTERVALS_OF_CHORDS = [((i * TIME_OF_CHORD), ((i + 1) * TIME_OF_CHORD)) for i in range(NUMBER_OF_CHORDS)]
VELOCITY = input_melody.instruments[0].notes[0].velocity

### GENETIC ALGORITHM PARAMETERS ###
ACCOMPANIMENT_LENGTH = NUMBER_OF_CHORDS  # gene length
POPULATION_SIZE = 1200  # number of individuals in the population
P_CROSSOVER = 0.9  # probability of the crossover
P_MUTATION = 0.1  # probability of mutation of an individual
NUMBER_OF_GENERATIONS = 20  # number of generations
HOF_SIZE = int(POPULATION_SIZE * 0.01)  # hall of fame size


# for getting useful chords
def get_progression_of_chords():
    if KEY.type == 'major':
        return [[KEY.pitches[0].midi + MAJOR_LAYOUT[i] for i in range(3)],
                [KEY.pitches[1].midi + MINOR_LAYOUT[i] for i in range(3)],
                [KEY.pitches[2].midi + MINOR_LAYOUT[i] for i in range(3)],
                [KEY.pitches[3].midi + MAJOR_LAYOUT[i] for i in range(3)],
                [KEY.pitches[4].midi + MAJOR_LAYOUT[i] for i in range(3)],
                [KEY.pitches[5].midi + MINOR_LAYOUT[i] for i in range(3)],
                [KEY.pitches[6].midi + DIM_LAYOUT[i] for i in range(3)]]
    if KEY.type == 'minor':
        return [[KEY.pitches[0].midi + MINOR_LAYOUT[i] for i in range(3)],
                [KEY.pitches[1].midi + DIM_LAYOUT[i] for i in range(3)],
                [KEY.pitches[2].midi + MAJOR_LAYOUT[i] for i in range(3)],
                [KEY.pitches[3].midi + MINOR_LAYOUT[i] for i in range(3)],
                [KEY.pitches[4].midi + MINOR_LAYOUT[i] for i in range(3)],
                [KEY.pitches[5].midi + MAJOR_LAYOUT[i] for i in range(3)],
                [KEY.pitches[6].midi + MAJOR_LAYOUT[i] for i in range(3)]]


# for shifting octaves
def make_octaves_shifting(chords, shift):
    for ind_chord in range(len(chords)):
        chord_list = [note for note in chords[ind_chord]]
        for i in range(len(chord_list)):
            chord_list[i] += shift * 12
        chords[ind_chord] = tuple(chord_list)
    return chords


# for merging accompaniment with melody and writing in the file "output.mid"
def write_merged_melody(chords):
    for i in range(NUMBER_OF_CHORDS):
        output_melody.notes.append(
            Note(velocity=VELOCITY, pitch=chords[i][0],
                 start=INTERVALS_OF_CHORDS[i][0], end=INTERVALS_OF_CHORDS[i][1])
        )
        output_melody.notes.append(
            Note(velocity=VELOCITY, pitch=chords[i][1],
                 start=INTERVALS_OF_CHORDS[i][0], end=INTERVALS_OF_CHORDS[i][1])
        )
        output_melody.notes.append(
            Note(velocity=VELOCITY, pitch=chords[i][2],
                 start=INTERVALS_OF_CHORDS[i][0], end=INTERVALS_OF_CHORDS[i][1])
        )
    input_melody.instruments.append(output_melody)
    input_melody.write(f'output.mid')


# for generating unique random list of integer numbers
def generate_sample_ints(low, high, n):
    sample = []
    seen = set()
    for _ in range(n):
        x = randint(low, high)
        while x in seen:
            x = randint(low, high)
        seen.add(x)
        sample.append(x)
    if n == 1:
        return sample[0]
    return sample


def get_fitness_value(individual):
    MINOR_CHORDS_COMBINATIONS = \
        [make_octaves_shifting([(69, 72, 76), (67, 71, 74), (62, 65, 69, 72), (62, 65, 69, 72)], OCTAVE_SHIFT),
         make_octaves_shifting([(69, 72, 76), (64, 67, 71), (67, 71, 74), (52, 65, 69)], OCTAVE_SHIFT),
         make_octaves_shifting([(69, 72, 76), (67, 71, 74), (64, 67, 71), (65, 69, 72)], OCTAVE_SHIFT),
         make_octaves_shifting([(69, 72, 76, 79), (64, 67, 71, 74), (67, 69, 71, 74), (62, 65, 69, 72)], OCTAVE_SHIFT)]
    MAJOR_CHORDS_COMBINATIONS = \
        [make_octaves_shifting([(72, 76, 79), (72, 77, 81), (71, 74, 79), (69, 72, 76)], OCTAVE_SHIFT),
         make_octaves_shifting([(72, 77, 81), (69, 72, 76), (71, 74, 79)], OCTAVE_SHIFT),
         make_octaves_shifting([(74, 77, 81), (69, 72, 76), (72, 76, 79), (71, 74, 79)], OCTAVE_SHIFT),
         make_octaves_shifting([(72, 76, 79), (71, 74, 79), (69, 72, 76), (67, 71, 74)], OCTAVE_SHIFT),
         make_octaves_shifting([(69, 72, 76), (67, 71, 74), (72, 76, 79), (71, 74, 79)], OCTAVE_SHIFT)]
    CHORDS_COMBINATIONS = {'minor': MINOR_CHORDS_COMBINATIONS,
                           'major': MAJOR_CHORDS_COMBINATIONS}
    value = 0

    if ACCOMPANIMENT_LENGTH % 2:
        individual.append(individual[-1])

    # evaluating first chord with the tonic

    if individual[0][0] == KEY_OCTAVE:
        value += 15

    # checking how common is the note
    for ind_chord in range(ACCOMPANIMENT_LENGTH):
        is_not_comb = True
        for comb in CHORDS_COMBINATIONS[KEY.type]:
            if individual[ind_chord] in comb:
                value += len(comb) + 2
                is_not_comb = False
        for note in individual[ind_chord]:
            for ind_comb in range(len(CHORDS_COMBINATIONS[KEY.type])):
                for ind_comb_chord in range(len(CHORDS_COMBINATIONS[KEY.type][ind_comb])):
                    if note in CHORDS_COMBINATIONS[KEY.type][ind_comb][ind_comb_chord]:
                        value += 2
                        is_not_comb = False
        if is_not_comb:
            value -= 20
            break

        if ind_chord < ACCOMPANIMENT_LENGTH - 4 and [individual[ind_chord], individual[ind_chord + 1],
                                                     individual[ind_chord + 2], individual[ind_chord + 3]] in \
                CHORDS_COMBINATIONS[KEY.type]:
            value += 40
        if ind_chord < ACCOMPANIMENT_LENGTH - 3 and [individual[ind_chord], individual[ind_chord + 1],
                                                     individual[ind_chord + 2]] in CHORDS_COMBINATIONS[KEY.type]:
            value += 30

    # checking on patterns of rhythms
    ind_chord = 0
    while ind_chord <= ACCOMPANIMENT_LENGTH - 4:
        if individual[ind_chord] == individual[ind_chord + 3]:
            value += 10
        if individual[ind_chord] == individual[ind_chord + 2]:
            value -= 10
        if individual[ind_chord] != individual[ind_chord + 2]:
            if individual[ind_chord] == individual[ind_chord + 1] and \
                    individual[ind_chord + 2] == individual[ind_chord + 3]:
                value += 35
            elif individual[ind_chord] == individual[ind_chord + 1] or \
                    individual[ind_chord + 2] == individual[ind_chord + 3]:
                value += 10
            else:
                value += 5

        # checking on patterns of note's positions
        for ind_shift in range(1, 4):
            dif_notes = min(individual[ind_chord + ind_shift]) - max(individual[ind_chord])
            if max(individual[ind_chord + ind_shift]) > max(individual[ind_chord]):
                dif_notes = (max(individual[ind_chord]) - min(individual[ind_chord + 1]))
            if dif_notes < 0:
                value -= 30
            elif dif_notes < 1:
                value -= 25
            elif dif_notes < 2:
                value -= 20
            elif dif_notes < 3:
                value -= 18
            elif dif_notes < 4:
                value -= 15
        ind_chord += 4

    # checking on variety of chords
    value += ((ACCOMPANIMENT_LENGTH // 2) - len(set(individual))) * 2

    # checking on difference between melody and accompaniment
    if max([max(note) for note in individual]) > min([note[0] for note in INPUT_NOTES]) - 2:
        value -= 25
    return value


def create_individual():
    chords = make_octaves_shifting(get_progression_of_chords(), OCTAVE_SHIFT)
    individual_chords = [chords[randint(0, len(chords) - 1)] for _ in range(ACCOMPANIMENT_LENGTH // 2)]
    individual = []
    for elem in individual_chords:
        individual += [elem, elem]
    return individual


def create_population():
    return [create_individual() for _ in range(POPULATION_SIZE)]


# selection, tournament selection best of (selection_number)
def create_next_population(population, selection_number):
    next_population = []
    for _ in range(POPULATION_SIZE - HOF_SIZE):
        tournament = generate_sample_ints(0, POPULATION_SIZE - 1, selection_number)
        tournament_fitness_values = [get_fitness_value(population[tournament[i]]) for i in range(selection_number)]
        index_of_max = tournament[tournament_fitness_values.index(max(tournament_fitness_values))]
        next_population.append(population[index_of_max])
    return next_population


# crossover, selects 'one-point' or 'two-point' with the probability (p_select_crossover)
def make_crossover(accompaniment_1, accompaniment_2):
    p_select_crossover = 0.5
    if random() < p_select_crossover:
        cut_1, cut_2 = sorted(generate_sample_ints(2, ACCOMPANIMENT_LENGTH - 3, 2))
        accompaniment_1[cut_1:cut_2], accompaniment_2[cut_1:cut_2] = \
            accompaniment_2[cut_1:cut_2], accompaniment_1[cut_1:cut_2]
    else:
        cut = randint(2, ACCOMPANIMENT_LENGTH - 3)
        accompaniment_1[cut:], accompaniment_2[cut:] = accompaniment_2[cut:], accompaniment_1[cut:]


# mutation, change 'note' with the probability (p_mutation_of_chord)
def make_mutation(accompaniment):
    p_mutation_of_chord = 1.0 / ACCOMPANIMENT_LENGTH
    for i in range(ACCOMPANIMENT_LENGTH):
        if random() < p_mutation_of_chord:
            mutated_chord = accompaniment[i]
            while mutated_chord == accompaniment[i]:
                mutated_chord = make_octaves_shifting(get_progression_of_chords(),
                                                      OCTAVE_SHIFT)[generate_sample_ints(0, 6, 1)]
            accompaniment[i] = mutated_chord


# draw the graph (max and mean fitness values of each generation)
# max values - red, mean values - green
def draw_graph(max_list, mean_list):
    plt.plot(max_list, color='red')
    plt.plot(mean_list, color='green')
    plt.xlabel('Generation')
    plt.ylabel('Max/mean fitness value')
    plt.show()


### MAIN PART ###

print("In progress...")
population = create_population()
counter_of_generations = 0

fitness_values = list(map(get_fitness_value, population))
max_fitness_value = []  # values in a current generation
mean_fitness_value = []  # values in a current generation

for _ in range(NUMBER_OF_GENERATIONS):
    next_population = create_next_population(population, 3)
    # crossover
    for i in range(POPULATION_SIZE - HOF_SIZE - 1):
        if random() < P_CROSSOVER:
            make_crossover(next_population[i], next_population[i + 1])

    # mutation
    for accompaniment in next_population:
        if random() < P_MUTATION:
            make_mutation(accompaniment)

    # hall of fame
    next_population += nlargest(HOF_SIZE, population)

    fitness_values = list(map(get_fitness_value, next_population))
    best_index = fitness_values.index(max(fitness_values))
    population = next_population

    max_fitness_value.append(max(fitness_values))
    mean_fitness_value.append(round(sum(fitness_values) / POPULATION_SIZE, 2))
    counter_of_generations += 1

    print(f'Generation №{counter_of_generations}: ', end='')
    print(f'Max fitness value = {max_fitness_value[-1]}; Avg fitness value = {mean_fitness_value[-1]}')
    print('Best accompaniment = ', population[best_index], '\n')

write_merged_melody(population[fitness_values.index(max(fitness_values))])
draw_graph(max_fitness_value, mean_fitness_value)
