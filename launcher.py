import os
import sys
import subprocess
from simple_term_menu import TerminalMenu


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_menu(options):
    menu = TerminalMenu(options)
    return menu.show()


def launch_task(path: str):
    clear_console()

    subprocess.run([sys.executable, path])
    input("\nPress Enter to return to the launcher.")


def main():
    while True:
        clear_console()
        print("Task Launcher")
        options = [
            "Task 1 - Launch Task 1/main.py",
            "Task 2 - Launch Task 2/main.py",
            "Task 3 - Launch Task 3/main.py",
            "Exit",
        ]

        choice = show_menu(options)

        match choice:
            case 0:
                launch_task(os.path.join("Task 1", "main.py"))
            case 1:
                launch_task(os.path.join("Task 2", "main.py"))
            case 2:
                launch_task(os.path.join("Task 3", "main.py"))
            case 3:
                clear_console()
                break


if __name__ == "__main__":
    main()

