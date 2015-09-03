# -*- coding: utf-8 -*-
import db_helper as db
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
            print("Created.")
        elif user_input == '2':
            delete_contact()
            print("Deleted.")
        elif user_input == '3':
            search_by_name()
        elif user_input == '4':
            search_by_phone()
        elif user_input == '5':
            try:
                db.import_to_json()
            except:
                print("Check contact name.")
        elif user_input == '9':
            print("Goodbye")
            checker = False
        elif user_input == "h":
            print("1 - add contact to book")
            print("2 - delete contact from book")
            print("3 - search contact in phone book by name")
            print("4 - search contact in phone book by phone number")
            print("5 - export contact to json file")
            print("9 - close phone book")
        else:
            print("Please, make a correct choice.")


def create_contact():
    print("If contact does not have some attribute, type '-'.")
    lastname = input("Last Name: ")
    firstname = input("First Name: ")
    phone1 = input("Phone 1: ")
    phone2 = input("Phone 2: ")
    phone3 = input("Phone 3: ")
    contact = Contact(firstname=firstname, lastname=lastname, phone1=phone1, phone2=phone2, phone3=phone3)
    db.write_to_bd(contact)


def get_name():
    lastname = '%' + input("Last Name: ") + '%'
    firstname = '%' + input("First Name: ") + '%'
    return firstname, lastname


def search_by_name():
    firstname, lastname = get_name()
    contact = [firstname, lastname]
    db.select_from_db_by_name(contact)


def search_by_phone():
    phone = ['%' + input("Phone: ") + '%']
    db.select_from_db_by_phone(phone)


def delete_contact():
    firstname, lastname = get_name()
    contact = [firstname, lastname]
    db.delete_contact_from_db(contact)


menu()
