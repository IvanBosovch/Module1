#цей файл потрібний для роботи з асистентом без установки. Він не прописаний в setup.py, він та і не потрібен.
# При установці буде використовуватися той що в папці group2. 
from group2.servicenote import OPERATORS
from group2.service_addressbook import FUNCTIONS, EXIT
from group2.terminal_tips import my_input

COMMANDS = {}
COMMANDS.update(EXIT)
COMMANDS.update(OPERATORS)
COMMANDS.update(FUNCTIONS)
COMMANDS = dict(sorted(COMMANDS.items(), reverse=True))

def parser(text: str):
    for func in COMMANDS.keys():
        if text.startswith(func):
            return func, text[len(func) :].strip().split()

def main():
    while True:
        user_input = my_input()
        func, data = parser(user_input.lower())
        current_func = COMMANDS.get(func)
        print(current_func(*data))


if __name__ == "__main__":
    main()