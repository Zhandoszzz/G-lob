import pymongo
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from datetime import datetime
from bson.objectid import ObjectId
# Create your views here.
from pymongo import MongoClient
client = MongoClient("mongodb+srv://admin:admin@cluster0.1dtth.mongodb.net/?retryWrites=true&w=majority")

def category(request, name):
    db = client['blog']
    cats = db.category.distinct('name')
    posts = db.post.aggregate([{"$match": {'category': name}}, {"$sort": {'date': -1}}])
    return render(request, 'GLOB/glob.html', {'posts': posts, 'cats': cats})


def search(request):
    text = (request.GET['text'])
    db = client['blog']['post']
    posts = list(db.find({"$or":[{'title': {"$regex": text}},{'content': {"$regex": text}}]}))
    return render(request, 'GLOB/glob.html', {'posts': posts})

def dashboard(request):
    db = client['blog']
    posts = list(db.post.find({'username': request.session['username'][0]}))
    for post in posts:
        post['id'] = post.get('_id')
    return render(request, 'GLOB/dashboard.html', {'posts': posts})

def register(request):

    db = client['blog']['user']
    info = request.POST
    user = {
        'firstname' : info.get('fname',''),
        'lastname' : info.get('lname', ''),
        'e-mail' : info.get('email', ''),
        'username' : info.get('username', ''),
        'password' : info.get('pwd', None),
    }
    cpwd = info.get('cpwd','')
    exist = db.find({'username': user['username']})
    if cpwd == user['password'] and not exist:
        db.insert_one(user)
        request.session['username'] = user['username'],
        return redirect('index')
    return render(request, 'GLOB/register.html')


def login(request):
    db = client['blog']['user']
    info = request.GET
    user = {
        'username': info.get('username', ''),
        'password': info.get('password', None),
    }
    user = db.find_one({'username': user['username'], 'password': user['password']})
    if user:
        request.session['username'] = user['username'],
        return redirect('index')
    return render(request, 'GLOB/signing.html')

def logout(request):
    del request.session['username']
    return redirect('index')

def add_post(request):
    db = client['blog']
    cats = db.category.distinct('name')
    posts = list(db.post.find())
    return render(request, 'GLOB/add-post.html', {'cats': cats})


class HomePage(View):

    def get(self, request, *args, **kwargs):
        db = client['blog']
        posts = list(db.post.find().sort('date', -1))
        for post in posts:
            post['id'] = post.get('_id')
        cats = db.category.distinct('name')
        return render(request, 'GLOB/glob.html', {'posts': posts, 'cats': cats})

    def post(self, request, *args, **kwargs):
        db = client['blog']
        info = dict(request.POST)
        post = {
            'title': info.get('title','?')[0],
            "content": info.get('content','?')[0],
            'category': info.get('category','?')[0],
            'username': request.session['username'][0],
            'date': datetime.now(),
        }
        db.post.insert_one(post)
        cats = db.category.distinct('name')
        posts = list(db.post.find().sort('date', -1))
        return render(request, 'GLOB/glob.html', {'posts': posts, 'cats': cats})


def delete_post(request, id):
    db = client['blog']['post']
    db.delete_one({'_id': ObjectId(id)})
    return redirect('dashboard')

def edit_post(request, id):
    db = client['blog']
    if request.method == 'GET':
        cats = db.category.distinct('name')

        return render(request, 'GLOB/edit-post.html', {'cats': cats,'id':id})
    if request.method == 'POST':
        db = client['blog']['post']
        info = request.POST
        post = {
            "$set":{
                'title': info.get('title', '?')[0],
                "content": info.get('content', '?')[0],
                'category': info.get('category', '?'),
            }
        }
        db.update_one({'_id': ObjectId(id)}, post)
    return redirect('dashboard')

def get_post(request, id):
    db = client['blog']
    post = db.post.find_one({'_id': ObjectId(id)})
    post['id'] = id
    comments = db.comment.find({'post_id': ObjectId(id)})
    return render(request, "GLOB/ext.html", {'post': post, 'comments': comments})


def comment(request, id):
    db = client['blog']
    info = request.POST
    comment = {
        "post_id" : ObjectId(id),
        "comment" : info.get('comment',''),
        'date' : datetime.now().strftime('%Y-%m-%d %H:%M'),
        'username': request.session['username'][0],
    }
    db.comment.insert_one(comment)
    return redirect('post', id=id)

def add_category(request):
    db = client['blog']['category']
    if request.method == 'POST':
        cat = {
            'name': request.POST['name']
        }
        db.insert_one(cat)
        return redirect('dashboard')
    return render(request, 'GLOB/add-category.html')