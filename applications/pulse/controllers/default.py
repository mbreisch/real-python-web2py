# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import requests
import json

def index():
    return dict()

def process(my_list):
    binary_first=my_list[1]
    output_first=json.loads(binary_first)
    label_first=output_first["label"]

    binary_second=my_list[3]
    output_second=json.loads(binary_second)
    label_second=output_second["label"]

    if label_first == "pos":
        if label_second != "pos":
            return my_list[0]
        else:
            if output_first["probability"]["pos"] > output_second["probability"]["pos"]:
                return my_list[0]
            else:
                return my_list[2]
    elif label_first == "neg":
        if label_second != "neg":
            return my_list[2]
        else:
            if output_first["probability"]["neg"] < output_second["probability"]["neg"]:
                return my_list[0]
            else:
                return my_list[2]
    elif label_first == "neutral":
        if label_second == "pos":
            return my_list[2]
        elif label_second == "neg":
            return my_list[0]
        else:
            if output_first["probability"]["pos"] > output_second["probability"]["pos"]:
                return my_list[0]
            else:
                return my_list[2]

def pulse():
    session.m=[]
    url='http://text-processing.com/api/sentiment/'

    text_first=request.vars.first_item
    text_first=text_first.split('_')
    text_first=' '.join(text_first)
    session.m.append(text_first)
    data_first={'text':text_first}
    r_first=requests.post(url,data=data_first)
    session.m.append(r_first.content)

    text_second=request.vars.second_item
    text_second=text_second.split('_')
    text_second=' '.join(text_second)
    session.m.append(text_second)
    data_second={'text':text_second}
    r_second=requests.post(url,data=data_second)
    session.m.append(r_second.content)

    winner=process(session.m)
    return "The winner is {}".format(winner)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
