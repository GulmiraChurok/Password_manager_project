
def number_in_range(value, ge, gt, le, lt):
    if ge is not None and value < ge:
        return False
    if gt is not None and value <= gt:
        return False
    if le is not None and value > le:
        return False
    if lt is not None and value >= lt:
        return False
    return True


def input_int(prompt="Please enter a whole number: ",
              error="Input must be a whole number",
              ge=None, gt=None, le=None, lt=None):
    while True:
        try:
            value_string = input(prompt)
            value_int = int(value_string)
            if number_in_range(value_int, ge, gt, le, lt):
                return value_int
            print(error)
        except ValueError:
            print(error)


def input_float(prompt="Please enter a decimal number: ",
                error="Input must be a decimal number",
                ge=None, gt=None, le=None, lt=None):
    while True:
        try:
            value_string = input(prompt)
            value_float = float(value_string)
            if number_in_range(value_float, ge, gt, le, lt):
                return value_float
            else:
                print(error)
        except ValueError:
            print(error)


def y_or_no(prompt="Please enter Yes or No: ", error="Input must be Yes or No!!!"):
    while True:
        value = input(prompt).lower()
        if value in ["yes", "y"]:
            return True
        if value in ["no", "n"]:
            return False
        print(error)


def input_string(prompt="Please enter any text: ", error="Input must be non-empty!", valid=lambda s: len(s) > 0):
    while True:
        value = input(prompt)
        if valid(value):
            return value
        print(error)


def select_item(prompt="Please type yes or no: ", error="Answer must be Yes or No!", choices=["Yes", "No"], map=None):
    value_dict = {}                                 #value_dict is empty, why to lowercase, when it is empty.
    for choice in choices:
        value_dict[choice.lower()] = choice         #lowercases key of choice, the value is just choice?
    if map is not None:
        for key in map:
            value_dict[key.lower()] = map[key]
    while True:
        val = input(prompt).lower()
        if val in value_dict:
            return value_dict[val]
        print(error)


def input_value(type="int", *args, **kwargs):
    if type == "int":
        return input_int(*args, **kwargs)
    elif type == "float":
        return input_float(*args, **kwargs)
    elif type == "y_or_n":
        return y_or_no(*args, **kwargs)
    elif type == "string":
        return input_string(*args, **kwargs)
    elif type == "select":
        return select_item(*args, **kwargs)
    else:
        print("Error! Unknown type", type)
