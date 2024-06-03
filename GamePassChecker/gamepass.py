import json
import requests
import sys
from tabulate import tabulate
import re


def main():

    show_option_table()

    user_option = validate_user_option(input("Please Enter An Option Number To Search Through: "))
    user_search = validate_user_search(input("Please Enter A Game Name: "))
    print(f"Searching...\n")

    link = get_link(user_option)
    game_ids_list = get_game_ids(link)
    game_list = get_game_list(game_ids_list)
    #print(game_list)
    results_list = compare_search_and_game_list(user_search, game_list)

    option_output = generate_option_output(user_option)
    result_output = generate_result_output(user_search, results_list)

    print(f"{option_output}\n{result_output}")

    if len(results_list) > 1:
        for num, item in enumerate(results_list):
            print(f"{num}) {item}")

    print(f"\n")

# Generates an options table when the program runs, prompting the user to enter in one of the numbers corresponding to an option.
def show_option_table():
    table = {
        "Option": ["1", "2", "3"],
        "Filter": ["Game Pass Console", "Game Pass PC", "Exit"],
    }

    formatted_table = tabulate(
        table, headers="keys", tablefmt="grid", numalign="center", stralign="center"
    )
    print("\n", formatted_table, "\n", sep="")


# Returns the option that the user enters from the option table. Attempts to make sure that only valid options (currently 1,2, and 3) are entered.
def validate_user_option(s):

    while True:
        try:
            if 1 <= int(s.strip()) <= 2:
                return s.strip()
            elif int(s.strip()) == 3:
                sys.exit("You Have Chosen To Exit")
            else:
                print("Not An Available Option.")
                s = input("Please Enter An Option Number To Search Through: ")
        except ValueError:
            print("Not An Available Option.")
            s = input("Please Enter An Option Number To Search Through: ")


# Returns the game name that the user wants to search for in a list. Removes whitepsace from beginning and end and checks to make sure something was entered.
def validate_user_search(s):

    while True:
        if s.strip() == "":
            print("Nothing Entered.")
            s = input("Please Enter A Game Name: ")
        else:
            return s.strip().split(" ")


# Returns a link with a dictionary of IDs to be parsed through based on the user's choice.
def get_link(table_option):

    # Returns a list of IDs for all Game Pass games available on console.
    if table_option == "1":
        return "https://catalog.gamepass.com/sigls/v2?id=f6f1f99f-9b49-4ccd-b3bf-4d9767a77f5e&language=en-us&market=US"
    # Returns a list of IDs for all Game Pass games available on PC.
    elif table_option == "2":
        return "https://catalog.gamepass.com/sigls/v2?id=fdd9e2a7-0fee-49f6-ad69-4354098401ff&language=en-us&market=US"


# Parses through the .json link with the dictionaries of IDs and returns a list of just the relevant game IDs.
def get_game_ids(link):

    game_id_list = []

    response = requests.get(link)
    # print(json.dumps(response.json(), indent=2))

    o = response.json()

    for _ in o:
        for k, v in _.items():
            if k == "id":
                game_id_list.append(v)

    return game_id_list


# For each game ID in the list of IDs, uses that ID to generate a link which contains all the details of that game, then finds just the name of the game and adds it to a list, eventaully returning that full list of games.
def get_game_list(id_list):

    game_list = []

    for _ in id_list:
        response = requests.get(f"https://displaycatalog.mp.microsoft.com/v7.0/products?bigIds={_}&market=US&languages=en-us&MS-CV=DGU1mcuYo0WMMp")
        o = response.json()
        game_list.append(o["Products"][0]["LocalizedProperties"][0]["ProductTitle"])
        # print(o["Products"][0]["LocalizedProperties"][0]["ProductTitle"])

    return game_list


# Compares the game name list that the user searched for with each game in the game list. If any part of the user input is found in any of the games, the full game name is added to a new list, which is returned.
def compare_search_and_game_list(search, game_list):

    results_list = []
    #print(" ".join(search))

    for _ in game_list:
        if " ".join(search).lower() == _.lower():
            #print(_.lower())
            results_list.append(_)
            return results_list

    for _ in game_list:
        for s in search:
            if s.lower() in _.lower():
                if _ not in results_list:
                    results_list.append(_)

    #print(results_list)
    return results_list


# Generates the first line of the final output, which basically reminds the user which option they searched for.
def generate_option_output(option):

    if option == "1":
        return "For Game Pass games available on Console:"
    elif option == "2":
        return "For Game Pass games available on PC:"


# Generates the second line of the final output, which gives more detail about what the program found. Can vary depending on the amount of matches or if an exact match was found.
def generate_result_output(search, results_list):

    if len(results_list) == 0:
        return "No Matches Found"
    elif len(results_list) == 1:
        for _ in results_list:
            for s in search:
                if " ".join(search).lower() == _.lower():
                    return f"Found An Exact Match! '{_}' is on the list of available games."
                else:
                    return f"No Exact Match. However, '{_}' is on the list of available games."
    elif len(results_list) > 1:
        return "No Exact Match. However, here is a list of games close to your search:\n"


if __name__ == "__main__":
    main()
