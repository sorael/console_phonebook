# -*- coding: utf-8 -*-
import db
from contact import Contact


def menu():
    checker = True
    while checker is True:
        print("\n----------------------")
        print("Enter 'h' to read a help")
        print("----------------------\n")
        user_input = input("Please make a choice: ")
        if user_input == '1':
            create_contact()
        elif user_input == '2':
            delete_contact()
            print("Deleted.")
        elif user_input == '3':
            search_by_lastname()
        elif user_input == '4':
            search_by_phone()
        elif user_input == '5':
            pass
        elif user_input == '9':
            print("Goodbye")
            checker = False
        elif user_input == "h":
            print("1 - add contact to book")
            print("2 - delete contact from book")
            print("3 - search contact in book by last name")
            print("4 - search contact in book by phone number")
            print("5 - export contact to json file")
            print("9 - close phone book")
        else:
            print("Please, make a correct choice.")


def create_contact():
    lastname = input("Last Name: ")
    firstname = input("First Name: ")
    phone1 = input("Phone 1: ")
    phone2 = input("Phone 2: ")
    phone3 = input("Phone 3: ")
    contact = Contact(lastname=lastname, firstname=firstname, phone1=phone1, phone2=phone2, phone3=phone3)
    db.write_to_bd(contact)


def search_by_lastname():
    lastname = '%' + input("Last Name: ") + '%'
    db.select_from_db_by_lastname(lastname)


def search_by_phone():
    phone = '%' + input("Phone: ") + '%'
    db.select_from_db_by_phone(phone)


def delete_contact():
    lastname = input("Last Name: ")
    db.delete_contact_from_db(lastname)


menu()
