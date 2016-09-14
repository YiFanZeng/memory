#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import chardet
import ConfigParser
import mysql.connector as mariadb

reload(sys)
sys.setdefaultencoding('utf-8')
# print(sys.getdefaultencoding())

# execute sql command and return values
def mariadb_cmd_ret(cmd):
    mariadb_connection = mariadb.connect(user='memory', password='????????',
                                         database='memory')
    cursor = mariadb_connection.cursor()
    cursor.execute(cmd)
    retSet = cursor.fetchall()
    # print retSet
    mariadb_connection.close()
    return retSet

# execute sql command
def mariadb_cmd(cmd):
    mariadb_connection = mariadb.connect(user='memory', password='????????',
                                         database='memory')
    cursor = mariadb_connection.cursor()
    cursor.execute(cmd)
    mariadb_connection.close()

# query database
def select_cmd(table_name, *args, **kw):
    if kw:
        cmd = 'select * from %s where id=%s;' % (table_name, kw['id'])
    elif args:
        cmd = 'select id, subject from %s;' % table_name
    else:
        cmd = 'select * from %s;' % table_name
    # print cmd
    return mariadb_cmd_ret(cmd)

# insert database's table
def insert_memory_table(table_name, vals):
    # print vals
    keys = ', '.join(vals.keys())
    values = "', '".join(vals.values())
    values = "'" + values + "'"
    cmd = 'insert into %s (%s) values (%s);' % (table_name, keys, values)
    mariadb_cmd(cmd)

# update databae's table
def update_memory_table(table_name, vals):
    # print vals
    for val in vals:
        cmd = "update %s set %s='%s' where id=%s;" % \
              (table_name, val, vals[val], vals['id'])
        # print cmd
        mariadb_cmd(cmd)

# get table elements
def get_table_elements(table_name):
    cmd = 'desc %s' % table_name
    cmd_resSet = mariadb_cmd_ret(cmd)
    elements = []
    for ele in cmd_resSet:
        elements.append(ele[0])
    # print 'elements: ', elements
    return elements

# add section
def add_section(section):
    config_file = 'memory_tmp'
    _config = ConfigParser.SafeConfigParser()
    _config.add_section(section)
    _config.write(open(config_file, 'w'))

# set key and value
def set_key_value(section, key, value):
    config_file = 'memory_tmp'
    _config = ConfigParser.SafeConfigParser()
    _config.read(config_file)
    _config.set(section, key, value)
    _config.write(open(config_file, 'w'))

# read info from memory_tmp
def read_memory_tmp(section):
    values = {}
    config_file = 'memory_tmp'
    _config = ConfigParser.SafeConfigParser()
    _config.read(config_file)
    keys = _config.options(section)
    for key in keys:
        values[key] = _config.get(section, key)
    return values

# write result of sql command to memory_tmp
def write_memory_tmp(table_name, *args):
    if len(args) == 1:
        # write key but not value is null
        add_section(table_name)
        for key in args[0]:
            set_key_value(table_name, key, '')
    elif len(args) == 2:
        # write key and value
        add_section(table_name)
        for i in range(len(args[0])):
            set_key_value(table_name, args[0][i], str(args[1][0][i]))
    else:
        sys.exit("There are something wrong in write_memory_tmp")

# mail_format
def mail_format(mail_text):
    msg = ''
    for task in mail_text:
        msg += '#' * 26
        msg += '\n'
        for par in task:
            if isinstance(par, unicode):
                msg += '&& '
                msg += par.encode('utf8')
                msg += '\n'
            else:
                msg += '&& '
                msg += str(par)
                msg += '\n'
    # print msg
    return msg
