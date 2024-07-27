import pandas as pd
import matplotlib as mlt

import csv
from datetime import datetime

from data_entry import get_amount, get_category, get_date, get_description

class CSV:
    CSV_FILE = "finance.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FROMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns= cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index= False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }

        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames= cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def get_transaction(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format= CSV.FROMAT )
        start_date = datetime.strptime(start_date, CSV.FROMAT)
        end_date = datetime.strptime(end_date, CSV.FROMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)

        filter_df = df.loc[mask]
        if filter_df.empty:
            print("No transactions found in given range.")
        else:
            print(f"Transactions start from {start_date.strftime(CSV.FROMAT)} to {end_date.strftime(CSV.FROMAT)}")
            print(
                filter_df.to_string(
                    index = False,
                    formatters = {"date": lambda x: x.strftime(CSV.FROMAT)}
                    )
                )
            
            total_income = filter_df[filter_df["category"] == "Income"]["amount"].sum()
            total_expense = filter_df[filter_df["category"] == "Expense"]["amount"].sum()
            print("\nSummery: ")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Total Saving: ${(total_income - total_expense):.2f}")

        return filter_df



def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of transaction in dd-mm-yyyy or enter for today's date: ", allow_default= True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


def main():
    while True:
        print("\n1. Add a new transaction.")
        print("2. View transactions and summery within given date range.")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()

        elif choice == "2":
            st_date = get_date("Enter your starting date (dd-mm-yyyy): ")
            en_date = get_date("Enter your ending date (dd-mm-yyyy): ")
            df = CSV.get_transaction(st_date, en_date)

        elif choice == "3":
            print("Exiting...")
            break 

        else:
            print("Invalid choice, choose from 1, 2 or 3.")       


if __name__ == "__main__":
    main()
