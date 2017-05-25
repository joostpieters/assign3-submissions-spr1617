#!/usr/bin/env python3 -tt
# Assignment 0 of CS41
# Due April 11, 2017

question = input("Ask me a question: ")

questions_answers = {
"What is your name?": "Mamadou",
"What is your quest?": "To eradicate poverty",
"What do you do in your free time?": "I like to play basketball, make curriculum, and plan events.",
"What else would you like to tell us that you haven't already expressed through the application?": "I have 9 siblings :) ",
"What are you most excited to learn about this quarter?": "I'm excited to learn more about what other Stanford students, especially upperclassmen, have done with their time at Stanofrd"
}

if question == "What can you answer?":
    for item in questions_answers.keys():
        print(item)
else:
    print(questions_answers.get(question, "What do you mean? I don't recognize your question."))
