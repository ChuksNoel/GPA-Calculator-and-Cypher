from time import sleep
gradepoint = {
    'A': 5,
    'B': 4,
    'C': 3,
    'D': 2,
    'F': 0,
}
colors = {
    'green':'\033[92m',
    'red':'\033[91m',
    'yellow':'\033[93m',
    'blue':'\033[94m',
    'cyan':'\033[96m',
    'reset':'\033[0m',
    'bold':'\033[1m',
    'underline':'\033[4m',
    'bg_red':'\033[41m',
}
courses = []
inputs = ''
index = -1

def s_print(*args, end='\n', sep=' ', file=None, flush=True, t=0.01) -> None: #Prints with intuition💖
    "Print with a delay between each character."
    for arg in args:
        for text in arg:
            print(text, end='', sep=sep, file=file, flush=flush)
            sleep(t)
    print(end=end, sep=sep, file=file, flush=flush)

def bksp(n=1, t=.01) -> None: #Backspaces technically
    for _ in range(n):
        print('\b \b', end='', flush=True)
        sleep(t)

def move_cursor_up(length_of_chatacters) -> None: #Guess what this function does 😊
    print(f"\033[A\033[{length_of_chatacters}C", end='', flush=True)

def get_gradepoint(grade) -> int|bool: #Returns the gradepoint of each grade (A -> F) regardless of the letter case
    "Get the grade point for a given grade."
    return gradepoint.get(grade.upper(), False)

def find_gpa(courses: list[str, int, str]) -> list[int, int, float]: #Returns the total weighted score, total units and the gpa
    '''Return the gpa of the courses'''
    total_scores = total_units = 0
    for name, weight, grade in courses:
        total_scores += get_gradepoint(grade) * weight
        total_units += weight
    
    return total_scores, total_units, total_scores/total_units

def show_courses(courses) -> None: #Prints the output to the terminal
    print("Name/Code\tUnit\tGrade")
    for sn, course in enumerate(courses):
        name, units, grade = course
        print(f"{sn}. {name}\t{units}\t{grade.upper()}")


def convert_cypher(string, number_displacement=0): #Caesar cypher function
    '''Converts a string using a Caesar cipher with a given displacement.'''
    new_string = ''
    for character in string:
        if character.isalpha():
            if character.isupper():
                new_character = chr((ord(character) - 65 + number_displacement) % 26 + 65)
            else:
                new_character = chr((ord(character) - 97 + number_displacement) % 26 + 97)
        else:
            new_character = character
        new_string += new_character
    return new_string

def convert_cypher_full(string, number_displacement=0): #Absolute cypher function
    new_string = ''
    for character in string:
        new_string += chr((ord(character) + number_displacement) % 1114111) #That's the maximum unicode character
    return new_string


def main1(): #The gpa calculator main function
    global inputs, courses
    s_print(" "*10 + colors['green'] + colors['bold'] + colors['underline'] + "GPA Calculator" + colors['reset'], t=.01)
    s_print(
        colors['blue'] + colors['bold'] + colors['underline'],
        "Welcome to the GPA calculator!",
        t=.01)
    sleep(.5)
    s_print(
        'Here we calculate your gpa and give you a result',
        colors['reset'],
        t=.01)

    while inputs != 'done':
        if not inputs:
            s_print(
                colors['yellow'] + "Enter course name and/or course code (or 'done' to finish):  " + colors['reset'],
                t=0.01, end='')
            inputs = input()

        if 'done' in inputs.lower() and len(inputs) < 5:
            s_print(colors['cyan']+ "Are you sure you're done? (yes/no): "+colors['reset'], t=0.01, end='')
            inputs = input().lower()

            if inputs in ('y', 'ye', 'yes', 'yeah') or 'y' in inputs:
                s_print(colors['green'] + "Okay😊 Getting your grade now!" + colors['reset'], t=0.01)
                inputs = 'done'
                continue
            elif inputs in ('n', 'no', 'nah') or 'n' in inputs:
                s_print(colors['red'] + "Okay! Let's continue!" + colors['reset'], t=0.01)
                inputs = ''
                continue

        elif not inputs:
            move_cursor_up(50)
            bksp(50, .01)
            s_print("Please enter a course name or code.")
            move_cursor_up(35)
            sleep(.5)
            bksp(35, .01)
            sleep(.5)
            continue

        else:
            if (courses and len(courses[-1]) in (1, 3)) or not courses:
                courses.append([inputs]) if not courses or len(courses[-1]) == 3 else None
                move_cursor_up(50 + len(inputs))
                bksp(50 + len(inputs), .01)
                sleep(.3)
                s_print(colors['cyan'] + f"   How many units is this course ({inputs})? " + colors['reset'], t=0.01, end='')
                inputs = input()

            try:
                match len(courses[-1]):
                    case 1: courses[-1].append(int(inputs))
                    case 2: pass
                    case 3: raise Exception

            except ValueError:
                move_cursor_up(50 + len(inputs))
                bksp(50 + len(inputs), .01)
                s_print(colors['bg_red'] + "Please enter a course name or code..." + colors['reset'])
                inputs = courses[-1][0]
                print(inputs, courses)
                sleep(1)
                continue
            except Exception as e: pass
            
            else:
                move_cursor_up(40 + len(inputs))
                bksp(40 + len(inputs), .01)
                s_print(colors['green'], f"What grade (A, B, C, D, F) did you get in the course ({courses[-1][0]})? " + colors['reset'], end='')
                inputs = input().upper()
                move_cursor_up(57 + len(courses[-1][0]) + len(inputs))
                bksp(57 + len(courses[-1][0]) + len(inputs), .01)
                if get_gradepoint(inputs) is False:
                    s_print(colors['bg_red'] + 'please Enter a correct grade (a -> f or A -> F)' + colors['reset'])
                    sleep(1)
                else:
                    courses[-1].append(inputs)
                    s_print(colors['bold'] + colors['green'] + f"Course{len(courses)} inputted! Moving on..." + colors['reset'])
                    move_cursor_up(29 + len(str(len(courses))))
                    inputs = ''
                    sleep(.7)
                    bksp(29 + len(str(len(courses))))
                    sleep(.7)

    s_print('these are the courses you offered with their respective grade')
    show_courses(courses)
    result = find_gpa(courses)
    s_print(f'Your GPA is {round(result[2], 2)}', t=0.05)
    sleep(.5)
    s_print(colors['green'] + colors['bold'] + colors['reverse'] + "Thank you for using the GPA calculator!" + colors['reset'], '😏', t=0.05)
    move_cursor_up(39)
    sleep(1)
    bksp(39)
    s_print(colors['cyan'] + colors['bg_red']+ 'Goodbye...' + colors['reset'], '\t🥲', t=.1)


def main2():
    word = "Chukwunonso"
    s_print(f"{colors['bg_red'] + colors['green']}The Caesar Cypher of my name, {word} displaced by 13 is {convert_cypher(word, 13)}{colors['reset']}")
    sleep(1)
    s_print(f"{colors['bg_red'] + colors['green']}The absolute Cypher of my name, {word} displaced by 13 is {convert_cypher_full(word, 13)}{colors['reset']}")
    sleep(1)
    s_print(colors['cyan'] + colors['bg_red']+ 'Goodbye...' + colors['reset'], '\t🥲', t=.1)

if __name__ == '__main__':
    # main1()
    main2()
