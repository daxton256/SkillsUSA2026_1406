def process_keystrokes(string):
    recreated_string = ""
    for l in string:
        if l == "#": #Check if character is backspace
            recreated_string = recreated_string[:-1] #Remove last element of recreated string
            continue #Starting next iteration
        
        recreated_string += l #Adding non backspaces to recreated string

    return recreated_string

print("Task 1 - Text Editor Backspace")
string1 = input("String 1: ")
string2 = input("String 2: ")
match = (process_keystrokes(string1) == process_keystrokes(string2))
print(f"The strings {'are a' if match else 'do not'} match.")