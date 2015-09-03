# -*- coding: utf-8 -*-
import sqlite3
import json
import os.path
from contact import Contact


def create_connection():
    conn = sqlite3.connect('phone_book.db')
    cur = conn.cursor()
    return conn, cur


def write_to_bd(contact):
    conn, cur = create_connection()
    create_tables(cur)
    add_data_to_db(cur, contact)
    close_connection(conn)


def select_from_db_by_name(contact):
    conn, cur = create_connection()
    names = cur.execute(
        "SELECT firstname, lastname FROM users WHERE firstname LIKE ? AND lastname LIKE ?", contact)
    name_list = []
    for i in names:
        name_list += i
    phones = cur.execute(
        "SELECT phone FROM phones WHERE u_id = (SELECT id FROM users WHERE firstname LIKE ? AND lastname LIKE ?)", contact)
    phone_list = []
    for i in phones:
        phone_list += i
    if not names:
        print("Contact with that name is not found in address book.")
    else:
        print("-----------------")
        print("first name: " + str(name_list[0]))
        print("last name: " + str(name_list[1]))
        print("phone number 1: " + str(phone_list[0]))
        print("phone number 2: " + str(phone_list[1]))
        print("phone number 3: " + str(phone_list[2]))
    close_connection(conn)


def select_from_db_by_phone(phone):
    conn, cur = create_connection()
    names = cur.execute(
        "SELECT firstname, lastname FROM users WHERE id IN (SELECT u_id FROM phones WHERE phone LIKE ?)", phone)
    name_list = []
    for i in names:
        name_list += i
    phones = cur.execute(
        "SELECT phone FROM phones WHERE u_id = (SELECT id FROM users WHERE firstname LIKE ? AND lastname LIKE ?)", name_list)
    phone_list = []
    for j in phones:
        phone_list += j
    if not names:
        print("Contact with that name is not found in address book.")
    else:
        print("-----------------")
        print("first name: " + str(name_list[0]))
        print("last name: " + str(name_list[1]))
        print("phone number 1: " + str(phone_list[0]))
        print("phone number 2: " + str(phone_list[1]))
        print("phone number 3: " + str(phone_list[2]))
    close_connection(conn)


def create_tables(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS users (id integer primary key autoincrement not null unique,
                                                    firstname text,
                                                    lastname text)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS phones (id integer primary key autoincrement not null unique,
                                                    phone text,
                                                    u_id integer not null)''')


def add_data_to_db(cur, contact):
    arguments = [contact.firstname, contact.lastname]
    cur.execute("INSERT INTO users (firstname,lastname) VALUES (?,?)", arguments)
    user_id = cur.execute("SELECT id FROM users WHERE firstname=? AND lastname=?", arguments)
    u_id = []
    for i in user_id:
        u_id += i
    u_id = ''.join(str(x) for x in u_id)
    phone1 = [contact.phone1, u_id]
    phone2 = [contact.phone2, u_id]
    phone3 = [contact.phone3, u_id]
    if contact.phone1 is not '':
        cur.execute("INSERT INTO phones (phone,u_id) VALUES (?,?)", phone1)
    if contact.phone2 is not '':
        cur.execute("INSERT INTO phones (phone,u_id) VALUES (?,?)", phone2)
    if contact.phone3 is not '':
        cur.execute("INSERT INTO phones (phone,u_id) VALUES (?,?)", phone3)


def delete_contact_from_db(contact):
    conn, cur = create_connection()
    cur.execute("DELETE FROM phones WHERE u_id = (SELECT id FROM users WHERE firstname LIKE ? AND lastname LIKE ?)", contact)
    cur.execute("DELETE FROM users WHERE firstname LIKE ? AND lastname LIKE ?", contact)
    close_connection(conn)


def import_to_json():
    # TODO: add check
    conn, cur = create_connection()
    lastname = input("Last Name: ")
    t = [lastname]
    # lastname and firstname
    name_from_db = cur.execute(
        "SELECT firstname, lastname FROM users WHERE lastname LIKE ?", t)
    name_list = []
    for i in name_from_db:
        name_list += i
    file_name = "_".join(name_list)
    # phones
    phones_from_db = cur.execute(
        "SELECT phone FROM phones WHERE u_id = (SELECT id FROM users WHERE lastname LIKE ?)", t)
    phones_list = []
    for i in phones_from_db:
        phones_list += i

    cont_json = Contact(firstname=name_list[0], lastname=name_list[1],
                        phone1=phones_list[0], phone2=phones_list[1], phone3=phones_list[2])
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "json_imported_files/%s.json" % file_name)
    with open(file, "w") as f:
        f.write(json.dumps(cont_json, default=lambda x: x.__dict__, indent=2, sort_keys=True))

    close_connection(conn)


def close_connection(conn):
    conn.commit()
    conn.close()
