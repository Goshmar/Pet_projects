

**Report**

Introduction to AI

Assignment 2: Accompaniment Generation

*Georgii Budnik, BS21-03*

\1. Program running manual and requirements

\-

To use the program, make sure your requirements are compatible with

the following libraries (the program is written in python 3.9):

.

.

.

matplotlib==3.6.2

music21==8.1.0

pretty-midi==0.2.9

\-

\-

After starting the program, enter the number of the track to be

launched (1, 2 or 3). These numbers correspond to “input1.mid”,

“input2.mid” and “input3.mid”, respectively (make sure they are in the

same directory).

After the work is done, the program writes the result to the "output.mid"

file and separately displays a window with a graph.

\2. General description

\-

The program accepts a melody as an input, determining with the help

of "musical" libraries the number of necessary chords, their tonality and

variety. Genes are then created, which are sequences of randomly

generated chords. With the help of a genetic algorithm and given

constraints (fitness value, "hall of fame", selection, mutation and

crossover functions), the program selects the fittest individual. The best

individual is converted to MIDI format and written along with the main

melody to the output file. Also, as a result, the program displays a

graph on which you can track the changes in the maximum and

average values of the fitness function for each generated generation.

\-

My program consists of the following consecutive blocks:

o FILES: Access to all data and files

o MUSIC THEORY PARAMETERS: Creation and generation of usable

variables for working with music theory (number and relevance

of chords, tonality, generation of suitable notes)

o GENETIC ALGORITHM PARAMETERS: Creating and calibrating

input values for the operation of the genetic algorithm

o MAIN PART: Application of all the above blocks and generation

of accompaniment according to a given melody





\3. Music theory part

\-

I read MIDI file using the “pretty-midi” library to get crucial meta data.

The velocity, resolution (ticks per beat), and duration (in seconds and

ticks) of the song will also be used when attaching the

accompaniment. The chords' number assists in creating the right

accompaniment. I also add melody notes to my data structures (note,

chord, and track classes), which aids the fitness function even more.

\-

For detecting the key of the tune, I utilized the “music21” library. The

Krumhansl-Schmuckler method is used by the library to find the most

likely key. Additionally, I create basic chords (chord lists) using the key

in accordance with the major and minor keys tables given in the

assignment.

\4. Genetic algorithm part

\-

During several excrement, I studied several methods of each of the stages

and selected the most optimal of them (which I managed to achieve when

running several options). My final genetic algorithm consists of:

o Initializing population (“def create\_population”)

o Getting initial fitness values (“fitness\_values”)

o Creating next population (“def create\_next\_population” using

*Selection*)

o Creating of additional modifications of the new population (“def make

crossover” using *Crossover* and “def make\_mutation” using *Mutation*)

o Preservation of the best individuals from the previous population (using

*Holl of fame*)

\- **Initializing population**. When creating a population, the algorithm uses

lowered notes by two octaves (harmonic sounding revealed empirically)

relative to the original melody. From the received notes, a gene is created in

which each note is duplicated

\- **Fitness calculation**. The fitness value is obtained by passing tests that have

been identified by me during my musical experience (I have been playing

drums for several years), as well as by the analytical method. The algorithm

uses hard and soft constraints, which in every possible way "praise" or "scold"

the sequence:

o Evaluating first chord with the tonic (one of the checks for harmonious

sound)

o Сhecking how common is the note (I have deduced the most

probable notes, chords and accompaniment’s melodies that can be

found for a particular key)

o Сhecking on patterns of rhythms (I received the best rhythmic patterns,

according to which the algorithm evaluates the quality of the gene)

o Сhecking on patterns of note's positions (Checking "out of bounds" of

nearby notes)





o Сhecking on variety of chords (Checking for the absence of excessive

variety of chords)

o Checking on difference between melody and accompaniment

(Check for consonance by calculating the distance between the

highest note of the accompaniment and the lowest note of the main

melody)

All changes to the fitness function were consistent with other values. The main

patterns of increasing and decreasing values were considered. Based on this,

"rewards" and "penalties" optimal for this algorithm were obtained to achieve

the maximum possible value of the fitness function.

\- **Selection**. Several gene selection methods have been considered. In the end,

I settled on the tournament system and empirically picked up a number for

the sample. The next population is generated based on the maximum "best of

three" fitness value, with each randomly compared gene being unique.

\- **Crossover**. Nearby individuals overcome the crossover process with an input

probability (“P\_CROSSOVER”). With a probability of “p\_select\_crossover”

(50%), one of two crossover methods is chosen: one-point crossover (one

random cut is made to replace a part), two-point crossover (two cuts are

made so that a gene segment is replaced).

\- **Mutation**. An individual overcomes the mutation process with an input

probability (“P\_MUTATION”). With probability “p\_mutation\_of\_chord” (1 /

“ACCOMPANIMENT\_LENGTH”), a random reselection of one chord from

harmonically suitable ones is performed.

\- **Hall of fame**. Faced with a number of generation issues, I came up with the

solution of using the Hall of Fame for 1% of the total number of genes in the

population. This helped to improve the quality of the result.

\- **Evolution conditions**. After careful selection of data, the following successful

input values were obtained:

o POPULATION\_SIZE = 1200 (Number of individuals in the population)

o P\_CROSSOVER = 0.9 (Probability of the crossover)

o P\_MUTATION = 0.1 (Probability of the mutation)

o NUMBER\_OF\_GENERATIONS = 20 (Number of generations)

o HOF\_SIZE = 12 (Hall of fame size)

\5. Result

\-

I obtained the most desirable person after evolution (with the maximum

fitness value). The person is my accompaniment, a progression of chords. Was

created a new track for accompaniment to the melody using the “pretty-

midi” library. I am able to maintain the sequence of the chords in the

accompaniment because to the resolution and delta time of each chord.

The product is prepared. The main features of the program can include:

flexible in parameters, visualization of the result, the use of a large set of





theoretical knowledge to implement genetic and music algorithms, follows

PEP8, a well-organized code structure and a full report :)

\-

To test, evaluate and create algorithms (including the selection of heuristic

values), analytics from the chart was used. The graph displays the maximum

(red) and average (green) value of the fitness function:

By fixing random values (for example, through the "random.seed" function)

and using a graph, we managed to achieve optimal results. For example,

realizing that if the graph of the average and the maximum value overlaps,

then this will mean that all values in the population are the same or almost the

same, then we should "complicate" our task for a better result.

