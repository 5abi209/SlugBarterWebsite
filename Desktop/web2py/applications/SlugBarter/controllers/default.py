# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

#controller for when the user is at index page
def index():
  return dict()
    
#controller for when the user registers
def register():
    return dict(form = auth.register())
   
#controller for when the user login
def login(): 
  form = auth.login()
  session.userName = form.vars.name
  return dict(form = form)
    
def mypage():
    username = session.userName
    return dict(username = username)
    
@auth.requires_login()   
def postlisting():
    form = SQLFORM(db.listing)
    if form.process().accepted:
        session.flash = T('Accepted')
    elif form.errors:
        session.flash = T('Form has errors')
    else:
        session.flash = T("Please complete all the information in the form")
        
    return dict(form = form)

@auth.requires_login()
def view_my_listings():
    query = (db.listing.user == auth.user_id)
    lists = db(query).select(db.listing.ALL)
    return dict(lists = lists)

def description_mode():
    reads = db.listing(request.args[0]) or redirect(URL('mypage'))
    return dict(reads = reads, user_id = auth.user_id)

def my_interests():
    return dict()
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


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
