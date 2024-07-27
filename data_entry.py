from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}

def get_date(prompt, allow_default = False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)
    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid Format. Enter in DD-MM-YYYY format")
        return get_date(prompt, allow_default)


def get_amount():
    try:
        amount = float(input("Enter your amount: "))
        if amount <= 0:
            raise ValueError("Anount shoul be more than zero")
        return amount
    except ValueError as e:
        print(e)
        return get_category()
    


def get_category():
    category = input("Enter a category ('I' for income or 'E' for Expenses): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]

    print("Invalid input. Please enter 'I' for income or 'E' for Expenses")
    return get_category()


def get_description():
    return input("Enter a description (optional): ")