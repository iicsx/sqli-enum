def banner():
    print(r"╭───────────────────────────────────────────────────────╮")
    print(r"│                                                       │")
    print(r"│     _____  _____ _     _ _____ _   _ _   ____  ___    │")
    print(r"│    /  ___||  _  | |   (_)  ___| \ | | | | |  \/  |    │")
    print(r"│    \ `--. | | | | |    _| |__ |  \| | | | | .  . |    │")
    print(r"│     `--. \| | | | |   | |  __|| . ` | | | | |\/| |    │")
    print(r"│    /\__/ /\ \/' / |___| | |___| |\  | |_| | |  | |    │")
    print(r"│    \____/  \_/\_\_____/_\____/\_| \_/\___/\_|  |_/    │")
    print(r"│                                                       │")
    print(r"╰───────────────────────────────────────────────────────╯")
    print(r"")


def usage():
    print("WIP")
    print("SQL Enum - v.0.1")
    print("")
    print("Examples:")
    print("    <script_name> -u http://192.168.1.2/login?name=FUZZ&password='' -s 'Successfully logged in' -e 'Incorrect credentials'")


def error(reason):
    print(r"An error occurred:")
    print(reason)


def column_error():
    print("\n[x] Could not get SQL version")
    print(r" │  Did you mistmatch the column number?")
    print(r" │  Try omitting it to run in brute-force mode")
    print(r" ╰─ This will determine the number of columns automatically at the cost of increased traffic")
