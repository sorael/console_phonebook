# -*- coding: utf-8 -*-
import sqlite3


def create_connection():
    conn = sqlite3.connect('phone_book.db')
    cur = conn.cursor()
    return conn, cur


def write_to_bd(contact):
    conn, cur = create_connection()
    create_tables(cur)
    add_data_to_db(cur, contact)
    close_connection(conn)


def select_from_db_by_lastname(lastname):
    conn, cur = create_connection()
    t = [lastname]
    name = cur.execute(
        "SELECT lastname, firstname FROM users WHERE lastname LIKE ?", t)
    name_list = []
    for i in name:
        name_list += i
    phones = cur.execute(
        "SELECT phone FROM phones WHERE u_id = (SELECT id FROM users WHERE lastname LIKE ?)", t)
    phone_list = []
    for i in phones:
        phone_list += i
    print(" ".join(name_list) + ": " + ", ".join(phone_list))
    close_connection(conn)


def select_from_db_by_phone(phone):
    # TODO: search by phone number works not correctly
    conn, cur = create_connection()
    t = [phone]
    name = cur.execute(
        "SELECT lastname, firstname FROM users WHERE id IN (SELECT u_id FROM phones WHERE phone LIKE ?)", t)
    name_list = []
    for i in name:
        name_list += i
    phones = cur.execute(
        "SELECT phone FROM phones WHERE u_id = (SELECT id FROM users WHERE lastname LIKE ?)", t)
    phone_list = []
    for i in phones:
        phone_list += i
    print(" ".join(name_list) + ": " + ", ".join(phone_list))
    close_connection(conn)


def create_tables(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS users (id integer primary key autoincrement not null unique,
                                                    lastname text,
                                                    firstname text)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS phones (id integer primary key autoincrement not null unique,
                                                    phone text,
                                                    u_id integer not null)''')


def add_data_to_db(cur, contact):
    arguments = [contact.lastname, contact.firstname]
    cur.execute("INSERT INTO users (lastname,firstname) VALUES (?,?)", arguments)
    user_id = cur.execute("SELECT id FROM users WHERE lastname=? AND firstname=?", arguments)
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


def delete_contact_from_db(lastname):
    conn, cur = create_connection()
    t = [lastname]
    cur.execute("DELETE FROM phones WHERE u_id = (SELECT id FROM users WHERE lastname=?)", t)
    cur.execute("DELETE FROM users WHERE lastname=?", t)
    close_connection(conn)


def close_connection(conn):
    conn.commit()
    conn.close()
