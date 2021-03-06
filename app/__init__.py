from flask import Flask, render_template, redirect, url_for, request, session
import os

from api import *
from db_builder import createTables, validate, check_existence, register, insert, updateTheme # # printTable
from db_builder import clearTable, authenticate, getInfo, editInfo, updateWidget, createTables
app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32) #create random key

def user_info():
    username = session['username']
    # ~
    page_theme = getInfo(session['username'], "theme")
    # print(f"PAGE THEME:, {page_theme}")
    theme = updateTheme(page_theme, "light")
    # print(theme)
    home_widgets = updateWidget(session['username'])
    return username, theme, home_widgets

def logged_in():
    return "username" in session

### NEEDS TO BE REPLACED BY FUNCTION IN DB_BUILDER ###
theme = updateTheme("info","light")
#theme of page: pageTheme = getInfo(session['username'], "theme")
#theme = updateTheme(pageTheme, "light")
symbols = ['DOW', 'NDAQ']
info = stocks_api(symbols)
widgets = ['weather', 'news', 'recommendations', 'fun', 'sports', 'space']
packages = {}
for widget in widgets:
    packages[widget] = get_api(widget)
@app.route('/')
@app.route("/home")
def home():
    # available widgets:
    # weather, news, recommendations, stocks, fun, sports, space
    # theme based on bootstrap colors [primary, light, success, danger, warning, info, light, dark]
    # theme = "dark" # should be replaced by function getting user theme from database
    if logged_in():
        # print("LOGGED IN HOME")
        username, theme, home_widgets = user_info()
        # print(f'HOME PAGE THEME: {theme}')
        #~
        # widgets = db_builder.enabledWidgets() # get only the selected widgets from the user's preferences
         #just for testing
        return render_template('home.html', name="Home", theme=theme, packages=packages, username = username, logged_in = logged_in(), widgets=home_widgets)
    else:
        # print("NOT LOGGED IN HOME")
        theme = updateTheme("info", "light")
        # widgets_gatekeeping = ['weather', 'news', 'recommendations']
        return render_template('home.html', name="Home", widgets=widgets, theme=theme, packages=packages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', theme=theme)

@app.route('/user')
def settings():
    return render_template('user.html', name="Log In", theme=theme)

@app.route('/weather')
def weather():
    # ONLY WORKS FOR EST TIME ZONE???
    cities = ['New+York+City', 'Toronto', 'Ontario', 'Sao+Paulo', 'California', 'Mexico+City', 'Miami', 'Cambridge']
    try:
        city = request.args['city']
    except:
        city = "New+York+City"
    info = weather_api(city)
    if logged_in():
        username, theme, home_widgets = user_info()
        return render_template('weather.html', name="Weather", theme=theme, info=info, cities=cities, username = username, logged_in = logged_in())
    else:
        theme = updateTheme("info","light")
        return render_template('weather.html', name="Weather", theme=theme, info=info, cities=cities)

@app.route('/news')
def news():
    info = news_api()
    if logged_in():
        username, theme, home_widgets = user_info()
        return render_template('news.html', name="News", theme=theme, info=info, username = username, logged_in = logged_in())
    else:
        theme = updateTheme("info","light")
        return render_template('news.html', name="News", theme=theme, info=info)

@app.route('/recommendations')
def recommendations():
    info = recommendations_api(3)
    if logged_in():
        username, theme, home_widgets = user_info()
        return render_template('recommendations.html', name="Recommendations", theme=theme, info=info, username = username, logged_in = logged_in())
    else:
        theme = updateTheme("info","light")
        return render_template('recommendations.html', name="Recommendations", theme=theme, info=info)

@app.route('/fun')
def fun():
    info = fun_api(3)
    if logged_in():
        username, theme, home_widgets = user_info()
        return render_template('fun.html', name="Fun", theme=theme, info=info, username = username, logged_in = logged_in())
    else:
        theme = updateTheme("info","light")
        return render_template('fun.html', name="Fun", theme=theme, info=info)

@app.route('/sports')
def sports():
    info = {'sports': sports_api(2021)}
    if logged_in():
        username, theme, home_widgets = user_info()
        return render_template('sports.html', name="Sports", theme=theme, packages=info, username = username, logged_in = logged_in())
    else:
        theme = updateTheme("info","light")
        return render_template('sports.html', name="Sports", theme=theme, packages=info)

@app.route('/space')
def space():
    info = space_api(3)
    if logged_in():
        username, theme, home_widgets = user_info()
        return render_template('space.html', name="Space", theme=theme, info=info, username = username, logged_in = logged_in())
    else:
        theme = updateTheme("info","light")
        return render_template('space.html', name="Space", theme=theme, info=info)

@app.route('/reg1', methods= ["GET", "POST"])
def reg1():
    return render_template("register.html", name = "Reg1", theme = theme)
@app.route('/reg2', methods= ["GET", "POST"])
def reg2():#registers a user
    # print("DELETED TABLE!~")
    # clearTable()
    request_user = request.args['regUser']
    request_password = request.args['regPass']
    # print(f"Hello*********, {request_user}")
    # print (f"Hello*********, {request_password}")
    createTables()
    # print("# printINTG TABLE")
    # printTable()
    session["username"] = request_user #puts user into session
    # print(f"session length: {len(session)}")

    return register(request_user,request_password) #puts username and pw into database, returns response.html
@app.route("/auth", methods=['GET', 'POST'])
def log():#using the loggin button will enter the user into the sesion

    request_user = request.args['regUser']
    # print(f"Hello*********, {request_user}")
    request_password = request.args['regPass']
    # print(f"Hello*********, {request_password}")
    # # printTable()

    session['username'] = request_user
    # print(f"***USERNAME IN SESSION*, {session['username']}")
    huh = getInfo(session['username'], "theme")
    #gets theme
    # print(f"***THEME IN SESSION*, {huh}")
    # editInfo(session['username'], "theme", "RED")
    # editInfo(session['username'], "sports", "0")
    #updates theme and sports

    updateTheme = getInfo(session['username'], "theme") #gets theme
    # print(f"***THEME IN SESSION*, {updateTheme}")## prints theme

    list = updateWidget(session['username'])
    # print(f"***WDIGETS*, {list}, for {session['username']}")
    # printTable()

    return authenticate(request_user,request_password)
    # return render_template('response.html',user = request_user, name = "Logged in", theme = theme)
@app.route("/logout", methods = ["GET","POST"])
def logout():
    # print("HITTING LOG OUT")
    session.pop("username")
    return render_template('home.html', name="Home", widgets=widgets, theme=theme, packages=packages)

@app.route('/preference')
def preference():
    userThemes = ['danger', 'warning', 'success', 'info', 'primary']
    if logged_in():
        username, theme, home_widgets = user_info()
        if theme['main'] not in ['danger', 'warning', 'success', 'info', 'primary']:
            theme['main'] = 'info'
        return render_template('preference.html', home_widgets=home_widgets, userThemes=userThemes, widgets=widgets, name='Settings', theme=theme, username=username, logged_in = logged_in())
    else:
        home()

@app.route('/preferenceSet')
def preferenceSet():
    #updates theme
    #themes = updateTheme(request.args[color])
    # editInfo(session['username'], "theme", request.args)

    #clear list

    home_widgets = updateWidget(session['username'])
    # print(request.args['color'])
    if request.args['color'] != "Select a Theme":
        themes = updateTheme(request.args['color'], 'light')
        color = request.args['color']
        # print(f"COLOR:, {color}" )
        editInfo(session['username'], "theme", color)

    # printTable()

    # clear list
    widgets = []
    space = news = sports = fun = recommendations = weather = True
    # print("WIDGETS")
    # print(request.args.keys())
    for widget in request.args.keys():
        if widget == 'space':
            editInfo(session['username'], "space", '1')
        if widget == 'news':
            editInfo(session['username'], "news", "1")
        if widget == 'sports':
            editInfo(session['username'], "sports", '1')
        if widget == 'fun':
            editInfo(session['username'], "fun", '1')
        if widget == 'recommendations':
            editInfo(session['username'], "recommendations", '1')
        if widget == 'weather':
            editInfo(session['username'], "weather", '1')
    if 'space' not in request.args.keys():
        editInfo(session['username'], 'space', '0')
    if 'news' not in request.args.keys():
        editInfo(session['username'], 'news', '0')
    if 'sports' not in request.args.keys():
        editInfo(session['username'], 'sports', '0')
    if 'fun' not in request.args.keys():
        editInfo(session['username'], 'fun', '0')
    if 'recommendations' not in request.args.keys():
        editInfo(session['username'], 'recommendations', '0')
    if 'weather' not in request.args.keys():
        editInfo(session['username'], 'weather', '0')

    # # add to list
    # # set equals to one in the library
    # else
    # set equals to zero in the library
    #
    # if integer of a widget = 0 or none

    # theme = getInfo(session['username'], "theme")
    # sports = getInfo(session['username'], "sports")
    #
    # editInfo(session['username'], "theme", request.args[])
    # if integer of a wdiget = 1 or none, show
    # new_widgets = list.insert(1, request.args)

    return preference()
def update():
    return True
if __name__ == "__main__":
    app.debug = True
    app.run()
