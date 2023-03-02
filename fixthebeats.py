import py_midicsv as pm
import re
import sys
import csv
import json


file_name = sys.argv[1]

#Building a dictionary of notes and corresponding enharmonic notes (between octaves -1 and 9 inclusively)
#and their numeric counterpart (based on the article: Mathematics 2019, 7, 19; doi:10.3390/math7010019)
notes_numbers = {"A0":21, "A#0":22, "Bb0":22, "B0":23}
for i in range(1,10):
    notes_numbers["C" + str(i)] = 12 + 12*i
    notes_numbers["B#" + str(i)] = 12 + 12*i

    notes_numbers["C#" + str(i)] = 13 + 12*i
    notes_numbers["Db" + str(i)] = 13 + 12*i

    notes_numbers["D" + str(i)] = 14 + 12*i

    notes_numbers["D#" + str(i)] = 15 + 12*i
    notes_numbers["Eb" + str(i)] = 15 + 12*i

    notes_numbers["E" + str(i)] = 16 + 12*i
    notes_numbers["Fb" + str(i)] = 16 + 12*i

    notes_numbers["F" + str(i)] = 17 + 12*i
    notes_numbers["E#" + str(i)] = 17 + 12*i

    notes_numbers["F#" + str(i)] = 18 + 12*i
    notes_numbers["Gb" + str(i)] = 18 + 12*i

    notes_numbers["G" + str(i)] = 19 + 12*i

    notes_numbers["G#" + str(i)] = 20 + 12*i
    notes_numbers["Ab" + str(i)] = 20 + 12*i

    notes_numbers["A" + str(i)] = 21 + 12*i

    notes_numbers["A#" + str(i)] = 22 + 12*i
    notes_numbers["Bb" + str(i)] = 22 + 12*i

    notes_numbers["B" + str(i)] = 23 + 12*i
    notes_numbers["Cb" + str(i)] = 23 + 12*i

list_notes_numbers_keys = list(notes_numbers.keys())
list_notes_numbers_values = list(notes_numbers.values())

#Remove the notes above the Midi note number 127 from the dictionary generated above
deleted_notes = ["Cb9", "B9", "Bb9", "A#9", "A9", "Ab9", "G#9"]
for deleted_note in deleted_notes:
    del notes_numbers[deleted_note]

#Notes for the 30-note Grand Illusions music box (F scale), according to musicboxmaniacs.com
#Only the notes between A5 and F6 could also be selected, as there are no missing accidentals in this interval (1.5 octaves).
music_box_notes = ["F3", "G3",	"A4", "A#4", "B4", "C4", "D4", "E4", "F4",
"G4", "A5", "A#5", "B5", "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5",
"A6", "C6", "C#6", "D6", "D#6", "E6", "F6", "G6"]


def get_instrument_notes(lowest_note, highest_note):
    lowest_MIDI_note = notes_numbers[lowest_note]
    highest_MIDI_note = notes_numbers[highest_note]
    return list(range(lowest_MIDI_note, highest_MIDI_note+1))

#Getting the lowest and highest notes of the instrument, along with the
#tempo_multiplier (if supplied). A tempo_multiplier of 2 will result
#in 50% tempo reduction. The tempo_multiplier defaults at one (unchanged tempo)
#The order in which the parameters are sent from PHP to python is the following.
#Please note that the only argvs that should be present in all exec commands are
#argv[0] and argv[1], hence the code below.
#argv[0] = python call
#argv[1] = ".mid" file path
#argv[2] = instrument's minimal note (ex: E2 for guitar)
#argv[3] = instrument's maximal note (ex: G#4 for guitar)
#argv[4] = tempo_multiplier (any float or integer over zero, within reason)
#argv[5] = semitone_lock setting, which only allows for different octave modifications
#(no semitone shifts allowed)
tempo_multiplier = 1
lowest_note = None
highest_note = None
semitone_lock = False

if len(sys.argv) > 2:
    if sys.argv[2] in list_notes_numbers_keys and sys.argv[3] in list_notes_numbers_keys:
        lowest_note = sys.argv[2]
        highest_note = sys.argv[3]
        instrument_MIDI_notes = get_instrument_notes(lowest_note, highest_note)
    else:
        instrument_MIDI_notes = sorted([notes_numbers[note] for note in music_box_notes])

    for argv in sys.argv[2:]:
        if argv == "semitone_lock":
            semitone_lock = True
        else:
            try:
                tempo_multiplier = float(argv.strip())
            except:
                pass
else:
    instrument_MIDI_notes = sorted([notes_numbers[note] for note in music_box_notes])


#A list of notes in the piece (notes_in_piece) is populated with the MIDI note values
# of the entries containing the " Note_on" label in the csv string.
notes_in_piece = []
csv_string = pm.midi_to_csv(file_name)
for row in csv.reader(csv_string):
    if row[2].strip()[:7] == "Note_on":
        notes_in_piece.append(int(row[4].strip()))

#Screening through the lists of values derived from the "notes_numbers" dictionary
#of MIDI note numbers until the indices of the average note in the piece and the average note
#in the playable notes of the instrument within the list are found. From these indices,
#the note in letter format is found by indexing the list of keys derived from the
#"notes_numbers" dictionary, and its last character is the octave of the corresponding note (ex: 5 in C#5).
number_of_notes_in_piece = len(notes_in_piece)
average_note_in_piece = int(sum(notes_in_piece)/len(notes_in_piece))
average_note_instrument = int(sum(instrument_MIDI_notes)/len(instrument_MIDI_notes))
for value in list_notes_numbers_values:
    if value == average_note_in_piece and value == average_note_instrument:
        index_value = list_notes_numbers_values.index(value)
        octave_of_average_note_instrument = int(list_notes_numbers_keys[index_value][-1])
    elif value == average_note_in_piece:
        index_value = list_notes_numbers_values.index(value)
        octave_of_average_note_in_piece = int(list_notes_numbers_keys[index_value][-1])
    elif value == average_note_instrument:
        index_value = list_notes_numbers_values.index(value)
        octave_of_average_note_instrument = int(list_notes_numbers_keys[index_value][-1])

#Adjusting all the notes in the piece by the average difference in octaves between the piece and the instrument range
octave_difference_between_piece_and_instrument = octave_of_average_note_in_piece - octave_of_average_note_instrument
if octave_difference_between_piece_and_instrument != 0:
    for i in range(len(notes_in_piece)):
        notes_in_piece[i] = notes_in_piece[i] - octave_difference_between_piece_and_instrument*12

#Calculating the percentage of notes in the piece that are in the instrument's range
notes_within_range_of_instrument = 0
for i in range(len(notes_in_piece)):
    if notes_in_piece[i] in instrument_MIDI_notes:
        notes_within_range_of_instrument+=1

percentage_of_notes_within_range_of_instrument = round(notes_within_range_of_instrument/number_of_notes_in_piece*100, 2)

optimal_modifier = 0
if semitone_lock == False:
    #Incrementally modifying all notes by a midi scale unit (either increasing or reducing by up to 12 units) and calculating
    #the modified_percentage_of_notes_within_range_of_instrument at every value of the modifier i. The optimal value of the
    #modifier will be applied to every note.
    modified_percentage_of_notes_within_range_of_instrument = percentage_of_notes_within_range_of_instrument
    for i in [-12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        modified_notes_within_range_of_instrument = 0
        for j in range(len(notes_in_piece)):
            modified_note = notes_in_piece[j] + i
            if modified_note in instrument_MIDI_notes:
                modified_notes_within_range_of_instrument+=1
        modified_percentage_of_notes_within_range_of_instrument = round(modified_notes_within_range_of_instrument/number_of_notes_in_piece*100, 2)
        if modified_percentage_of_notes_within_range_of_instrument > percentage_of_notes_within_range_of_instrument:
            percentage_of_notes_within_range_of_instrument = modified_percentage_of_notes_within_range_of_instrument
            optimal_modifier = i

#Applying the optimal_modifier to every note and further modifications to the octave of the note if it is not
#within the range of notes that can be played by the instrument. Any outliers are recorded in the lists:
#outlier_notes_with_tags (notes that could not be adjusted successfully) and
#outlier_modifications_with_tags (notes that have been further shifted by a given number of octaves so that
#they are playable by the instrument).
modified_notes_in_piece = []
outlier_notes_with_tags = []
maximal_note_in_instrument_range = max(instrument_MIDI_notes)
minimal_note_in_instrument_range = min(instrument_MIDI_notes)

for i in range(len(notes_in_piece)):
    modified_note = notes_in_piece[i] + optimal_modifier
    if modified_note in instrument_MIDI_notes:
        modified_notes_in_piece.append(modified_note)
    elif modified_note < minimal_note_in_instrument_range:
        for j in range(1,6):
            new_modified_note = modified_note + j*12
            if new_modified_note in instrument_MIDI_notes:
                modified_notes_in_piece.append([notes_in_piece[i], new_modified_note, i, j, "i-" + str(j)])
                outlier_notes_with_tags.append([notes_in_piece[i], new_modified_note, i, j, "i-" + str(j)])
                break
            #If the note is still outside of the range of notes playable by the instrument,
            #the note will be added to the list of outlier_notes_with_tags
            #with the label "outlier".
            elif j == 5 and new_modified_note not in instrument_MIDI_notes:
                modified_notes_in_piece.append([notes_in_piece[i], modified_note, i, 0, "outlier"])
                outlier_notes_with_tags.append([notes_in_piece[i], modified_note, i, 0, "outlier"])
    #If the modified note above the range of the instrument, it will be lowered by
    #up to 5 octaves until it is among the playable notes of the instrument. The comment
    #in the meta text tag will read: "downwards arrow" + "number of octaves" + "OCT".
    elif modified_note > maximal_note_in_instrument_range:
        for j in range(1,6):
            new_modified_note = modified_note - j*12
            if new_modified_note in instrument_MIDI_notes:
                modified_notes_in_piece.append([notes_in_piece[i], new_modified_note, i, -j, "d-" + str(j)])
                outlier_notes_with_tags.append([notes_in_piece[i], new_modified_note, i, -j, "d-" + str(j)])
                break
            elif j == 5 and new_modified_note not in instrument_MIDI_notes:
                modified_notes_in_piece.append([notes_in_piece[i], modified_note, i, 0, "outlier"])
                outlier_notes_with_tags.append([notes_in_piece[i], modified_note, i, 0, "outlier"])
    #If the note is in between the maximal and minimal notes of the instrument's range (some sharps
    #and one natural note are missing) it will be either lowered or increased by up to 5 octaves,
    #until it is among the playable notes of the instrument. The comment in the meta text tag will read:
    #"i" or "d" + "number of octaves" + "oct".
    elif modified_note not in instrument_MIDI_notes:
        for j in range(1,6):
            new_modified_note = modified_note + j*12
            if new_modified_note in instrument_MIDI_notes:
                modified_notes_in_piece.append([notes_in_piece[i], new_modified_note, i, j, "i-" + str(j)])
                outlier_notes_with_tags.append([notes_in_piece[i], new_modified_note, i, j, "i-" + str(j)])
                break
            new_modified_note = modified_note - j*12
            if new_modified_note in instrument_MIDI_notes:
                modified_notes_in_piece.append([notes_in_piece[i], new_modified_note, i, -j, "d-" + str(j)])
                outlier_notes_with_tags.append([notes_in_piece[i], new_modified_note, i, -j, "d-" + str(j)])
                break
            elif j == 5 and new_modified_note not in instrument_MIDI_notes:
                modified_notes_in_piece.append([notes_in_piece[i], modified_note, i, 0, "outlier"])
                outlier_notes_with_tags.append([notes_in_piece[i], modified_note, i, 0, "outlier"])


#The last "list" instance in the list "modified_notes_in_piece" will be determined
#by cycling through the list and updating the latest index at which a list is observed.
list_instances_in_modified_notes_in_piece = []
for i in range(len(modified_notes_in_piece)):
    if type(modified_notes_in_piece[i]) == list:
        list_instances_in_modified_notes_in_piece.append(i)

#Only do the following "if" statement if there are modified notes
#(list instances) in the list "modified_notes_in_piece"
if list_instances_in_modified_notes_in_piece != []:


    #GENERATING THE CSV AND MIDI FILES (WITHOUT ADDITIONAL OUTLIERS)

    #The csv_string will be updated with all the modifications made to the notes of the piece.
    #"Lyric_t" tags will annotate the music scoresheets in the ".mid" files with the
    #"modified_with_tags" suffix. The counters "counter_note_on" and "counter_note_off" are
    #used to avoid assigning duplicate tags to notes.
    with open("modified song without tags.csv", "w+") as output_csv:
        writer = csv.writer(output_csv)
        counter_note_on = 0
        open_notes_on = []
        for row in csv.reader(csv_string):
            if row[2].strip()[:7] == "Note_on":
                note_in_csv_string = int(row[4].strip())
                for i in range(counter_note_on, len(notes_in_piece)):
                    if (note_in_csv_string == notes_in_piece[i]+
                    octave_difference_between_piece_and_instrument*12 - optimal_modifier):
                        open_notes_on.append(modified_notes_in_piece[i])
                        #Applying the tempo_multiplier to the timestamps (default value of 1).
                        #A tempo_multiplier of 2 will result in 50% tempo.
                        if i < len(notes_in_piece)-2:
                            counter_note_on = i+1
                        timestamp = int(row[1])
                        new_timestamp = int(timestamp*tempo_multiplier)
                        row[1] = new_timestamp
                        if type(modified_notes_in_piece[i]) == int:
                            row[4] = " " + str(modified_notes_in_piece[i])
                            writer.writerow(row)
                            break
                        elif type(modified_notes_in_piece[i]) == list and modified_notes_in_piece[i][2] == i:
                            row[4] = " " + str(modified_notes_in_piece[i][1])
                            writer.writerow(row)
                            break

            #Here, "Lyric_t" tags are not appended to the csv_string, as they have already been added
            #to the corresponding "Note_on". The note in the current "Note_off" row is compared to
            #all of the open "Note_on" notes within the "open_notes_on" list. The matching notes are
            #updated within the row ("open_notes_on" derives from the "modified_notes_in_piece", so
            #if the notes weren't modified other than the overall changes in octaves and semitones,
            #the value will be of the type "int". Alternatively, if further changes in octave have
            #been individually applied to the note, it will be of the type "list", the element [0]
            #being the original note after the overall changes in octaves and semitones and the
            #element [1] will be the value of the note after individualized octave adjustments).
            #Once the row has been written in the "csv" file, the note is removed from the "open_note_on" list.
            elif row[2].strip()[:8] == "Note_off":
                note_in_csv_string = int(row[4].strip())
                timestamp = int(row[1])
                new_timestamp = int(timestamp*tempo_multiplier)
                row[1] = new_timestamp
                for j in range(len(open_notes_on)):
                    if (type(open_notes_on[j]) == list and note_in_csv_string == open_notes_on[j][0] +
                    octave_difference_between_piece_and_instrument*12 - optimal_modifier):
                        row[4] = " " + str(open_notes_on[j][1])
                        writer.writerow(row)
                        open_notes_on.pop(j)
                        break
                    elif (type(open_notes_on[j]) == int and note_in_csv_string == open_notes_on[j] +
                    octave_difference_between_piece_and_instrument*12 - optimal_modifier):
                        row[4] = " " + str(open_notes_on[j])
                        writer.writerow(row)
                        open_notes_on.pop(j)
                        break
            else:
                #Applying the tempo_multiplier to the timestamps (default value of 1).
                #A tempo_multiplier of 2 will result in 50% tempo.
                timestamp = int(row[1])
                new_timestamp = int(timestamp*tempo_multiplier)
                row[1] = new_timestamp
                writer.writerow(row)

    #Open the "_modified.csv" file that was just written in reading mode
    #and convert it to the corresponding MIDI file using the py_midicsv module.
    with open("modified song without tags.csv", "r") as new_csv_string:
        midi_object = pm.csv_to_midi(new_csv_string)
        with open("modified song without tags.mid", "wb") as output_file:
            midi_writer = pm.FileWriter(output_file)
            midi_writer.write(midi_object)

    #Repeat the process while adding tags at the outlier notes(whether they were further increased or decreased in octaves or not).
    #If these outlier notes were further modified in octaves, the "Lyric_t" tag would mention "i" for increase or "d" for decrease,
    #followed by the number of octaves. For example, "i1oct" indicates that the note, after its initial octave modification and
    #optimal_modifier application, was further increased by 1 octave in order be within the range of the instrument playable notes.
    with open("modified song with tags.csv", "w+") as output_csv:
        writer = csv.writer(output_csv)
        counter_note_on = 0
        open_notes_on = []
        for row in csv.reader(csv_string):
            if row[2].strip()[:7] == "Note_on":
                note_in_csv_string = int(row[4].strip())
                for i in range(counter_note_on, len(notes_in_piece)):
                    if (note_in_csv_string == notes_in_piece[i]+
                    octave_difference_between_piece_and_instrument*12 - optimal_modifier):
                        open_notes_on.append(modified_notes_in_piece[i])
                        #Applying the tempo_multiplier to the timestamps (default value of 1).
                        #A tempo_multiplier of 2 will result in 50% tempo.
                        if i < len(notes_in_piece)-2:
                            counter_note_on = i+1
                        timestamp = int(row[1])
                        new_timestamp = int(timestamp*tempo_multiplier)
                        row[1] = new_timestamp
                        if type(modified_notes_in_piece[i]) == int:
                            row[4] = " " + str(modified_notes_in_piece[i])
                            writer.writerow(row)
                            break
                        #Lyric_t meta-tags are added to the csv_string, which will appear in the annotated MIDI file.
                        #elif type(modified_notes_in_piece[i]) == list and modified_notes_in_piece[i][2] == i:
                        elif type(modified_notes_in_piece[i]) == list:
                            row[4] = " " + str(modified_notes_in_piece[i][1])
                            writer.writerow(row)
                            track = int(row[0])
                            time = int(row[1])
                            writer.writerow([track, time, "Text_t", modified_notes_in_piece[i][4]])
                            break
            #Here, "Lyric_t" tags are not appended to the csv_string, as they have already been added
            #to the corresponding "Note_on".
            elif row[2].strip()[:8] == "Note_off":
                note_in_csv_string = int(row[4].strip())
                timestamp = int(row[1])
                new_timestamp = int(timestamp*tempo_multiplier)
                row[1] = new_timestamp
                for j in range(len(open_notes_on)):
                    if (type(open_notes_on[j]) == list and note_in_csv_string == open_notes_on[j][0] +
                    octave_difference_between_piece_and_instrument*12 - optimal_modifier):
                        row[4] = " " + str(open_notes_on[j][1])
                        writer.writerow(row)
                        open_notes_on.pop(j)
                        break
                    elif (type(open_notes_on[j]) == int and note_in_csv_string == open_notes_on[j] +
                    octave_difference_between_piece_and_instrument*12 - optimal_modifier):
                        row[4] = " " + str(open_notes_on[j])
                        writer.writerow(row)
                        open_notes_on.pop(j)
                        break
            else:
                #Applying the tempo_multiplier to the timestamps (default value of 1).
                #A tempo_multiplier of 2 will result in 50% tempo.
                timestamp = int(row[1])
                new_timestamp = int(timestamp*tempo_multiplier)
                row[1] = new_timestamp
                writer.writerow(row)

    #Open the "_modified.csv" file that was just written in reading mode
    #and convert it to the corresponding MIDI file using the py_midicsv module.
    with open("modified song with tags.csv", "r") as new_csv_string:
        midi_object = pm.csv_to_midi(new_csv_string)
        with open("modified song with tags.mid", "wb") as output_file:
            midi_writer = pm.FileWriter(output_file)
            midi_writer.write(midi_object)


    #GENERATING THE CSV AND MIDI FILES (WITH INFERRED CHANGES MADE TO UP TO
    #THREE NOTES BASED ON THE MODIFICATIONS OF THE FLANKING NOTES)

    ditto_and_modified_notes_in_piece = modified_notes_in_piece.copy()

    #When looping through every note of the "ditto_and_modified_notes_in_piece" list, if two identically modified notes (list elements)
    #are separated by at most three unmodified notes (integer elements), the same octave modifications are then applied
    #to these notes by inference. The inferred annotations are parenthesized for clarity.
    for i in range(len(ditto_and_modified_notes_in_piece)-4):
        if (type(ditto_and_modified_notes_in_piece[i]) == list
        and type(ditto_and_modified_notes_in_piece[i+1]) == int and type(ditto_and_modified_notes_in_piece[i+2]) == list):
            if ditto_and_modified_notes_in_piece[i][4] == ditto_and_modified_notes_in_piece[i+2][4]:
                new_modified_note = ditto_and_modified_notes_in_piece[i+1] + ditto_and_modified_notes_in_piece[i][3]*12
                if new_modified_note in instrument_MIDI_notes:
                    ditto_and_modified_notes_in_piece[i+1] = [notes_in_piece[i+1], new_modified_note, i+1, ditto_and_modified_notes_in_piece[i][3], "(" + ditto_and_modified_notes_in_piece[i][4] + ")"]
                else:
                    modified_note = notes_in_piece[i+1] + optimal_modifier
                    ditto_and_modified_notes_in_piece[i+1] = [notes_in_piece[i+1], modified_note, i+1, 0, "outlier"]
            #A similar approach is followed if a inferred modification tag (without parentheses)
            #is identical to the modification tag of a modified note two notes away
            elif ditto_and_modified_notes_in_piece[i][4][1:-1] == ditto_and_modified_notes_in_piece[i+2][4]:
                new_modified_note = ditto_and_modified_notes_in_piece[i+1] + ditto_and_modified_notes_in_piece[i][3]*12
                if new_modified_note in instrument_MIDI_notes:
                    ditto_and_modified_notes_in_piece[i+1] = [notes_in_piece[i+1], new_modified_note, i+1, ditto_and_modified_notes_in_piece[i][3], ditto_and_modified_notes_in_piece[i][4]]
                else:
                    modified_note = notes_in_piece[i+1] + optimal_modifier
                    ditto_and_modified_notes_in_piece[i+1] = [notes_in_piece[i+1], modified_note, i+1, 0, "outlier"]

        elif (type(ditto_and_modified_notes_in_piece[i]) == list
        and type(ditto_and_modified_notes_in_piece[i+1]) == int and type(ditto_and_modified_notes_in_piece[i+3]) == list):
            if ditto_and_modified_notes_in_piece[i][4] == ditto_and_modified_notes_in_piece[i+3][4]:
                new_modified_note = ditto_and_modified_notes_in_piece[i+1] + ditto_and_modified_notes_in_piece[i][3]*12
                if new_modified_note in instrument_MIDI_notes:
                    ditto_and_modified_notes_in_piece[i+1] = [notes_in_piece[i+1], new_modified_note, i+1, ditto_and_modified_notes_in_piece[i][3], "(" + ditto_and_modified_notes_in_piece[i][4] + ")"]
                else:
                    modified_note = notes_in_piece[i+1] + optimal_modifier
                    ditto_and_modified_notes_in_piece[i+1] = [notes_in_piece[i+1], modified_note, i+1, 0, "outlier"]
            #A similar approach is followed if a inferred modification tag (without parentheses)
            #is identical to the modification tag of a modified note three notes away
            elif ditto_and_modified_notes_in_piece[i][4][1:-1] == ditto_and_modified_notes_in_piece[i+3][4]:
                new_modified_note = ditto_and_modified_notes_in_piece[i+1] + ditto_and_modified_notes_in_piece[i][3]*12
                if new_modified_note in instrument_MIDI_notes:
                    ditto_and_modified_notes_in_piece[i+1] = [notes_in_piece[i+1], new_modified_note, i+1, ditto_and_modified_notes_in_piece[i][3], ditto_and_modified_notes_in_piece[i][4]]
                else:
                    modified_note = notes_in_piece[i+1] + optimal_modifier
                    ditto_and_modified_notes_in_piece[i+1] = [notes_in_piece[i+1], modified_note, i+1, 0, "outlier"]
        elif (type(ditto_and_modified_notes_in_piece[i]) == list
        and type(ditto_and_modified_notes_in_piece[i+1]) == int and type(ditto_and_modified_notes_in_piece[i+4]) == list):
            if ditto_and_modified_notes_in_piece[i][4] == ditto_and_modified_notes_in_piece[i+4][4]:
                new_modified_note = ditto_and_modified_notes_in_piece[i+1] + ditto_and_modified_notes_in_piece[i][3]*12
                if new_modified_note in instrument_MIDI_notes:
                    ditto_and_modified_notes_in_piece[i+1] = [notes_in_piece[i+1], new_modified_note, i+1, ditto_and_modified_notes_in_piece[i][3], "(" + ditto_and_modified_notes_in_piece[i][4] + ")"]
                else:
                    modified_note = notes_in_piece[i+1] + optimal_modifier
                    ditto_and_modified_notes_in_piece[i+1] = [notes_in_piece[i+1], modified_note, i+1, 0, "outlier"]


    #The following code will apply modifications by inference to the last unmodified notes
    #of the piece that may have been overlooked, as the previous "for i in range(len(ditto_and_modified_notes_in_piece)-4)"
    #look ended before the end to accomodate for an incrementation of the index by up to four units. The code
    #is very similar to the code above, but proceeds in reverse order and the loop breaks when the label of the next
    #analyzed note (i-1) starts with an opening parenthesis (as in "(i-1)"), as any further integers have already
    #been modified by inference.

    #The last "int" instance in the list "modified_notes_in_piece" will be determined
    #by cycling through the list and updating the latest index at which an integer is observed.
    last_int_instances_in_ditto_and_modified_notes_in_piece = []
    for i in range(len(ditto_and_modified_notes_in_piece)-1, len(ditto_and_modified_notes_in_piece)-4, -1):
        if type(ditto_and_modified_notes_in_piece[i]) == int:
            last_int_instances_in_ditto_and_modified_notes_in_piece.append(i)


    if last_int_instances_in_ditto_and_modified_notes_in_piece != []:
        for i in range(list_instances_in_modified_notes_in_piece[-1], -1, -1):
            if i > 0 and type(ditto_and_modified_notes_in_piece[i-1]) == list and ditto_and_modified_notes_in_piece[i-1][4][0] == "(":
                break
            elif (type(ditto_and_modified_notes_in_piece[i]) == list
            and type(ditto_and_modified_notes_in_piece[i-1]) == int and type(ditto_and_modified_notes_in_piece[i-2]) == list):
                if ditto_and_modified_notes_in_piece[i][4] == ditto_and_modified_notes_in_piece[i-2][4]:
                    new_modified_note = ditto_and_modified_notes_in_piece[i-1] + ditto_and_modified_notes_in_piece[i][3]*12
                    if new_modified_note in instrument_MIDI_notes and ditto_and_modified_notes_in_piece[i][4][0] != "(":
                        ditto_and_modified_notes_in_piece[i-1] = [notes_in_piece[i-1], new_modified_note, i-1, ditto_and_modified_notes_in_piece[i][3], "(" + ditto_and_modified_notes_in_piece[i][4] + ")"]
                    elif new_modified_note in instrument_MIDI_notes and ditto_and_modified_notes_in_piece[i][4][0] == "(":
                        ditto_and_modified_notes_in_piece[i-1] = [notes_in_piece[i-1], new_modified_note, i-1, ditto_and_modified_notes_in_piece[i][3], ditto_and_modified_notes_in_piece[i][4]]
                    else:
                        modified_note = notes_in_piece[i-1] + optimal_modifier
                        ditto_and_modified_notes_in_piece[i-1] = [notes_in_piece[i-1], modified_note, i-1, 0, "outlier"]
                #A similar approach is followed if an inferred modification tag (without parentheses)
                #is identical to the modification tag of a modified note two notes away
                elif ditto_and_modified_notes_in_piece[i][4] == ditto_and_modified_notes_in_piece[i-2][4][1:-1]:
                    new_modified_note = ditto_and_modified_notes_in_piece[i-1] + ditto_and_modified_notes_in_piece[i][3]*12
                    if new_modified_note in instrument_MIDI_notes and ditto_and_modified_notes_in_piece[i][4][0] != "(":
                        ditto_and_modified_notes_in_piece[i-1] = [notes_in_piece[i-1], new_modified_note, i-1, ditto_and_modified_notes_in_piece[i][3], "(" + ditto_and_modified_notes_in_piece[i][4] + ")"]
                    elif new_modified_note in instrument_MIDI_notes and ditto_and_modified_notes_in_piece[i][4][0] == "(":
                        ditto_and_modified_notes_in_piece[i-1] = [notes_in_piece[i-1], new_modified_note, i-1, ditto_and_modified_notes_in_piece[i][3], ditto_and_modified_notes_in_piece[i][4]]
                    else:
                        modified_note = notes_in_piece[i-1] + optimal_modifier
                        ditto_and_modified_notes_in_piece[i-1] = [notes_in_piece[i-1], modified_note, i-1, 0, "outlier"]

            elif (type(ditto_and_modified_notes_in_piece[i]) == list
            and type(ditto_and_modified_notes_in_piece[i-1]) == int and type(ditto_and_modified_notes_in_piece[i-3]) == list):
                if ditto_and_modified_notes_in_piece[i][4] == ditto_and_modified_notes_in_piece[i-3][4]:
                    new_modified_note = ditto_and_modified_notes_in_piece[i-1] + ditto_and_modified_notes_in_piece[i][3]*12
                    if new_modified_note in instrument_MIDI_notes and ditto_and_modified_notes_in_piece[i][4][0] != "(":
                        ditto_and_modified_notes_in_piece[i-1] = [notes_in_piece[i-1], new_modified_note, i-1, ditto_and_modified_notes_in_piece[i][3], "(" + ditto_and_modified_notes_in_piece[i][4] + ")"]
                    elif new_modified_note in instrument_MIDI_notes and ditto_and_modified_notes_in_piece[i][4][0] == "(":
                        ditto_and_modified_notes_in_piece[i-1] = [notes_in_piece[i-1], new_modified_note, i-1, ditto_and_modified_notes_in_piece[i][3], ditto_and_modified_notes_in_piece[i][4]]
                    else:
                        modified_note = notes_in_piece[i-1] + optimal_modifier
                        ditto_and_modified_notes_in_piece[i-1] = [notes_in_piece[i-1], modified_note, i-1, 0, "outlier"]
                #A similar approach is followed if a inferred modification tag (without parentheses)
                #is identical to the modification tag of a modified note three notes away
                elif ditto_and_modified_notes_in_piece[i][4] == ditto_and_modified_notes_in_piece[i-3][4][1:-1]:
                    new_modified_note = ditto_and_modified_notes_in_piece[i-1] + ditto_and_modified_notes_in_piece[i][3]*12
                    if new_modified_note in instrument_MIDI_notes and ditto_and_modified_notes_in_piece[i][4][0] != "(":
                        ditto_and_modified_notes_in_piece[i-1] = [notes_in_piece[i-1], new_modified_note, i-1, ditto_and_modified_notes_in_piece[i][3], "(" + ditto_and_modified_notes_in_piece[i][4] + ")"]
                    elif new_modified_note in instrument_MIDI_notes and ditto_and_modified_notes_in_piece[i][4][0] == "(":
                        ditto_and_modified_notes_in_piece[i-1] = [notes_in_piece[i-1], new_modified_note, i-1, ditto_and_modified_notes_in_piece[i][3], ditto_and_modified_notes_in_piece[i][4]]
                    else:
                        modified_note = notes_in_piece[i-1] + optimal_modifier
                        ditto_and_modified_notes_in_piece[i-1] = [notes_in_piece[i-1], modified_note, i-1, 0, "outlier"]
            elif (type(ditto_and_modified_notes_in_piece[i]) == list
            and type(ditto_and_modified_notes_in_piece[i-1]) == int and type(ditto_and_modified_notes_in_piece[i-4]) == list):
                if ditto_and_modified_notes_in_piece[i][4] == ditto_and_modified_notes_in_piece[i-4][4]:
                    new_modified_note = ditto_and_modified_notes_in_piece[i-1] + ditto_and_modified_notes_in_piece[i][3]*12
                    if new_modified_note in instrument_MIDI_notes and ditto_and_modified_notes_in_piece[i][4][0] != "(":
                        ditto_and_modified_notes_in_piece[i-1] = [notes_in_piece[i-1], new_modified_note, i-1, ditto_and_modified_notes_in_piece[i][3], "(" + ditto_and_modified_notes_in_piece[i][4] + ")"]
                    elif new_modified_note in instrument_MIDI_notes and ditto_and_modified_notes_in_piece[i][4][0] == "(":
                        ditto_and_modified_notes_in_piece[i-1] = [notes_in_piece[i-1], new_modified_note, i-1, ditto_and_modified_notes_in_piece[i][3], ditto_and_modified_notes_in_piece[i][4]]
                    else:
                        modified_note = notes_in_piece[i-1] + optimal_modifier
                        ditto_and_modified_notes_in_piece[i-1] = [notes_in_piece[i-1], modified_note, i-1, 0, "outlier"]

    #The csv_string will be updated with all the modifications made to the notes of the piece.
    #"Lyric_t" tags will annotate the music scoresheets in the ".mid" files with the
    #"modified_with_tags" suffix. The counters "counter_note_on" and "counter_note_off" are
    #used to avoid assigning duplicate tags to notes.
    with open("modified song with inferences and without tags.csv", "w+") as output_csv:
        writer = csv.writer(output_csv)
        counter_note_on = 0
        open_notes_on = []
        for row in csv.reader(csv_string):
            if row[2].strip()[:7] == "Note_on":
                note_in_csv_string = int(row[4].strip())
                for i in range(counter_note_on, len(notes_in_piece)):
                    if (note_in_csv_string == notes_in_piece[i]+
                    octave_difference_between_piece_and_instrument*12 - optimal_modifier):
                        open_notes_on.append(ditto_and_modified_notes_in_piece[i])
                        #Applying the tempo_multiplier to the timestamps (default value of 1).
                        #A tempo_multiplier of 2 will result in 50% tempo.
                        if i < len(notes_in_piece)-2:
                            counter_note_on = i+1
                        timestamp = int(row[1])
                        new_timestamp = int(timestamp*tempo_multiplier)
                        row[1] = new_timestamp
                        if type(ditto_and_modified_notes_in_piece[i]) == int:
                            row[4] = " " + str(ditto_and_modified_notes_in_piece[i])
                            writer.writerow(row)
                            break
                        elif type(ditto_and_modified_notes_in_piece[i]) == list and ditto_and_modified_notes_in_piece[i][2] == i:
                            row[4] = " " + str(ditto_and_modified_notes_in_piece[i][1])
                            writer.writerow(row)
                            break

            #Here, "Lyric_t" tags are not appended to the csv_string, as they have already been added
            #to the corresponding "Note_on". The note in the current "Note_off" row is compared to
            #all of the open "Note_on" notes within the "open_notes_on" list. The matching notes are
            #updated within the row ("open_notes_on" derives from the "modified_notes_in_piece", so
            #if the notes weren't modified other than the overall changes in octaves and semitones,
            #the value will be of the type "int". Alternatively, if further changes in octave have
            #been individually applied to the note, it will be of the type "list", the element [0]
            #being the original note after the overall changes in octaves and semitones and the
            #element [1] will be the value of the note after individualized octave adjustments).
            #Once the row has been written in the "csv" file, the note is removed from the "open_note_on" list.
            elif row[2].strip()[:8] == "Note_off":
                note_in_csv_string = int(row[4].strip())
                timestamp = int(row[1])
                new_timestamp = int(timestamp*tempo_multiplier)
                row[1] = new_timestamp
                for j in range(len(open_notes_on)):
                    if (type(open_notes_on[j]) == list and note_in_csv_string == open_notes_on[j][0] +
                    octave_difference_between_piece_and_instrument*12 - optimal_modifier):
                        row[4] = " " + str(open_notes_on[j][1])
                        writer.writerow(row)
                        open_notes_on.pop(j)
                        break
                    elif (type(open_notes_on[j]) == int and note_in_csv_string == open_notes_on[j] +
                    octave_difference_between_piece_and_instrument*12 - optimal_modifier):
                        row[4] = " " + str(open_notes_on[j])
                        writer.writerow(row)
                        open_notes_on.pop(j)
                        break
            else:
                #Applying the tempo_multiplier to the timestamps (default value of 1).
                #A tempo_multiplier of 2 will result in 50% tempo.
                timestamp = int(row[1])
                new_timestamp = int(timestamp*tempo_multiplier)
                row[1] = new_timestamp
                writer.writerow(row)

    #Open the "_modified.csv" file that was just written in reading mode
    #and convert it to the corresponding MIDI file using the py_midicsv module.
    with open("modified song with inferences and without tags.csv", "r") as new_csv_string:
        midi_object = pm.csv_to_midi(new_csv_string)
        with open("modified song with inferences and without tags.mid", "wb") as output_file:
            midi_writer = pm.FileWriter(output_file)
            midi_writer.write(midi_object)

    #Repeat the process while adding tags at the outlier notes(whether they were further increased or decreased in octaves or not).
    #If these outlier notes were further modified in octaves, the "Lyric_t" tag would mention "i" for increase or "d" for decrease,
    #followed by the number of octaves. For example, "i1oct" indicates that the note, after its initial octave modification and
    #optimal_modifier application, was further increased by 1 octave in order be within the range of the instrument playable notes.
    with open("modified song with inferences and tags.csv", "w+") as output_csv:
        writer = csv.writer(output_csv)
        counter_note_on = 0
        open_notes_on = []
        for row in csv.reader(csv_string):
            if row[2].strip()[:7] == "Note_on":
                note_in_csv_string = int(row[4].strip())
                for i in range(counter_note_on, len(notes_in_piece)):
                    if (note_in_csv_string == notes_in_piece[i]+
                    octave_difference_between_piece_and_instrument*12 - optimal_modifier):
                        open_notes_on.append(ditto_and_modified_notes_in_piece[i])
                        #Applying the tempo_multiplier to the timestamps (default value of 1).
                        #A tempo_multiplier of 2 will result in 50% tempo.
                        if i < len(notes_in_piece)-2:
                            counter_note_on = i+1
                        timestamp = int(row[1])
                        new_timestamp = int(timestamp*tempo_multiplier)
                        row[1] = new_timestamp
                        if type(ditto_and_modified_notes_in_piece[i]) == int:
                            row[4] = " " + str(ditto_and_modified_notes_in_piece[i])
                            writer.writerow(row)
                            break
                        #Lyric_t meta-tags are added to the csv_string, which will appear in the annotated MIDI file.
                        elif type(ditto_and_modified_notes_in_piece[i]) == list:
                            row[4] = " " + str(ditto_and_modified_notes_in_piece[i][1])
                            writer.writerow(row)
                            track = int(row[0])
                            time = int(row[1])
                            writer.writerow([track, time, "Text_t", ditto_and_modified_notes_in_piece[i][4]])
                            break
            #Here, "Lyric_t" tags are not appended to the csv_string, as they have already been added
            #to the corresponding "Note_on".
            elif row[2].strip()[:8] == "Note_off":
                note_in_csv_string = int(row[4].strip())
                timestamp = int(row[1])
                new_timestamp = int(timestamp*tempo_multiplier)
                row[1] = new_timestamp
                for j in range(len(open_notes_on)):
                    if (type(open_notes_on[j]) == list and note_in_csv_string == open_notes_on[j][0] +
                    octave_difference_between_piece_and_instrument*12 - optimal_modifier):
                        row[4] = " " + str(open_notes_on[j][1])
                        writer.writerow(row)
                        open_notes_on.pop(j)
                        break
                    elif (type(open_notes_on[j]) == int and note_in_csv_string == open_notes_on[j] +
                    octave_difference_between_piece_and_instrument*12 - optimal_modifier):
                        row[4] = " " + str(open_notes_on[j])
                        writer.writerow(row)
                        open_notes_on.pop(j)
                        break
            else:
                #Applying the tempo_multiplier to the timestamps (default value of 1).
                #A tempo_multiplier of 2 will result in 50% tempo.
                timestamp = int(row[1])
                new_timestamp = int(timestamp*tempo_multiplier)
                row[1] = new_timestamp
                writer.writerow(row)

    #Open the "_modified.csv" file that was just written in reading mode
    #and convert it to the corresponding MIDI file using the py_midicsv module.
    with open("modified song with inferences and tags.csv", "r") as new_csv_string:
        midi_object = pm.csv_to_midi(new_csv_string)
        with open("modified song with inferences and tags.mid", "wb") as output_file:
            midi_writer = pm.FileWriter(output_file)
            midi_writer.write(midi_object)



    #GENERATING THE CSV AND MIDI FILES (WITH ADDITIONAL OUTLIERS)

    outliers_and_modified_notes_in_piece = modified_notes_in_piece.copy()

    #The last  of the "list" instances in the list "ditto_and_modified_notes_in_piece" (determined earlier)
    #will be used as a threshold upon which the "while" loop will be broken. The "note_counter"
    #will be incremented by 5 units after every run through the
    #"for i in range(note_counter, len(outliers_and_modified_notes_in_piece)-5):" loop.
    #When "note_counter" is incremented for the last time, it will exceed the
    #value of "last_list_instance_in_modified_notes_in_piece" and the "while"
    #loop will be broken.
    last_list_instance_in_modified_notes_in_piece = list_instances_in_modified_notes_in_piece[-1]

    #Every entry in the "outliers_and_modified_notes_in_piece" (starting at entry 4) is accessed to determine
    #its type. If the entry is a "list", the previous four and next four entries are screened
    #in order to determine their type. Every time a "list" is encountered, the counters
    #"modified_note_count_before" and "modified_note_count_after" are incremented by one.
    note_counter = 4
    isolated_and_consecutive_modified_note_indices = []
    while note_counter < last_list_instance_in_modified_notes_in_piece and note_counter < len(outliers_and_modified_notes_in_piece)-4:
        for i in range(note_counter, len(outliers_and_modified_notes_in_piece)-4):
            if type(outliers_and_modified_notes_in_piece[i]) == list:
                modified_note_count_before = 0
                modified_note_count_after = 0
                for j in range(-1, -5, -1):
                    if type(outliers_and_modified_notes_in_piece[i+j]) == list:
                        modified_note_count_before +=1
                for j in range(1, 5):
                    if type(outliers_and_modified_notes_in_piece[i+j]) == list:
                        modified_note_count_after +=1

                #If there are no "lists" in the previous and next four notes, it means the note
                #is an isolated modified note. It is then added to the list
                #"isolated_and_consecutive_modified_note_indices".
                if modified_note_count_before == 0 and modified_note_count_after == 0:
                    isolated_and_consecutive_modified_note_indices.append(i)

                #If there are no "lists" in the previous four notes and the next four notes are
                #all lists, it means that the previous four notes are unmodified and that there
                #is a sequence of five (including the current note at index i) consecutive
                #modified notes.These five notes are added to the list
                #"isolated_and_consecutive_modified_note_indices"
                elif modified_note_count_before == 0 and modified_note_count_after == 4:
                    isolated_and_consecutive_modified_note_indices.extend([i, i+1, i+2, i+3, i+4])

                #If the previous four notes are all lists and there are no "lists" in the next four notes,
                #it means that the next four notes are unmodified and that there
                #is a sequence of five (including the current note at index i) consecutive
                #modified notes.These five notes are added to the list
                #"isolated_and_consecutive_modified_note_indices"
                elif modified_note_count_before == 4 and modified_note_count_after == 0:
                    isolated_and_consecutive_modified_note_indices.extend([i-4, i-3, i-2, i-1, i])

                #If the previous and next four notes are all lists, it means that there
                #is a sequence of nine (including the current note at index i) consecutive
                #modified notes.These nine notes are added to the list
                #"isolated_and_consecutive_modified_note_indices"
                elif modified_note_count_before == 4 and modified_note_count_after == 4:
                    isolated_and_consecutive_modified_note_indices.extend([i-4, i-3, i-2, i-1, i, i+1, i+2, i+3, i+4])

                #If the previous four notes are all lists, and some but not all of the next four
                #notes are lists, it means that there are at least five consecutive modified notes.
                elif (modified_note_count_before == 4 and modified_note_count_after < 4):
                    #If the type of the next note is "int", then it means that there are only five
                    #consecutive modified notes (including the current note at index i). These five
                    #notes are added to the list "isolated_and_consecutive_modified_note_indices"
                    #Then, the notes at indices i+2 onwards are checked (as we know that note i+1 is an integer)
                    #and if their type is "list" and if they aren't found in the list
                    #"isolated_and_consecutive_modified_note_indices", They will be labeled as outliers
                    #and reverted to their original value in the list "outliers_and_modified_notes_in_piece"
                    #before individualized note octave modifications.
                    if type(outliers_and_modified_notes_in_piece[i+1]) == int:
                        isolated_and_consecutive_modified_note_indices.extend([i-4, i-3, i-2, i-1, i])
                        for j in range(2, 5):
                            if type(outliers_and_modified_notes_in_piece[i+j]) == list and (i+j not in isolated_and_consecutive_modified_note_indices):
                                outliers_and_modified_notes_in_piece[i+j] = [notes_in_piece[i+j], notes_in_piece[i+j] + optimal_modifier, i+j, 0, "O"]
                    #A similar approach to above is taken, but as i+1 is of the type "list" (otherwise it would have been intercepted above),
                    #There are now six consecutive modified notes, which will be added to the list
                    #"isolated_and_consecutive_modified_note_indices".
                    elif type(outliers_and_modified_notes_in_piece[i+2]) == int:
                        isolated_and_consecutive_modified_note_indices.extend([i-4, i-3, i-2, i-1, i, i+1])
                        for j in range(3, 5):
                            if type(outliers_and_modified_notes_in_piece[i+j]) == list and (i+j not in isolated_and_consecutive_modified_note_indices):
                                outliers_and_modified_notes_in_piece[i+j] = [notes_in_piece[i+j], notes_in_piece[i+j] + optimal_modifier, i+j, 0, "O"]
                    #Likewise, if the note at index i+2 is of the type "list" (otherwise it would have been intercepted above),
                    #There are now seven consecutive modified notes, which will be added to the list
                    #"isolated_and_consecutive_modified_note_indices".
                    elif type(outliers_and_modified_notes_in_piece[i+3]) == int:
                        isolated_and_consecutive_modified_note_indices.extend([i-4, i-3, i-2, i-1, i, i+1, i+2])
                        if type(outliers_and_modified_notes_in_piece[i+4]) == list and (i+4 not in isolated_and_consecutive_modified_note_indices):
                            outliers_and_modified_notes_in_piece[i+4] = [notes_in_piece[i+4], notes_in_piece[i+4] + optimal_modifier, i+4, 0, "O"]
                    #Finally, if the note at index i+3 is of the type "list" (otherwise it would have been intercepted above),
                    #There are now eight consecutive modified notes, which will be added to the list
                    #"isolated_and_consecutive_modified_note_indices".
                    elif type(outliers_and_modified_notes_in_piece[i+4]) == int:
                        isolated_and_consecutive_modified_note_indices.extend([i-4, i-3, i-2, i-1, i, i+1, i+2, i+3])

                #This is very similar to the "elif" directly above, but reversed.
                elif modified_note_count_before < 4 and modified_note_count_after == 4:
                    if type(outliers_and_modified_notes_in_piece[i-1]) == int:
                        isolated_and_consecutive_modified_note_indices.extend([i, i+1, i+2, i+3, i+4])
                        for j in range(-2,-5, -1):
                            if type(outliers_and_modified_notes_in_piece[i+j]) == list and (i+j not in isolated_and_consecutive_modified_note_indices):
                                outliers_and_modified_notes_in_piece[i+j] = [notes_in_piece[i+j], notes_in_piece[i+j] + optimal_modifier, i+j, 0, "O"]
                    elif type(outliers_and_modified_notes_in_piece[i-2]) == int:
                        isolated_and_consecutive_modified_note_indices.extend([i-1, i, i+1, i+2, i+3, i+4])
                        for j in range(-3,-5, -1):
                            if type(outliers_and_modified_notes_in_piece[i+j]) == list and (i+j not in isolated_and_consecutive_modified_note_indices):
                                outliers_and_modified_notes_in_piece[i+j] = [notes_in_piece[i+j], notes_in_piece[i+j] + optimal_modifier, i+j, 0, "O"]
                    elif type(outliers_and_modified_notes_in_piece[i-3]) == int:
                        isolated_and_consecutive_modified_note_indices.extend([i-2, i-1, i, i+1, i+2, i+3, i+4])
                        if type(outliers_and_modified_notes_in_piece[i-4]) == list and (i-4 not in isolated_and_consecutive_modified_note_indices):
                            outliers_and_modified_notes_in_piece[i-4] = [notes_in_piece[i-4], notes_in_piece[i-4] + optimal_modifier, i-4, 0, "O"]
                    elif type(outliers_and_modified_notes_in_piece[i-4]) == int:
                        isolated_and_consecutive_modified_note_indices.extend([i-3, i-2, i-1, i, i+1, i+2, i+3, i+4])

                #If some but not all of the previous and next notes are of the type "list" (we already intercepted the cases where
                #none of the previous or next notes are "lists" above), all of the notes of the type "list", including the current
                #note at index i, will be converted to outliers, provided that they are not in the list
                #"isolated_and_consecutive_modified_note_indices".
                elif modified_note_count_before < 4 and modified_note_count_after < 4:
                    for j in range(-1,-5, -1):
                        if type(outliers_and_modified_notes_in_piece[i+j]) == list and (i+j not in isolated_and_consecutive_modified_note_indices):
                            outliers_and_modified_notes_in_piece[i+j] = [notes_in_piece[i+j], notes_in_piece[i+j] + optimal_modifier, i+j, 0, "O"]
                    for j in range(1,5, 1):
                        if type(outliers_and_modified_notes_in_piece[i+j]) == list and (i+j not in isolated_and_consecutive_modified_note_indices):
                            outliers_and_modified_notes_in_piece[i+j] = [notes_in_piece[i+j], notes_in_piece[i+j] + optimal_modifier, i+j, 0, "O"]
                    outliers_and_modified_notes_in_piece[i] = [notes_in_piece[i], notes_in_piece[i] + optimal_modifier, i, 0, "O"]

                #Analyzing the last modified note and its preceding four notes for consistency. If the previous four notes are
                #of the type "list", it means that there are really five contiguous modified notes and the values of the notes
                #are reinitialized to their original value in the "modified_notes_in_piece" list, in case one or more of them
                #are labelled as outliers. Also, there is at least one unmodified note and one modified in the four notes prior
                #to the final modified note, the four notes are converted to outliers (and reinitialized to their original value
                #in the "notes_in_piece" list).
                elif i >= last_list_instance_in_modified_notes_in_piece:
                    o_note_count_before = 0
                    modified_note_count_before = 0
                    for i in range(last_list_instance_in_modified_notes_in_piece, last_list_instance_in_modified_notes_in_piece-5, -1):
                        if type(outliers_and_modified_notes_in_piece[i]) == list and outliers_and_modified_notes_in_piece[i][4] == "O":
                            o_note_count_before += 1
                        elif type(outliers_and_modified_notes_in_piece[i]) == list and outliers_and_modified_notes_in_piece[i][4] != "O":
                            modified_note_count_before += 1
                    if o_note_count_before + modified_note_count_before == 5:
                        for i in range(last_list_instance_in_modified_notes_in_piece, last_list_instance_in_modified_notes_in_piece-5, -1):
                            outliers_and_modified_notes_in_piece[i] = modified_notes_in_piece[i]
                    elif o_note_count_before + modified_note_count_before != 5 and o_note_count_before > 0:
                        for i in range(last_list_instance_in_modified_notes_in_piece, last_list_instance_in_modified_notes_in_piece-5, -1):
                            if type(outliers_and_modified_notes_in_piece[i]) == list:
                                outliers_and_modified_notes_in_piece[i] = [notes_in_piece[i], notes_in_piece[i] + optimal_modifier, i, 0, "O"]

            #The "note_counter" is incremented by five to walk along the indices of the list "outliers_and_modified_notes_in_piece"
            #and search for the next modified note (that is, of the type "list").
            note_counter = i + 5
            break

    for i in range(len(outliers_and_modified_notes_in_piece)):
        #Reverting any outliers flanked by four modified notes to their original value
        #in the "modified_notes_in_piece" list. These outliers appear because depending
        #on where the index ends up after incrementing the "note_counter", it could lie
        #after the start of a stretch of at least five modified notes, but within four
        #notes of an unmodified note before the new index, meaning it will percieve any
        #modified notes before it as outliers (example: "unmod unmod mod mod index mod mod mod mod mod"
        #would be converted to "O O O O O mod mod mod mod mod").
        if type(outliers_and_modified_notes_in_piece[i]) == list:
            modified_note_count_before = 0
            o_note_count_before = 0
            modified_note_count_after = 0
            o_note_count_after = 0
            #In order to look at the four indices prior to the current index, i needs to exceed four
            if i > 4:
                for j in range(0, -5, -1):
                    if (type(outliers_and_modified_notes_in_piece[i+j]) == list
                    and outliers_and_modified_notes_in_piece[i+j][4] == "O"):
                        o_note_count_before += 1
                    elif (type(outliers_and_modified_notes_in_piece[i+j]) == list
                    and outliers_and_modified_notes_in_piece[i+j][4] != "O"):
                        modified_note_count_before += 1
            elif i < len(outliers_and_modified_notes_in_piece)-4:
                for j in range(0, 5):
                    if (type(outliers_and_modified_notes_in_piece[i+j]) == list
                    and outliers_and_modified_notes_in_piece[i+j][4] == "O"):
                        o_note_count_after += 1
                    elif (type(outliers_and_modified_notes_in_piece[i+j]) == list
                    and outliers_and_modified_notes_in_piece[i+j][4] != "O"):
                        modified_note_count_after += 1
            #If the five notes analyzed (four previous notes and current index) consist of a mixture of outliers and
            #modified notes, all these notes will be reverted to their original values in
            #the "modified_notes_in_piece", because they really form a sequence of five
            #modified notes and should not contain outliers.
            if (modified_note_count_before !=5 and o_note_count_before !=5
            and modified_note_count_before + o_note_count_before == 5):
                for j in range(0, -5, -1):
                    outliers_and_modified_notes_in_piece[i+j] = modified_notes_in_piece[i+j]
                    isolated_and_consecutive_modified_note_indices.append(i+j)
            #If the five notes analyzed (four following notes and current index) consist of a mixture of outliers and
            #modified notes, all these notes will be reverted to their original values in
            #the "modified_notes_in_piece", because they really form a sequence of five
            #modified notes and should not contain outliers.
            elif (modified_note_count_after !=5 and o_note_count_after !=5
            and modified_note_count_after + o_note_count_after == 5):
                for j in range(0, 5):
                    outliers_and_modified_notes_in_piece[i+j] = modified_notes_in_piece[i+j]
                    isolated_and_consecutive_modified_note_indices.append(i+j)
            elif o_note_count_before == 5:
                for j in range(0, -5, -1):
                    outliers_and_modified_notes_in_piece[i+j] = modified_notes_in_piece[i+j]
                    isolated_and_consecutive_modified_note_indices.append(i+j)
            elif o_note_count_after == 5:
                for j in range(0, 5):
                    outliers_and_modified_notes_in_piece[i+j] = modified_notes_in_piece[i+j]
                    isolated_and_consecutive_modified_note_indices.append(i+j)

    #Checking for modified notes that should really be labeled as "O" outliers, because they contain
    for i in range(len(outliers_and_modified_notes_in_piece)):
        if type(outliers_and_modified_notes_in_piece[i]) == list:
            list_note_count_before = 0
            int_note_count_before = 0
            list_note_count_after = 0
            int_note_count_after = 0
            #In order to look at the four indices prior to the current index, i needs to exceed 4
            if i > 4:
                for j in range(-1, -5, -1):
                    if (type(outliers_and_modified_notes_in_piece[i+j]) == list and
                    i+j not in isolated_and_consecutive_modified_note_indices):
                        list_note_count_before += 1
                    elif type(outliers_and_modified_notes_in_piece[i+j]) == int:
                        int_note_count_before += 1
            #In order to look at the four last indices after the current index,
            #i needs to be at most len(outliers_and_modified_notes_in_piece)-3
            elif i < len(outliers_and_modified_notes_in_piece)-4:
                for j in range(1, 5):
                    if (type(outliers_and_modified_notes_in_piece[i+j]) == list and
                    i+j not in isolated_and_consecutive_modified_note_indices):
                        list_note_count_after += 1
                    elif type(outliers_and_modified_notes_in_piece[i+j]) == int:
                        int_note_count_after += 1
            #If there are between 1 and 3 unmodified notes ("int type") before the current note
            #and at least one modified note ("list" type) the notes will be converted to "O" outliers.
            if int_note_count_before > 0 and int_note_count_before < 4 and list_note_count_before > 0:
                for j in range(0, -5, -1):
                    if (type(outliers_and_modified_notes_in_piece[i+j]) == list and
                    i+j not in isolated_and_consecutive_modified_note_indices):
                        outliers_and_modified_notes_in_piece[i+j] = [notes_in_piece[i+j], notes_in_piece[i+j] + optimal_modifier, i+j, 0, "O"]
            #If there are between 1 and 3 unmodified notes ("int type") after the current note
            #and at least one modified note ("list" type) the notes will be converted to "O" outliers.
            elif int_note_count_after > 0 and int_note_count_after < 4 and list_note_count_after > 0:
                for j in range(0, 5):
                    if (type(outliers_and_modified_notes_in_piece[i+j]) == list and
                    i+j not in isolated_and_consecutive_modified_note_indices):
                        outliers_and_modified_notes_in_piece[i+j] = [notes_in_piece[i+j], notes_in_piece[i+j] + optimal_modifier, i+j, 0, "O"]


    #The csv_string will be updated with all the modifications made to the notes of the piece.
    #"Lyric_t" tags will annotate the music scoresheets in the ".mid" files with the
    #"modified_with_tags" suffix. The counters "counter_note_on" and "counter_note_off" are
    #used to avoid assigning duplicate tags to notes.
    with open("modified song with outliers and without tags.csv", "w+") as output_csv:
        writer = csv.writer(output_csv)
        counter_note_on = 0
        open_notes_on = []
        for row in csv.reader(csv_string):
            if row[2].strip()[:7] == "Note_on":
                note_in_csv_string = int(row[4].strip())
                for i in range(counter_note_on, len(notes_in_piece)):
                    if (note_in_csv_string == notes_in_piece[i]+
                    octave_difference_between_piece_and_instrument*12 - optimal_modifier):
                        open_notes_on.append(outliers_and_modified_notes_in_piece[i])
                        #Applying the tempo_multiplier to the timestamps (default value of 1).
                        #A tempo_multiplier of 2 will result in 50% tempo.
                        if i < len(notes_in_piece)-2:
                            counter_note_on = i+1
                        timestamp = int(row[1])
                        new_timestamp = int(timestamp*tempo_multiplier)
                        row[1] = new_timestamp
                        if type(outliers_and_modified_notes_in_piece[i]) == int:
                            row[4] = " " + str(outliers_and_modified_notes_in_piece[i])
                            writer.writerow(row)
                            break
                        elif type(outliers_and_modified_notes_in_piece[i]) == list and outliers_and_modified_notes_in_piece[i][2] == i:
                            row[4] = " " + str(outliers_and_modified_notes_in_piece[i][1])
                            writer.writerow(row)
                            break

            #Here, "Lyric_t" tags are not appended to the csv_string, as they have already been added
            #to the corresponding "Note_on".
            elif row[2].strip()[:8] == "Note_off":
                note_in_csv_string = int(row[4].strip())
                timestamp = int(row[1])
                new_timestamp = int(timestamp*tempo_multiplier)
                row[1] = new_timestamp
                for j in range(len(open_notes_on)):
                    if (type(open_notes_on[j]) == list and note_in_csv_string == open_notes_on[j][0] +
                    octave_difference_between_piece_and_instrument*12 - optimal_modifier):
                        row[4] = " " + str(open_notes_on[j][1])
                        writer.writerow(row)
                        open_notes_on.pop(j)
                        break
                    elif (type(open_notes_on[j]) == int and note_in_csv_string == open_notes_on[j] +
                    octave_difference_between_piece_and_instrument*12 - optimal_modifier):
                        row[4] = " " + str(open_notes_on[j])
                        writer.writerow(row)
                        open_notes_on.pop(j)
                        break
            else:
                #Applying the tempo_multiplier to the timestamps (default value of 1).
                #A tempo_multiplier of 2 will result in 50% tempo.
                timestamp = int(row[1])
                new_timestamp = int(timestamp*tempo_multiplier)
                row[1] = new_timestamp
                writer.writerow(row)

    #Open the "_modified.csv" file that was just written in reading mode
    #and convert it to the corresponding MIDI file using the py_midicsv module.
    with open("modified song with outliers and without tags.csv", "r") as new_csv_string:
        midi_object = pm.csv_to_midi(new_csv_string)
        with open("modified song with outliers and without tags.mid", "wb") as output_file:
            midi_writer = pm.FileWriter(output_file)
            midi_writer.write(midi_object)


    #Repeat the process while adding tags at the outlier notes(whether they were further increased or decreased in octaves or not).
    #If these outlier notes were further modified in octaves, the "Lyric_t" tag would mention "i" for increase or "d" for decrease,
    #followed by the number of octaves. For example, "i1oct" indicates that the note, after its initial octave modification and
    #optimal_modifier application, was further increased by 1 octave in order be within the range of the instrument playable notes.
    with open("modified song with outliers and tags.csv", "w+") as output_csv:
        writer = csv.writer(output_csv)
        counter_note_on = 0
        open_notes_on = []
        for row in csv.reader(csv_string):
            if row[2].strip()[:7] == "Note_on":
                note_in_csv_string = int(row[4].strip())
                for i in range(counter_note_on, len(notes_in_piece)):
                    if (note_in_csv_string == notes_in_piece[i]+
                    octave_difference_between_piece_and_instrument*12 - optimal_modifier):
                        #Here the note originates from the "outliers_and_modified_notes_in_piece"
                        #list, as if it is an "O" outlier, the individualized octave changes
                        #will have been reversed and element[1] will be equivalent to element[0]
                        open_notes_on.append(outliers_and_modified_notes_in_piece[i])
                        #Applying the tempo_multiplier to the timestamps (default value of 1).
                        #A tempo_multiplier of 2 will result in 50% tempo.
                        if i < len(notes_in_piece)-2:
                            counter_note_on = i+1
                        timestamp = int(row[1])
                        new_timestamp = int(timestamp*tempo_multiplier)
                        row[1] = new_timestamp
                        if type(outliers_and_modified_notes_in_piece[i]) == int:
                            row[4] = " " + str(outliers_and_modified_notes_in_piece[i])
                            writer.writerow(row)
                            break
                        #Lyric_t meta-tags are added to the csv_string, which will appear in the annotated MIDI file.
                        elif type(outliers_and_modified_notes_in_piece[i]) == list:
                            row[4] = " " + str(outliers_and_modified_notes_in_piece[i][1])
                            writer.writerow(row)
                            track = int(row[0])
                            time = int(row[1])
                            writer.writerow([track, time, "Text_t", outliers_and_modified_notes_in_piece[i][4]])
                            break

            #Here, "Lyric_t" tags are not appended to the csv_string, as they have already been added
            #to the corresponding "Note_on".
            elif row[2].strip()[:8] == "Note_off":
                note_in_csv_string = int(row[4].strip())
                timestamp = int(row[1])
                new_timestamp = int(timestamp*tempo_multiplier)
                row[1] = new_timestamp
                for j in range(len(open_notes_on)):
                    if (type(open_notes_on[j]) == list and note_in_csv_string == open_notes_on[j][0] +
                    octave_difference_between_piece_and_instrument*12 - optimal_modifier):
                        row[4] = " " + str(open_notes_on[j][1])
                        writer.writerow(row)
                        open_notes_on.pop(j)
                        break
                    elif (type(open_notes_on[j]) == int and note_in_csv_string == open_notes_on[j] +
                    octave_difference_between_piece_and_instrument*12 - optimal_modifier):
                        row[4] = " " + str(open_notes_on[j])
                        writer.writerow(row)
                        open_notes_on.pop(j)
                        break
            else:
                #Applying the tempo_multiplier to the timestamps (default value of 1).
                #A tempo_multiplier of 2 will result in 50% tempo.
                timestamp = int(row[1])
                new_timestamp = int(timestamp*tempo_multiplier)
                row[1] = new_timestamp
                writer.writerow(row)


    #Open the "_modified.csv" file that was just written in reading mode
    #and convert it to the corresponding MIDI file using the py_midicsv module.
    with open("modified song with outliers and tags.csv", "r") as new_csv_string:
        midi_object = pm.csv_to_midi(new_csv_string)
        with open("modified song with outliers and tags.mid", "wb") as output_file:
            midi_writer = pm.FileWriter(output_file)
            midi_writer.write(midi_object)


    #GENERATE REPORTS ON MODIFICATIONS

    #Statistics are compiled to give the user a summary of the modifications made to the music piece,
    #while explaining how the annotations should be read. The PHP code will validate that the Python
    #script was run successfully by ensuring that the first letter of the output string is an "A".
    if octave_difference_between_piece_and_instrument > 0:
        octave_modification_adjective = "decreased"
    elif octave_difference_between_piece_and_instrument < 0:
        octave_modification_adjective = "increased"

    if optimal_modifier > 0:
        optimal_modifier_adjective = "raised"
    elif optimal_modifier < 0:
        optimal_modifier_adjective = "lowered"

    percentage_of_notes_within_range_of_instrument = int(percentage_of_notes_within_range_of_instrument)

    if lowest_note != None and highest_note != None:
        if octave_difference_between_piece_and_instrument not in [-1, 0, 1] and optimal_modifier not in [-1, 0, 1]:
            statistics = ("After arrangement, all the notes were <i><b>" + octave_modification_adjective +
            "</b></i> by <b>" + str(abs(octave_difference_between_piece_and_instrument)) + " octaves</b>. After that, every note was <i><b>" +
            optimal_modifier_adjective + "</b></i> by <b>" + str(abs(optimal_modifier)) + " half steps</b>. These " +
            "modifications resulted in <b>" + str(percentage_of_notes_within_range_of_instrument) + "% of notes </b>" +
            "being within the specified range (" + str(lowest_note) + "-" + str(highest_note) + "). " +
            "<br><br>The remaining notes (if any) were labeled as follows in the <b>annotated</b> MIDI (.mid) files: " +
            '“i-” for increased or “d-” for decreased, followed by the number of octaves ' +
            "<b>(ex: “i-1” for increased one octave)</b> If a note could not be brought within the range of your instrument by " +
            "further modifying its octave, is was tagged as an “outlier”. " +
            "The tags may be reviewed by opening the annotated MIDI files in a scorewriter software." +
            "<br><br>Three different sets of MIDI files (<b>with or without annotations</b>) are available for download: " +
            "<br><ul> <li>If there were at most three unmodified notes in between two identically modified notes, " +
            "the same modifications were then applied to these notes by inference. These deduced modifications were parenthesized for clarity (<b>with inferences</b>).</li>" +
            "<li>Alternatively, if a passage was strewn with modified and unmodified notes, the individual octave changes " +
            "were reversed and these notes were tagged as “O” to indicate that these outliers will need to be arranged manually (<b>with “O” outliers</b>).</li>" +
            "<li>Finally, all the notes outside the range of the instrument were modified, if possible (<b>with changes</b>).</li></ul>")
        elif octave_difference_between_piece_and_instrument not in [-1, 0, 1] and optimal_modifier in [-1, 1]:
            statistics = ("After arrangement, all the notes were <i><b>" + octave_modification_adjective +
            "</b></i> by <b>" + str(abs(octave_difference_between_piece_and_instrument)) + " octaves</b>. After that, every note was <i><b>" +
            optimal_modifier_adjective + "</b></i> by <b>" + str(abs(optimal_modifier)) + " half step</b>. These " +
            "modifications resulted in <b>" + str(percentage_of_notes_within_range_of_instrument) + "% of notes </b>" +
            "being within the specified range (" + str(lowest_note) + "-" + str(highest_note) + "). " +
            "<br><br>The remaining notes (if any) were labeled as follows in the <b>annotated</b> MIDI (.mid) files: " +
            '“i-” for increased or “d-” for decreased, followed by the number of octaves ' +
            "<b>(ex: “i-1” for increased one octave)</b>. If a note could not be brought within the range of your instrument by " +
            "further modifying its octave, is was tagged as an “outlier”. " +
            "The tags may be reviewed by opening the annotated MIDI files in a scorewriter software." +
            "<br><br>Three different sets of MIDI files (<b>with or without annotations</b>) are available for download: " +
            "<br><ul> <li>If there were at most three unmodified notes in between two identically modified notes, " +
            "the same modifications were then applied to these notes by inference. These deduced modifications were parenthesized for clarity (<b>with inferences</b>).</li>" +
            "<li>Alternatively, if a passage was strewn with modified and unmodified notes, the individual octave changes " +
            "were reversed and these notes were tagged as “O” to indicate that these outliers will need to be arranged manually (<b>with “O” outliers</b>).</li>" +
            "<li>Finally, all the notes outside the range of the instrument were modified, if possible (<b>with changes</b>).</li></ul>")
        elif octave_difference_between_piece_and_instrument not in [-1, 0, 1] and optimal_modifier == 0:
            statistics = ("After arrangement, all the notes were <i><b>" + octave_modification_adjective +
            "</b></i> by <b>" + str(abs(octave_difference_between_piece_and_instrument)) + " octaves</b>. These " +
            "modifications resulted in <b>" + str(percentage_of_notes_within_range_of_instrument) + "% of notes </b>" +
            "being within the specified range (" + str(lowest_note) + "-" + str(highest_note) + "). " +
            "<br><br>The remaining notes (if any) were labeled as follows in the <b>annotated</b> MIDI (.mid) files: " +
            '“i-” for increased or “d-” for decreased, followed by the number of octaves ' +
            "<b>(ex: “i-1” for increased one octave)</b>. If a note could not be brought within the range of your instrument by " +
            "further modifying its octave, is was tagged as an “outlier”. " +
            "The tags may be reviewed by opening the annotated MIDI files in a scorewriter software." +
            "<br><br>Three different sets of MIDI files (<b>with or without annotations</b>) are available for download: " +
            "<br><ul> <li>If there were at most three unmodified notes in between two identically modified notes, " +
            "the same modifications were then applied to these notes by inference. These deduced modifications were parenthesized for clarity (<b>with inferences</b>).</li>" +
            "<li>Alternatively, if a passage was strewn with modified and unmodified notes, the individual octave changes " +
            "were reversed and these notes were tagged as “O” to indicate that these outliers will need to be arranged manually (<b>with “O” outliers</b>).</li>" +
            "<li>Finally, all the notes outside the range of the instrument were modified, if possible (<b>with changes</b>).</li></ul>")
        elif octave_difference_between_piece_and_instrument in [-1, 1] and optimal_modifier not in [-1, 0, 1]:
            statistics = ("After arrangement, all the notes were <i><b>" + octave_modification_adjective +
            "</b></i> by <b>" + str(abs(octave_difference_between_piece_and_instrument)) + " octave</b>. After that, every note was <i><b>" +
            optimal_modifier_adjective + "</b></i> by <b>" + str(abs(optimal_modifier)) + " half steps</b>. These " +
            "modifications resulted in <b>" + str(percentage_of_notes_within_range_of_instrument) + "% of notes </b>" +
            "being within the specified range (" + str(lowest_note) + "-" + str(highest_note) + "). " +
            "<br><br>The remaining notes (if any) were labeled as follows in the <b>annotated</b> MIDI (.mid) files: " +
            '“i-” for increased or “d-” for decreased, followed by the number of octaves ' +
            "<b>(ex: “i-1” for increased one octave)</b>. If a note could not be brought within the range of your instrument by " +
            "further modifying its octave, is was tagged as an “outlier”. " +
            "The tags may be reviewed by opening the annotated MIDI files in a scorewriter software." +
            "<br><br>Three different sets of MIDI files (<b>with or without annotations</b>) are available for download: " +
            "<br><ul> <li>If there were at most three unmodified notes in between two identically modified notes, " +
            "the same modifications were then applied to these notes by inference. These deduced modifications were parenthesized for clarity (<b>with inferences</b>).</li>" +
            "<li>Alternatively, if a passage was strewn with modified and unmodified notes, the individual octave changes " +
            "were reversed and these notes were tagged as “O” to indicate that these outliers will need to be arranged manually (<b>with “O” outliers</b>).</li>" +
            "<li>Finally, all the notes outside the range of the instrument were modified, if possible (<b>with changes</b>).</li></ul>")
        elif octave_difference_between_piece_and_instrument in [-1, 1] and optimal_modifier in [-1, 1]:
            statistics = ("After arrangement, all the notes were <i><b>" + octave_modification_adjective +
            "</b></i> by <b>" + str(abs(octave_difference_between_piece_and_instrument)) + " octave</b>. After that, every note was <i><b>" +
            optimal_modifier_adjective + "</b></i> by <b>" + str(abs(optimal_modifier)) + " half step</b>. These " +
            "modifications resulted in <b>" + str(percentage_of_notes_within_range_of_instrument) + "% of notes </b>" +
            "being within the specified range (" + str(lowest_note) + "-" + str(highest_note) + "). " +
            "<br><br>The remaining notes (if any) were labeled as follows in the <b>annotated</b> MIDI (.mid) files: " +
            '“i-” for increased or “d-” for decreased, followed by the number of octaves ' +
            "<b>(ex: “i-1” for increased one octave)</b>. If a note could not be brought within the range of your instrument by " +
            "further modifying its octave, is was tagged as an “outlier”. " +
            "The tags may be reviewed by opening the annotated MIDI files in a scorewriter software." +
            "<br><br>Three different sets of MIDI files (<b>with or without annotations</b>) are available for download: " +
            "<br><ul> <li>If there were at most three unmodified notes in between two identically modified notes, " +
            "the same modifications were then applied to these notes by inference. These deduced modifications were parenthesized for clarity (<b>with inferences</b>).</li>" +
            "<li>Alternatively, if a passage was strewn with modified and unmodified notes, the individual octave changes " +
            "were reversed and these notes were tagged as “O” to indicate that these outliers will need to be arranged manually (<b>with “O” outliers</b>).</li>" +
            "<li>Finally, all the notes outside the range of the instrument were modified, if possible (<b>with changes</b>).</li></ul>")
        elif octave_difference_between_piece_and_instrument in [-1, 1] and optimal_modifier == 0:
            statistics = ("After arrangement, all the notes were <i><b>" + octave_modification_adjective +
            "</b></i> by <b>" + str(abs(octave_difference_between_piece_and_instrument)) + " octave</b>. These " +
            "modifications resulted in <b>" + str(percentage_of_notes_within_range_of_instrument) + "% of notes </b>" +
            "being within the specified range (" + str(lowest_note) + "-" + str(highest_note) + "). " +
            "<br><br>The remaining notes (if any) were labeled as follows in the <b>annotated</b> MIDI (.mid) files: " +
            '“i-” for increased or “d-” for decreased, followed by the number of octaves ' +
            "<b>(ex: “i-1” for increased one octave)</b>. If a note could not be brought within the range of your instrument by " +
            "further modifying its octave, is was tagged as an “outlier”. " +
            "The tags may be reviewed by opening the annotated MIDI files in a scorewriter software." +
            "<br><br>Three different sets of MIDI files (<b>with or without annotations</b>) are available for download: " +
            "<br><ul> <li>If there were at most three unmodified notes in between two identically modified notes, " +
            "the same modifications were then applied to these notes by inference. These deduced modifications were parenthesized for clarity (<b>with inferences</b>).</li>" +
            "<li>Alternatively, if a passage was strewn with modified and unmodified notes, the individual octave changes " +
            "were reversed and these notes were tagged as “O” to indicate that these outliers will need to be arranged manually (<b>with “O” outliers</b>).</li>" +
            "<li>Finally, all the notes outside the range of the instrument were modified, if possible (<b>with changes</b>).</li></ul>")
        elif octave_difference_between_piece_and_instrument == 0 and optimal_modifier not in [-1, 0, 1]:
            statistics = ("After arrangement, every note was <i><b>" +
            optimal_modifier_adjective + "</b></i> by <b>" + str(abs(optimal_modifier)) + " half steps</b>. These " +
            "modifications resulted in <b>" + str(percentage_of_notes_within_range_of_instrument) + "% of notes </b>" +
            "being within the specified range (" + str(lowest_note) + "-" + str(highest_note) + "). " +
            "<br><br>The remaining notes (if any) were labeled as follows in the <b>annotated</b> MIDI (.mid) files: " +
            '“i-” for increased or “d-” for decreased, followed by the number of octaves ' +
            "<b>(ex: “i-1” for increased one octave)</b>. If a note could not be brought within the range of your instrument by " +
            "further modifying its octave, is was tagged as an “outlier”. " +
            "The tags may be reviewed by opening the annotated MIDI files in a scorewriter software." +
            "<br><br>Three different sets of MIDI files (<b>with or without annotations</b>) are available for download: " +
            "<br><ul> <li>If there were at most three unmodified notes in between two identically modified notes, " +
            "the same modifications were then applied to these notes by inference. These deduced modifications were parenthesized for clarity (<b>with inferences</b>).</li>" +
            "<li>Alternatively, if a passage was strewn with modified and unmodified notes, the individual octave changes " +
            "were reversed and these notes were tagged as “O” to indicate that these outliers will need to be arranged manually (<b>with “O” outliers</b>).</li>" +
            "<li>Finally, all the notes outside the range of the instrument were modified, if possible (<b>with changes</b>).</li></ul>")
        elif octave_difference_between_piece_and_instrument == 0 and optimal_modifier in [-1, 1]:
            statistics = ("After arrangement, every note was <i><b>" +
            optimal_modifier_adjective + "</b></i> by <b>" + str(abs(optimal_modifier)) + " half step</b>. These " +
            "modifications resulted in <b>" + str(percentage_of_notes_within_range_of_instrument) + "% of notes </b>" +
            "being within the specified range (" + str(lowest_note) + "-" + str(highest_note) + "). " +
            "<br><br>The remaining notes (if any) were labeled as follows in the <b>annotated</b> MIDI (.mid) files: " +
            '“i-” for increased or “d-” for decreased, followed by the number of octaves ' +
            "<b>(ex: “i-1” for increased one octave)</b>. If a note could not be brought within the range of your instrument by " +
            "further modifying its octave, is was tagged as an “outlier”. " +
            "The tags may be reviewed by opening the annotated MIDI files in a scorewriter software." +
            "<br><br>Three different sets of MIDI files (<b>with or without annotations</b>) are available for download: " +
            "<br><ul> <li>If there were at most three unmodified notes in between two identically modified notes, " +
            "the same modifications were then applied to these notes by inference. These deduced modifications were parenthesized for clarity (<b>with inferences</b>).</li>" +
            "<li>Alternatively, if a passage was strewn with modified and unmodified notes, the individual octave changes " +
            "were reversed and these notes were tagged as “O” to indicate that these outliers will need to be arranged manually (<b>with “O” outliers</b>).</li>" +
            "<li>Finally, all the notes outside the range of the instrument were modified, if possible (<b>with changes</b>).</li></ul>")
        elif octave_difference_between_piece_and_instrument == 0 and optimal_modifier == 0:
            statistics = ("Arrangement was limited to the notes not initially within the specified range (" +
            str(lowest_note) + "-" + str(highest_note) + "). " + str(percentage_of_notes_within_range_of_instrument) + "% of notes </b>" +
            "were in range (" + str(lowest_note) + "-" + str(highest_note) + ") to begin with. " +
            "<br><br>The remaining notes (if any) were labeled as follows in the <b>annotated</b> MIDI (.mid) files: " +
            '“i-” for increased or “d-” for decreased, followed by the number of octaves ' +
            "<b>(ex: “i-1” for increased one octave)</b>. If a note could not be brought within the range of your instrument by " +
            "further modifying its octave, is was tagged as an “outlier”. " +
            "The tags may be reviewed by opening the annotated MIDI files in a scorewriter software." +
            "<br><br>Three different sets of MIDI files (<b>with or without annotations</b>) are available for download: " +
            "<br><ul> <li>If there were at most three unmodified notes in between two identically modified notes, " +
            "the same modifications were then applied to these notes by inference. These deduced modifications were parenthesized for clarity (<b>with inferences</b>).</li>" +
            "<li>Alternatively, if a passage was strewn with modified and unmodified notes, the individual octave changes " +
            "were reversed and these notes were tagged as “O” to indicate that these outliers will need to be arranged manually (<b>with “O” outliers</b>).</li>" +
            "<li>Finally, all the notes outside the range of the instrument were modified, if possible (<b>with changes</b>).</li></ul>")

    else:
        if octave_difference_between_piece_and_instrument not in [-1, 0, 1] and optimal_modifier not in [-1, 0, 1]:
            statistics = ("After arrangement, all the notes were <i><b>" + octave_modification_adjective +
            "</b></i> by <b>" + str(abs(octave_difference_between_piece_and_instrument)) + " octaves</b>. After that, every note was <i><b>" +
            optimal_modifier_adjective + "</b></i> by <b>" + str(abs(optimal_modifier)) + " half steps</b>. These " +
            "modifications resulted in <b>" + str(percentage_of_notes_within_range_of_instrument) + "% of notes </b>" +
            "being within the range of the 30 note music box (F scale). " +
            "<br><br>The remaining notes (if any) were labeled as follows in the <b>annotated</b> MIDI (.mid) files: " +
            '“i-” for increased or “d-” for decreased, followed by the number of octaves ' +
            "<b>(ex: “i-1” for increased one octave)</b>. If a note could not be brought within the range of your instrument by " +
            "further modifying its octave, is was tagged as an “outlier”. " +
            "The tags may be reviewed by opening the annotated MIDI files in a scorewriter software." +
            "<br><br>Three different sets of MIDI files (<b>with or without annotations</b>) are available for download: " +
            "<br><ul> <li>If there were at most three unmodified notes in between two identically modified notes, " +
            "the same modifications were then applied to these notes by inference. These deduced modifications were parenthesized for clarity (<b>with inferences</b>).</li>" +
            "<li>Alternatively, if a passage was strewn with modified and unmodified notes, the individual octave changes " +
            "were reversed and these notes were tagged as “O” to indicate that these outliers will need to be arranged manually (<b>with “O” outliers</b>).</li>" +
            "<li>Finally, all the notes outside the range of the instrument were modified, if possible (<b>with changes</b>).</li></ul>")
        elif octave_difference_between_piece_and_instrument not in [-1, 0, 1] and optimal_modifier in [-1, 1]:
            statistics = ("After arrangement, all the notes were <i><b>" + octave_modification_adjective +
            "</b></i> by <b>" + str(abs(octave_difference_between_piece_and_instrument)) + " octaves</b>. After that, every note was <i><b>" +
            optimal_modifier_adjective + "</b></i> by <b>" + str(abs(optimal_modifier)) + " half step</b>. These " +
            "modifications resulted in <b>" + str(percentage_of_notes_within_range_of_instrument) + "% of notes </b>" +
            "being within the range of the 30 note music box (F scale). " +
            "<br><br>The remaining notes (if any) were labeled as follows in the <b>annotated</b> MIDI (.mid) files: " +
            '“i-” for increased or “d-” for decreased, followed by the number of octaves ' +
            "<b>(ex: “i-1” for increased one octave)</b>. If a note could not be brought within the range of your instrument by " +
            "further modifying its octave, is was tagged as an “outlier”. " +
            "The tags may be reviewed by opening the annotated MIDI files in a scorewriter software." +
            "<br><br>Three different sets of MIDI files (<b>with or without annotations</b>) are available for download: " +
            "<br><ul> <li>If there were at most three unmodified notes in between two identically modified notes, " +
            "the same modifications were then applied to these notes by inference. These deduced modifications were parenthesized for clarity (<b>with inferences</b>).</li>" +
            "<li>Alternatively, if a passage was strewn with modified and unmodified notes, the individual octave changes " +
            "were reversed and these notes were tagged as “O” to indicate that these outliers will need to be arranged manually (<b>with “O” outliers</b>).</li>" +
            "<li>Finally, all the notes outside the range of the instrument were modified, if possible (<b>with changes</b>).</li></ul>")
        elif octave_difference_between_piece_and_instrument not in [-1, 0, 1] and optimal_modifier == 0:
            statistics = ("After arrangement, all the notes were <i><b>" + octave_modification_adjective +
            "</b></i> by <b>" + str(abs(octave_difference_between_piece_and_instrument)) + " octaves</b>. These " +
            "modifications resulted in <b>" + str(percentage_of_notes_within_range_of_instrument) + "% of notes </b>" +
            "being within the range of the 30 note music box (F scale). " +
            "<br><br>The remaining notes (if any) were labeled as follows in the <b>annotated</b> MIDI (.mid) files: " +
            '“i-” for increased or “d-” for decreased, followed by the number of octaves ' +
            "<b>(ex: “i-1” for increased one octave)</b>. If a note could not be brought within the range of your instrument by " +
            "further modifying its octave, is was tagged as an “outlier”. " +
            "The tags may be reviewed by opening the annotated MIDI files in a scorewriter software." +
            "<br><br>Three different sets of MIDI files (<b>with or without annotations</b>) are available for download: " +
            "<br><ul> <li>If there were at most three unmodified notes in between two identically modified notes, " +
            "the same modifications were then applied to these notes by inference. These deduced modifications were parenthesized for clarity (<b>with inferences</b>).</li>" +
            "<li>Alternatively, if a passage was strewn with modified and unmodified notes, the individual octave changes " +
            "were reversed and these notes were tagged as “O” to indicate that these outliers will need to be arranged manually (<b>with “O” outliers</b>).</li>" +
            "<li>Finally, all the notes outside the range of the instrument were modified, if possible (<b>with changes</b>).</li></ul>")
        elif octave_difference_between_piece_and_instrument in [-1, 1] and optimal_modifier not in [-1, 0, 1]:
            statistics = ("After arrangement, all the notes were <i><b>" + octave_modification_adjective +
            "</b></i> by <b>" + str(abs(octave_difference_between_piece_and_instrument)) + " octave</b>. After that, every note was <i><b>" +
            optimal_modifier_adjective + "</b></i> by <b>" + str(abs(optimal_modifier)) + " half steps</b>. These " +
            "modifications resulted in <b>" + str(percentage_of_notes_within_range_of_instrument) + "% of notes </b>" +
            "being within the range of the 30 note music box (F scale). " +
            "<br><br>The remaining notes (if any) were labeled as follows in the <b>annotated</b> MIDI (.mid) files: " +
            '“i-” for increased or “d-” for decreased, followed by the number of octaves ' +
            "<b>(ex: “i-1” for increased one octave)</b>. If a note could not be brought within the range of your instrument by " +
            "further modifying its octave, is was tagged as an “outlier”. " +
            "The tags may be reviewed by opening the annotated MIDI files in a scorewriter software." +
            "<br><br>Three different sets of MIDI files (<b>with or without annotations</b>) are available for download: " +
            "<br><ul> <li>If there were at most three unmodified notes in between two identically modified notes, " +
            "the same modifications were then applied to these notes by inference. These deduced modifications were parenthesized for clarity (<b>with inferences</b>).</li>" +
            "<li>Alternatively, if a passage was strewn with modified and unmodified notes, the individual octave changes " +
            "were reversed and these notes were tagged as “O” to indicate that these outliers will need to be arranged manually (<b>with “O” outliers</b>).</li>" +
            "<li>Finally, all the notes outside the range of the instrument were modified, if possible (<b>with changes</b>).</li></ul>")
        elif octave_difference_between_piece_and_instrument in [-1, 1] and optimal_modifier in [-1, 1]:
            statistics = ("After arrangement, all the notes were <i><b>" + octave_modification_adjective +
            "</b></i> by <b>" + str(abs(octave_difference_between_piece_and_instrument)) + " octave</b>. After that, every note was <i><b>" +
            optimal_modifier_adjective + "</b></i> by <b>" + str(abs(optimal_modifier)) + " half step</b>. These " +
            "modifications resulted in <b>" + str(percentage_of_notes_within_range_of_instrument) + "% of notes </b>" +
            "being within the range of the 30 note music box (F scale). " +
            "<br><br>The remaining notes (if any) were labeled as follows in the <b>annotated</b> MIDI (.mid) files: " +
            '“i-” for increased or “d-” for decreased, followed by the number of octaves ' +
            "<b>(ex: “i-1” for increased one octave)</b>. If a note could not be brought within the range of your instrument by " +
            "further modifying its octave, is was tagged as an “outlier”. " +
            "The tags may be reviewed by opening the annotated MIDI files in a scorewriter software." +
            "<br><br>Three different sets of MIDI files (<b>with or without annotations</b>) are available for download: " +
            "<br><ul> <li>If there were at most three unmodified notes in between two identically modified notes, " +
            "the same modifications were then applied to these notes by inference. These deduced modifications were parenthesized for clarity (<b>with inferences</b>).</li>" +
            "<li>Alternatively, if a passage was strewn with modified and unmodified notes, the individual octave changes " +
            "were reversed and these notes were tagged as “O” to indicate that these outliers will need to be arranged manually (<b>with “O” outliers</b>).</li>" +
            "<li>Finally, all the notes outside the range of the instrument were modified, if possible (<b>with changes</b>).</li></ul>")
        elif octave_difference_between_piece_and_instrument in [-1, 1] and optimal_modifier == 0:
            statistics = ("After arrangement, all the notes were <i><b>" + octave_modification_adjective +
            "</b></i> by <b>" + str(abs(octave_difference_between_piece_and_instrument)) + " octave</b>. These " +
            "modifications resulted in <b>" + str(percentage_of_notes_within_range_of_instrument) + "% of notes </b>" +
            "being within the range of the 30 note music box (F scale). " +
            "<br><br>The remaining notes (if any) were labeled as follows in the <b>annotated</b> MIDI (.mid) files: " +
            '“i-” for increased or “d-” for decreased, followed by the number of octaves ' +
            "<b>(ex: “i-1” for increased one octave)</b>. If a note could not be brought within the range of your instrument by " +
            "further modifying its octave, is was tagged as an “outlier”. " +
            "The tags may be reviewed by opening the annotated MIDI files in a scorewriter software." +
            "<br><br>Three different sets of MIDI files (<b>with or without annotations</b>) are available for download: " +
            "<br><ul> <li>If there were at most three unmodified notes in between two identically modified notes, " +
            "the same modifications were then applied to these notes by inference. These deduced modifications were parenthesized for clarity (<b>with inferences</b>).</li>" +
            "<li>Alternatively, if a passage was strewn with modified and unmodified notes, the individual octave changes " +
            "were reversed and these notes were tagged as “O” to indicate that these outliers will need to be arranged manually (<b>with “O” outliers</b>).</li>" +
            "<li>Finally, all the notes outside the range of the instrument were modified, if possible (<b>with changes</b>).</li></ul>")
        elif octave_difference_between_piece_and_instrument == 0 and optimal_modifier not in [-1, 0, 1]:
            statistics = ("After arrangement, every note was <i><b>" +
            optimal_modifier_adjective + "</b></i> by <b>" + str(abs(optimal_modifier)) + " half steps</b>. These " +
            "modifications resulted in <b>" + str(percentage_of_notes_within_range_of_instrument) + "% of notes </b>" +
            "being within the range of the 30 note music box (F scale). " +
            "<br><br>The remaining notes (if any) were labeled as follows in the <b>annotated</b> MIDI (.mid) files: " +
            '“i-” for increased or “d-” for decreased, followed by the number of octaves ' +
            "<b>(ex: “i-1” for increased one octave)</b>. If a note could not be brought within the range of your instrument by " +
            "further modifying its octave, is was tagged as an “outlier”. " +
            "The tags may be reviewed by opening the annotated MIDI files in a scorewriter software." +
            "<br><br>Three different sets of MIDI files (<b>with or without annotations</b>) are available for download: " +
            "<br><ul> <li>If there were at most three unmodified notes in between two identically modified notes, " +
            "the same modifications were then applied to these notes by inference. These deduced modifications were parenthesized for clarity (<b>with inferences</b>).</li>" +
            "<li>Alternatively, if a passage was strewn with modified and unmodified notes, the individual octave changes " +
            "were reversed and these notes were tagged as “O” to indicate that these outliers will need to be arranged manually (<b>with “O” outliers</b>).</li>" +
            "<li>Finally, all the notes outside the range of the instrument were modified, if possible (<b>with changes</b>).</li></ul>")
        elif octave_difference_between_piece_and_instrument == 0 and optimal_modifier in [-1, 1]:
            statistics = ("After arrangement, every note was <i><b>" +
            optimal_modifier_adjective + "</b></i> by <b>" + str(abs(optimal_modifier)) + " half step</b>. These " +
            "modifications resulted in <b>" + str(percentage_of_notes_within_range_of_instrument) + "% of notes </b>" +
            "being within the range of the 30 note music box (F scale). " +
            "<br><br>The remaining notes (if any) were labeled as follows in the <b>annotated</b> MIDI (.mid) files: " +
            '“i-” for increased or “d-” for decreased, followed by the number of octaves ' +
            "<b>(ex: “i-1” for increased one octave)</b>. If a note could not be brought within the range of your instrument by " +
            "further modifying its octave, is was tagged as an “outlier”. " +
            "The tags may be reviewed by opening the annotated MIDI files in a scorewriter software." +
            "<br><br>Three different sets of MIDI files (<b>with or without annotations</b>) are available for download: " +
            "<br><ul> <li>If there were at most three unmodified notes in between two identically modified notes, " +
            "the same modifications were then applied to these notes by inference. These deduced modifications were parenthesized for clarity (<b>with inferences</b>).</li>" +
            "<li>Alternatively, if a passage was strewn with modified and unmodified notes, the individual octave changes " +
            "were reversed and these notes were tagged as “O” to indicate that these outliers will need to be arranged manually (<b>with “O” outliers</b>).</li>" +
            "<li>Finally, all the notes outside the range of the instrument were modified, if possible (<b>with changes</b>).</li></ul>")
        elif octave_difference_between_piece_and_instrument == 0 and optimal_modifier == 0:
            statistics = ("Arrangement was limited to the notes not initially within the specified range (" +
            str(lowest_note) + "-" + str(highest_note) + "). " + str(percentage_of_notes_within_range_of_instrument) + "% of notes </b>" +
            "were within the range of the 30 note music box (F scale) to begin with. " +
            "<br><br>The remaining notes (if any) were labeled as follows in the <b>annotated</b> MIDI (.mid) files: " +
            '“i-” for increased or “d-” for decreased, followed by the number of octaves ' +
            "<b>(ex: “i-1” for increased one octave)</b>. If a note could not be brought within the range of your instrument by " +
            "further modifying its octave, is was tagged as an “outlier”. " +
            "The tags may be reviewed by opening the annotated MIDI files in a scorewriter software." +
            "<br><br>Three different sets of MIDI files (<b>with or without annotations</b>) are available for download: " +
            "<br><ul> <li>If there were at most three unmodified notes in between two identically modified notes, " +
            "the same modifications were then applied to these notes by inference. These deduced modifications were parenthesized for clarity (<b>with inferences</b>).</li>" +
            "<li>Alternatively, if a passage was strewn with modified and unmodified notes, the individual octave changes " +
            "were reversed and these notes were tagged as “O” to indicate that these outliers will need to be arranged manually (<b>with “O” outliers</b>).</li>" +
            "<li>Finally, all the notes outside the range of the instrument were modified, if possible (<b>with changes</b>).</li></ul>")

else:
    if lowest_note != None and highest_note != None:
        statistics = "Every note of the music piece was already within the specified range (" + str(lowest_note) + "-" + str(highest_note) + ")!"
    else:
        statistics = "Every note of the music piece was already within the specified range!"


print(json.dumps(statistics))
