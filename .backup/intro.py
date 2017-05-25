#!/user/bin/env python3 -tt
#File: intro.py 

def print_questions():
    print("What is your name?")
    print("What is your quest?")
    print("What do you do in your free time?")
    print("What else would you like to tell us that you haven't already expressed through the application?")
    print("What are you most excited to learn about this quarter?")

if __name__ == '__main__': 
    input = input("Ask me a question: ")
    if input == "What is your name?":
        print("The name is Mr. Powers, Austin Powers, baby.")
    elif input == "What is your quest?":
        print("To save the world… and to shag, baby!")
    elif input == "What do you do in your free time?":
        print("Spend time with my dad… and shag, baby!")
    elif input == "What else would you like to tell us that you haven't already expressed through the application?":
        print("Daddy wasn’t there, to take me to the fair.")
    elif input == "What are you most excited to learn about this quarter?":
        print("How I might make my member gold.")
    elif input == "What can you answer?":
        print_questions()
    else: 
        print("I don't know what you mean... that's not groovy, baby!")