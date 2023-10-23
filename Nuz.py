import numpy as np
import hjson
import argparse


class Pokemon:
    def __init__(self, id, area, species, nickname, status="Team"):
        self.id = id
        self.area = area 
        self.species = species
        self.nickname = nickname 
        self.status = status
    def __str__(self):
        return (f"ID: {self.id}, Species: {self.species}, Nickname: {self.nickname}, Origin: {self.area}, Status: {self.status}")

def edition_selection(edition):
    if(edition):
        edition = edition.replace(" ","_")
    if(edition in allEditions):
        print(f" Used Edition: {edition}")
        return edition
    elif(edition):
        print(f" Edition {edition} is not featured. Please select from the following:\n")
    elif(not edition):
        print("Please select your Edition from the following list:")
        for e in allEditions:
            print(f" {e}") 
    edition = edition_selection(input("Enter edition..."))
    return edition

def boot(edition):
    try:
        edition_stats = hjson.load(open('stats.json'))[edition]
        run_Number = edition_stats["run_Number"]

    except:
        print("No stats file found, creating new stats...")
        run_Number = 1

    _e = edition.replace("_", " ")
    print(f" NuzLocke Run of Pokemon {_e}:")
    print(f" Run Number: {run_Number}")
    pokemon = []

    try:
        pokemon_dict = edition_stats["pokemon"]
        for id in pokemon_dict:
            pokemon.append(Pokemon(pokemon_dict[id]["id"], pokemon_dict[id]["area"], pokemon_dict[id]["species"], pokemon_dict[id]["nickname"], status=pokemon_dict[id]["status"]))
    except: 
        print(" There are currently no Pokemon in your list.\n Would you like to add one? [Y/N]")
        _l = input()
        if(_l.upper()=="Y"):
            add_pokemon(pokemon)
        else:
            print("Oh poopie")
    return pokemon, run_Number

def list_pokemon(pokemon):
    if(len(pokemon)==0):
        print("You currently have no Pokemon :(\n")
        return
    print("\n These are your Pokemon:\n") 
    print("ID     Nickname         Origin                   Status")
    print("_______________________________________________________\n")
    max_lenghts = [2, 12, 20, 6]
    for p in pokemon:
        _print_attr = [str(p.id), p.nickname, p.area, p.status]
        for i,attr in enumerate(_print_attr):
            for j in range(max_lenghts[i]-len(attr)+4):
                _print_attr[i] = _print_attr[i]+" "        
        print(f"{_print_attr[0]} {_print_attr[1]} {_print_attr[2]} {_print_attr[3]}")
    print("_______________________________________________________\n")
    return

def find_pokemon(pokemon, string):
    for p in pokemon:
        if(string==str(p.id) or string==p.nickname or string==p.species or string==p.area):
            return p.id 
    return

def add_pokemon(pokemon):
    print("Adding a New Pokemon:")
    id = len(pokemon)
    
    n = input("Type pokemon species...")
    nick = input("Type pokemon nickname...")
    if(len(nick)>12):
        print("Invalid Nickname")
        return pokemon
    if(find_pokemon(pokemon,nick)):
        print("Nickname already taken")
        return pokemon
    a = input("Type origin...")
    if(len(a)>20):
        print("Invalid Area")
        return pokemon
    if(find_pokemon(pokemon,a)):
        print("You already caught a Pokemon in this area.")
        return pokemon
    pkm = Pokemon(id, a, n, nick)
    pokemon.append(pkm)
    print(f" Successfully added the following:\n {pkm}") 
    return pokemon  

def add_fail(pokemon):
    print("Adding a failed Route:")
    a = input("Type failed Route...")
    if(find_pokemon(pokemon,a)):
        print("You already caught a Pokemon in this area.")
        return pokemon
    id = len(pokemon)
    pkm = Pokemon(id, a, "-", "-", status = "failed")
    pokemon.append(pkm)
    print(f"Added {a} as a failed Route")
    return pokemon


def kill_pokemon(pid):
    for p in pokemon:
        if(pid == p.id):
            p.status = "Dead"
            print(f"Killed {p.nickname}.")
            return
    print("No Pokemon found in that list")
    return

def change_box_status(pid):
    for p in pokemon:
        if(pid == p.id):
            if p.status=="boxed":
                p.status="Team"
                print(f"Changed {p.nickname} to your team")
            elif p.status=="Team":
                p.status="boxed"
                print(f"Boxed {p.nickname} to your computer")
            return
    print("No Pokemon found in that list")
    return


def input_loop(pokemon, endbool): 
    print("Choose your next action (type help for listing all options)")  
    action = input(" ")
    if(action=="help"):
        print("\nlist:           List all your pokemon")
        print("list team:      List all your Team pokemon")
        print("list boxed:     List all your boxed pokemon")
        print("list dead:      List all your dead  pokemon")
        print("list failed:    List all your dead  pokemon\n")
        print("show:           Show details of a specific pokemon\n")

        print("add:            Add a pokemon to your List")
        print("add fail:       Add a route where you failed to catch your pokemon")
        print("box:            Changes box status of a pokemon (boxed <-> Team)")
        print("kill:           Change the status of a pokemon of your list to dead")
        print("change:         Manually Change an attribute of a Pokemon\n")

        print("exit:           Save every change and exit NuzLocke\n")

    if(action=="list"):
        list_pokemon(pokemon)
    if(action=="list team"):
        _team = []
        for p in pokemon:
            if p.status == "Team":
                _team.append(p)
        list_pokemon(_team)
    if(action=="list boxed"):
        _team = []
        for p in pokemon:
            if p.status == "boxed":
                _team.append(p)
        list_pokemon(_team)
    if(action=="list dead"):
        _team = []
        for p in pokemon:
            if p.status == "dead":
                _team.append(p)
        list_pokemon(_team)
    if(action=="list failed"):
        _team = []
        for p in pokemon:
            if p.status == "failed":
                _team.append(p)
        list_pokemon(_team)

    if(action=="show"):
        _s = input("Enter ID, Nickname or species...")
        _id = find_pokemon(pokemon,_s)
        print("\n",pokemon[_id],"\n")

    if(action=="add"):
        add_pokemon(pokemon)
    if(action=="add fail"):
        add_fail(pokemon)
    if(action=="kill"):
        _to_kill = input("What Pokemon do you want to kill?...")
        _to_kill = find_pokemon(pokemon,_to_kill)
        kill_pokemon(_to_kill)
    if(action=="box"):
        _to_box = input("What Pokemon do you want (Un)box?...")
        print(_to_box)
        _to_box = find_pokemon(pokemon,_to_box)
        change_box_status(_to_box)
    if(action=="exit"):
        endbool=1
    return pokemon, endbool  
   
def saveAll(edition, pokemon,  run_Number, hjson_dict):
    pokemon_dict = {}
    for _p in pokemon:
       _pdict = {"id": _p.id, "nickname": _p.nickname, "species": _p.species, "area": _p.area, "status": _p.status}
       pokemon_dict[_p.id] = _pdict
    hjson_dict[edition] = {"run_Number": run_Number, "pokemon": pokemon_dict}
    with open("stats.json", "w") as outfile: 
        hjson.dump(hjson_dict, outfile)
    return



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Interactive Tracking Tool for Nuzlocke Challanges")
    parser.add_argument("-edition", default = None, help="Possible Editions: Omega_Ruby, Ruby")
    args = parser.parse_args()

    edition = args.edition
    allEditions = ["OmegaRuby", "Ruby"]

    print("\n######################################################")
    print("############     Welcome to NuzLocke!     ############")
    print("######################################################\n")

    edition = edition_selection(edition)

    pokemon, run_Number = boot(edition)
    endbool = 0
    while(endbool == 0):
        pokemon, endbool = input_loop(pokemon, endbool)

    hjson_dict = {}
    _dic = hjson.load(open('stats.json'))
    for _e in _dic:
        hjson_dict[_e] = _dic[_e]
    
    saveAll(edition, pokemon, run_Number, hjson_dict)

    print("\n######################################################")
    print("########     Thank you for using NuzLocke     ########")
    print("########              Goodbye <3              ########")
    print("######################################################\n")

