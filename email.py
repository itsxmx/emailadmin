#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This is a simple python program to help manage email address
that are set up using mysql. This program allows you to
add/delete email addresses, add new domains, and add
new aliases.
'''

import MySQLdb as mdb
import os

def db():
        data = open('/path/to/mysqlinfo', 'r')  # this grabs mysql info
        login = data.read().split(',')		# from a text document
        return mdb.connect(login[0], login[1], login[2], login[3])

def listDomains():
        con = db() 
        with con:
                cur = con.cursor()
                cur.execute("SELECT id, name FROM virtual_domains")
                domains = cur.fetchall()

                print 'id   :  domain'
                for d in domains:
                        print d[0], ' : ', d[1]
                cur.close()
                
def createEmail():
        
        os.system('clear')      # clear terminal
        listDomains()
        id = raw_input('Select id of domain: ')
        email = raw_input('User Email (include the proper domain): ')
        pw = raw_input('User Pw: ')

        if id and email and pw:
                con = db()
                
                with con:
                        cur = con.cursor()

                        #make sure email address doesnt exists
                        cur.execute("SELECT * FROM virtual_users WHERE email = '%s';" % (email))
                        found = cur.fetchall()

                        if found: # if email address exists
                                print 'Email already exists'
                        else:   # if not, then add it
                                cur.execute("INSERT INTO `virtual_users`(`domain_id`, `password` , `email`)" \
                                            " VALUES('%s', ENCRYPT('%s', CONCAT('$6$', SUBSTRING(SHA(RAND()), -16))) , '%s');" % (id, pw, email))

                                cur.execute("SELECT * FROM virtual_users WHERE email='%s';" % (email))
                                rows = cur.fetchall()

                                if rows: #display web client info
                                        print 'Email added!'
                                else:
                                        print 'Error adding email.'
                con.close()

def delEmail():
        os.system('clear')
        email = raw_input('User Email to delete: ')

        if email:
                con = db()
                
                with con:
                        cur = con.cursor()
                        # dels email address - WARNING: anyone has the power to del account. Don't abuse.
                        cur.execute("DELETE FROM virtual_users WHERE email='%s';" % (email))
                        
                        cur.execute("SELECT * FROM virtual_users WHERE email='%s';" % (email))
                        rows = cur.fetchall()

                        if not rows:
                                print 'Email deleted!'
                        else:
                                print 'Error deleting email'
                con.close()

def newDomains():
        os.system('clear')
        domain = raw_input('Enter new domain: ')
        
        if domain:        
                con = db()
                
                with con:
                        cur = con.cursor()
                        cur.execute("INSERT INTO virtual_domains(`name`) VALUES('%s');" % (domain))

                        cur.execute("SELECT * FROM virtual_domains WHERE name='%s';" %(domain)) # verify its been added
                        rows = cur.fetchall()

                        if rows:
                                print 'Domain added!'
                        else:
                                print 'Error adding domain!'

def aliases():
        os.system('clear')
        listDomains()
        id = raw_input('Select the id of domain: ')
        alias = raw_input('Alias address: ')
        orig = raw_input('Current email: ')

        con = db()
        with con:
                cur = con.cursor()

                cur.execute("SELECT * FROM virtual_users WHERE email='%s';" % (orig))
                rows = cur.fetchall()

                if rows:
                        cur.execute("INSERT INTO virtual_aliases(`domain_id`, `source`, `destination`)" \
                                    " VALUES('%s', '%s', '%s');" % (id, alias, orig))
                        
                        cur.execute("SELECT * FROM virtual_aliases WHERE source='%s';" %(alias))
                        row = cur.fetchall()

                        if row:
                                print 'Aliases added!'
                        else:
                                print 'Error adding alias'
                else:
                        print 'That email address does not exists'

def menu():
        print '\nEmail Admin Tool'
        print 'Choose 1 to create an email'
        print 'Choose 2 to delete an email'
        print 'Choose 3 to add a new domain'
        print 'Choose 4 to add an alias'
        print 'Or type q to exit\n'
        
def main():
        menu()
        while True:
                print 'Press "m" to see the menu again'
                choice = raw_input('Choice: ')
                
                if choice == 'q':
                        break
                if choice == 'm':
                        menu()
                elif choice == '1':
                        createEmail()
                elif choice == '2':
                        delEmail()
                elif choice == '3':
                        newDomains()
                elif choice == '4':
                        aliases()
                else:
                        print 'Invalid option. Please choose again.'
                        
                        
if __name__ == "__main__": main()
