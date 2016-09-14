#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import sys
import json
import memory_general as general
import memory_mail

reload(sys)
sys.setdefaultencoding('utf-8')

# query memory list
def command_memory_list(table_name):
    cmd_resSet = general.select_cmd(table_name, True)
    #print 'cmd_resSet: ', type(cmd_resSet[8])
    for i in cmd_resSet:
        print i[0],i[1]

# show memory
def command_memory_show(table_name, table_id):
    elements = general.get_table_elements(table_name)
    cmd_resSet = general.select_cmd(table_name, True, id=table_id)
    print general.mail_format(cmd_resSet)
    general.write_memory_tmp(table_name, elements, cmd_resSet)

# new/create data
def command_memory_new(table_name):
    elements = general.get_table_elements(table_name)
    general.write_memory_tmp(table_name, elements)

# insert data after new/update
def command_memory_insert(table_name):
    # read memory_tmp
    vals = general.read_memory_tmp(table_name)
    # insert mysql command
    general.insert_memory_table(table_name, vals)

# update data after new/update
def command_memory_update(table_name):
    # read memory_tmp
    vals = general.read_memory_tmp(table_name)
    # execute mysql command
    general.update_memory_table(table_name, vals)

# delete data from table
def command_memory_delete(table_name, table_id):
    cmd = 'delete from %s where id=%s;' % (table_name, table_id)
    # print cmd
    general.mariadb_cmd(cmd)

# send email
def command_memory_send(table_name):
    if table_name == 'table_task':
        command_memory_send_task(table_name)
    elif table_name == 'table_summary':
        command_memory_send_summary(table_name)
    else:
        return False

# send email of task
def command_memory_send_task(table_name):
    # get progress and judge endtime, and update endtime
    cmd = 'select id from %s where progress < 100 and endTime < CURDATE();' \
        % table_name
    resSet = general.mariadb_cmd_ret(cmd)
    for res in resSet:
        cmd = 'update %s set endTime=CURDATE() where id=%s;' % \
            (table_name, res[0])
        general.mariadb_cmd(cmd)
    # compare endtime
    cmd = 'select * from %s where progress < 100;' % table_name
    resSet = general.mariadb_cmd_ret(cmd)
    # send email
    memory_mail.send_email(table_name, resSet)
    # memory_mail.send_email(table_name, str(resSet))

# send email of summary
def command_memory_send_summary(table_name):
    # get data before 30
    cmd = 'select * from %s where to_days(now()) - to_days(datetime) <= 15;' \
        % table_name
    resSet = general.mariadb_cmd_ret(cmd)
    # send email
    memory_mail.send_email(table_name, resSet)
