# -*- coding: utf-8 -*-
import json
import os
import os.path
import glob
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
            print("Added.")
        elif user_input == '2':
            delete_contact()
            print("Deleted.")
        elif user_input == '3':
            search_by_name()
        elif user_input == '4':
            search_by_phone()
        elif user_input == '9':
            print("Goodbye")
            checker = False
        elif user_input == "h":
            print("1 - add contact to book")
            print("2 - delete contact from book")
            print("3 - search contact in phone book by name")
            print("4 - search contact in phone book by phone number")
            print("9 - close phone book")
        else:
            print("Please, make a correct choice.")


def create_contact():
    # TODO: add contact with non latin symbols
    print("If contact does not have some attribute, type '-'.")
    firstname, lastname = get_name()
    phone1 = input("Phone 1: ")
    phone2 = input("Phone 2: ")
    phone3 = input("Phone 3: ")
    contact = Contact(firstname=firstname, lastname=lastname, phone1=phone1, phone2=phone2, phone3=phone3)
    l = [contact.firstname, contact.lastname]
    file_name = "_".join(l)
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "json_imported_files/%s.json" % file_name)
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(contact, default=lambda x: x.__dict__, indent=2, sort_keys=True))


def delete_contact():
    file_name = get_file_name()
    file = get_file(file_name)
    os.remove(file)


def search_by_name():
    file_name = get_file_name()
    file = get_file(file_name)
    f = open(file, "r")
    data = json.load(f)
    if not data:
        print("Contact with that name is not found in address book.")
    else:
        print("-----------------")
        print("first name: " + str(data["firstname"]))
        print("last name: " + str(data["lastname"]))
        print("phone number 1: " + str(data["phone1"]))
        print("phone number 2: " + str(data["phone2"]))
        print("phone number 3: " + str(data["phone3"]))


def search_by_phone():
    files = glob.glob("json_imported_files/*.*")
    phone = input("Phone: ")
    for i in files:
        with open(i, "r") as f:
            for line in f:
                if phone in line:
                    file = open(i, "r")
                    data = json.load(file)
                    print("-----------------")
                    print("first name: " + str(data["firstname"]))
                    print("last name: " + str(data["lastname"]))
                    print("phone number 1: " + str(data["phone1"]))
                    print("phone number 2: " + str(data["phone2"]))
                    print("phone number 3: " + str(data["phone3"]))


def get_file(file_name):
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "json_imported_files/%s.json" % file_name)
    return file


def get_file_name():
    firstname, lastname = get_name()
    contact = Contact(firstname=firstname, lastname=lastname)
    l = [contact.firstname, contact.lastname]
    file_name = "_".join(l)
    return file_name


def get_name():
    lastname = input("Last Name: ")
    firstname = input("First Name: ")
    return firstname, lastname


menu()
