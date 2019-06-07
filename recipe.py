import json
import os

from color import Color as c


class Recipe(object):
    """ Object for storing recipe information and methods
    """
    def __init__(self, recipe_name=None, recipe_dir='~/recipes/'):
        self.recipe_dir = recipe_dir
        if recipe_name:
            with open(os.path.expanduser(recipe_dir+recipe_name+'.json')) as f:
                data = json.load(f)
            requirements = ['name', 'ingredients', 'steps']
            if not all(requirement in data for requirement in requirements):
                raise Exception("Recipe is missing a required field!")
            self.name = data['name']
            self.ingredients = data['ingredients']
            self.steps = data['steps']
            self.tags = data['tags'] if 'tags' in data else None
            self.description = data['description'] if 'description' in data else None
        else:
            self.new_recipe()

    def new_recipe(self):
        """ Ask the user about the new recipe then save it to a json file
        """
        os.system("clear")
        self.name = input("Recipe Name: ")
        self.ingredients = None
        self.steps=None
        self.description = None
        self.tags = {}
        self.edit_ingredients()
        self.edit_steps()
        if _yes_no_select("Would you like to add a description?"):
            self.description = input("Description: ")
        self.edit_tags()
        while not self.check():
            continue

    def edit_ingredients(self):
        if self.ingredients:
            while True:
                ingredients = [ingredient for ingredient in self.ingredients.keys()]
                ingredients.append("Add Ingredients")
                ingredients.append("No Change")
                os.system("clear")
                self.print_ingredients()
                _, key = _num_select("Which ingredient would you like to edit?",
                                     ingredients)
                if key == "No Change":
                    return
                if key == "Add Ingredients":
                    self.ingredients.update(_get_list_response(data_type='dict', primary_name='Ingredient'))
                else:
                    print("Leave blank for no change")
                    primary = input("Ingredient: ")
                    secondary = input("Quantity: ")
                    if primary:
                        del self.ingredients[key]
                        self.ingredients[primary] = secondary
                    elif secondary:
                        self.ingredients[key] = secondary
        else:
            self.ingredients = _get_list_response(data_type='dict', primary_name='Ingredient')

    def edit_steps(self):
        if self.steps:
            while True:
                steps = self.steps.copy()
                steps.append("Add Steps")
                steps.append("No Change")
                os.system("clear")
                self.print_steps()
                ind, key = _num_select("Which step would you like to edit?",
                                       steps)
                if key == "No Change":
                    return
                if key == "Add Steps":
                    self.steps += _get_list_response()
                else:
                    print("Leave blank for no change")
                    self.steps[ind] = input("Step: ")
        else:
            self.steps = _get_list_response()

    def edit_tags(self):
        """ edit tags for a recipe
        """
        os.system("clear")
        while True:
            tag_categories = ["meal", "genre", "complexity", "course", "no change"]
            _, key = _num_select("Which tag would you like to edit", tag_categories)
            if key == "meal":
                _, value = _num_select("Which tag would you like to apply",
                                     ["breakfast", "lunch", "dinner"])
                self.tags[key]=value
            elif key == "genre":
                genres = ["american", "italian", "mexican", "asian", "indian", "misc"]
                _, value = _num_select("Which tag would you like to apply",
                                       genres)
            elif key == "complexity":
                _, value = _num_select("Which tag would you like to apply",
                                       ["simple", "intermediate", "complicated"])
            elif key == "course":
                _, value = _num_select("Which tag would you like to apply",
                                       ["appetizer", "salad", "side", "main", "dessert"])
            else:
                return

    def check(self):
        """ Check if everything is entered correctly and ask for any changes
        """
        os.system("clear")
        self.print()
        print("\n")
        _, response = _num_select("Would you like to make any changes?",
                                  ["Name", "Ingredients", "Steps", "Description", "Tags", "No"])
        if response == "Name":
            self.name = input("Recipe Name: ")
            print("New name is: " + self.name)
            return False
        elif response == "Ingredients":
            self.edit_ingredients()
            return False
        elif response == "Steps":
            self.edit_steps()
            return False
        elif response == "Description":
            self.description = input("Description: ")
            return False
        elif response == "Tags":
            self.edit_tags()
            return False
        return True

    def save(self):
        data = {"name":self.name, "description":self.description, "tags":self.tags, "ingredients": self.ingredients, "steps":self.steps}
        filename = "_".join(self.name.split()) + ".json"
        with open(os.path.expanduser(self.recipe_dir + filename), 'w') as f:
            json.dump(data, f)

    def display_tags(self):
        pass

    def print(self):
        print(c.bold + "Recipe Name: " + c.end + self.name)
        print(self.description + "\n") if self.description else print()
        self.print_ingredients()
        self.print_steps()

    def print_ingredients(self):
        print(c.bold + "Ingredient List: " + c.end)
        for ingredient, quantity in self.ingredients.items():
            print("\t" + quantity + " " + ingredient)
        print()

    def print_steps(self):
        print(c.bold + "Steps: " + c.end)
        for number, step in enumerate(self.steps):
            print("\t" + str(number + 1) + ") " + step)
        print()


def _get_list_response(data_type='list', primary_name="Step", secondary_name="Quantity"):
    """ Prompt the user for a series of response that are appended to a list

    Parameters
    ----------
    data_type: str {'list', 'dict'}
        Whether the list of responses should be stored in a list or a dictionary
    primary_name: str
        What question should the use be asked about the key or item in a list
    secondary_name: str
        What question should the user be asked about the value in a key-value pair (dictionary only)

    Returns
    -------
    list or dict
        Set of user responses
    """
    if data_type not in ['list', 'dict']:
        raise Exception("data_type must be 'list' or 'dict'!")
    responses = [] if data_type == 'list' else {}
    counter = 1
    print("Add " + primary_name.lower() + "s below, or leave blank to end")
    while True:
        primary = input(primary_name + " " + str(counter) + ": ")
        counter += 1
        if not primary:
            break
        if isinstance(responses, dict):
            secondary = input(secondary_name + ": ")
            responses[primary] = secondary
        else:
            responses.append(primary)
    return responses


def _yes_no_select(question):
    """ Ask the user a yes/no question and return T/F

    Parameters
    ----------
    question: str
        question to ask the user

    Returns
    -------
    bool
        boolean corresponding to user's response
    """
    while True:
        response = input(question + " [y/n] ")
        if response in ["y", "yes"]:
            return True
        elif response in ["n", "no"]:
            return False
        else:
            print("\nPlease select y or n\n")


def _num_select(question, options):
    """ Prompts users to select from a list

    Parameters
    ----------
    question : str
        question to ask the user
    options : list of str
        list of possible responses

    Returns
    -------
    tuple
        (response number, option selected)
    """
    while True:
        print(question)
        i = 0
        for option in options:
            print("\t" + str(i) + ") " + option)
            i += 1
        response = input()
        if not _is_int(response):
            print("\nPlease input an integer.\n")
        else:
            response = int(response)
            if response < 0 or response > i-1:
                print("\nThat is not a valid response, please try again.\n")
            elif _yes_no_select("You selected '" + options[response] + "', is that correct?"):
                return (response, options[response])


def _is_int(test_val):
    """ Check if an input string is an integer

    Parameters
    ----------
    test_val : str
        string to be tested

    Returns
    -------
    boolean
        True for int, False for non-int
    """
    try:
        int(test_val)
        return True
    except ValueError:
        return False
