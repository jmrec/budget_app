from math import floor

def get_percentage_spent_by_category(total_withdrawal_by_category, format):
    array = []
    for each in total_withdrawal_by_category:
        array.append(
                floor((each / sum(total_withdrawal_by_category)) * 10)
            )

    try:
        return format(array)
    except:
        return array

def convert_to_single_numbers(percentage_list):
    array = []
    for percentage in percentage_list:
        match percentage:
            case 100:
                array.append(10)
            case 0:
                array.append(0)
            case _:
                array.append(
                    int(str(percentage)[0])
                )
    return array

def render_each_record(key):
    description = key['description'][0:23]

    if key['amount'] >= 10000:
        amount = "9999.99".rjust(29 - len(description))
    else:
        amount = str("%.2f" % (key['amount'])).rjust(29 - len(description))

    return f"{description} {amount}\n"

def is_last_in_list(element, list):
    return element == list[-1]

def is_first_in_list(element, list):
    return element == list[0]

def get_category_names(list_of_categories):
    name_of_categories = []
    for each in list_of_categories:
        name_of_categories.append(each.get_category_name())

    return name_of_categories

def render_object_for_printing(
        name_of_category, ledger, render_function, balance
        ):
    to_be_printed = f"{name_of_category.center(30,'*')}\n"
    for key in ledger:
        to_be_printed += render_function(key)

    return to_be_printed + f"Total: {'%.2f' % balance}"

def vertically_align_category_names(name_of_categories):
    index = 0
    to_be_printed = ""
    longest_string = max(name_of_categories, key=len)

    while index < len(longest_string):
        for name in name_of_categories:
            if is_first_in_list(name, name_of_categories):
                to_be_printed += "     "

            try:
                to_be_printed += name[index]
            except:
                if is_last_in_list(name, name_of_categories):
                    to_be_printed += "\n"
                else:
                    to_be_printed += "   "
                continue

            if index == len(longest_string) - 1:
                to_be_printed += "  "
                break
            elif is_last_in_list(name, name_of_categories):
                to_be_printed += "  \n"
            else:
                to_be_printed += "  "

        index += 1
    return to_be_printed

def fill_chart_with_o(chart, percentage_spent_per_category):
    for row in chart:
        for percentage in percentage_spent_per_category:
            if percentage * 10 >= int(row[0]):
                row.append("o")
            else:
                row.append(" ")

    return chart

def create_line(list_of_categories):
    return f"    ----{'---' * (len(list_of_categories) - 1)}\n"

def render_chart(filled_chart):
    string = ""
    for row in filled_chart:
            string += f"{row[0]}| "
            for circle in row[1::]:
                if circle != "":
                    string += f"{circle}  "

            string += "\n"

    return string

class Category:
    def __init__(self, category_name):
        self.ledger = []
        self.balance = 0
        self.category_name = category_name

    def __str__(self):
        return render_object_for_printing(
            name_of_category= self.category_name,
            ledger= self.ledger,
            render_function= render_each_record,
            balance= self.balance,
        )

    def get_category_name(self):
        return self.category_name

    def get_total_withdrawal_amount(self):
        amount = 0
        for key in self.ledger:
            if key["amount"] < 0:
                amount += key["amount"]

        return amount

    def deposit(self, amount, description=""):
        self.ledger.append({
            "amount": amount,
            "description": description
            })
        self.balance += amount

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({
                "amount": 0 - amount,
                "description": description
                })
            self.balance -= amount
            return True
        else:
            return False

    def get_balance(self):
        return self.balance

    def transfer(self, amount, budget_category):
        if self.check_funds(amount):
            self.ledger.append({
                "amount": 0 - amount,
                "description": f"Transfer to {budget_category.get_category_name()}",
            })
            budget_category.deposit(
                amount,
                description= f"Transfer from {self.category_name}"
            )
            self.balance -= amount
            return True
        else:
            return False

    def check_funds(self, amount):
        return self.balance >= amount

def create_spend_chart(list_of_categories):
    total_withdrawal_by_category = []
    for category in list_of_categories:
        total_withdrawal_by_category.append(
            abs(category.get_total_withdrawal_amount())
            )

    percentage_spent_per_category = get_percentage_spent_by_category(
        total_withdrawal_by_category,
        format= convert_to_single_numbers
    )

    list_of_category_names = get_category_names(list_of_categories)

    chart = [
        ["100"],
        [" 90"],
        [" 80"],
        [" 70"],
        [" 60"],
        [" 50"],
        [" 40"],
        [" 30"],
        [" 20"],
        [" 10"],
        ["  0"],
    ]

    filled_chart = fill_chart_with_o(chart, percentage_spent_per_category)

    to_be_printed = "Percentage spent by category\n"

    to_be_printed += render_chart(filled_chart)

    to_be_printed += create_line(list_of_categories)

    to_be_printed += vertically_align_category_names(
        list_of_category_names,
        )

    return to_be_printed
