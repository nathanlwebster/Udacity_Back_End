
from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from sqlalchemy import create_engine
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new')
def newRestaurant():
    return "This page will be for making a new restaurant"

@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    return "This page will be for editing restaurant %s" % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurantToDelete = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurantToDelete)
        session.commit()
        flash("Menu item deleted!")
        return redirect(url_for('showRestaurants'))
    
    else:
        return render_template('deleteRestaurant.html', restaurant_id = restaurantToDelete.id, restaurant = restaurantToDelete)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    return "This page is the menu for restaurant %s" % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    return "This page is for making a new menu item for restaurant %s" % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return "This page is for editing menu item %s" % menu_id

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Menu item deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    
    else:
        return render_template('deleteMenuItem.html', restaurant_id = itemToDelete.restaurant_id, menu_id = itemToDelete.id, item = itemToDelete)





if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8080)