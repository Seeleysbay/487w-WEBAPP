from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'

db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(300))


@app.route('/')
def index():
    return redirect(url_for('browse_items'))


@app.route('/items')
def browse_items():
    items = Item.query.all()
    return render_template('browse.html', items=items)


@app.route('/items/sort/<criteria>')
def sort_items(criteria):
    if criteria == "id":
        items = Item.query.order_by(Item.id).all()
    elif criteria == "name":
        items = Item.query.order_by(Item.name).all()
    else:
        items = Item.query.all()
    return render_template('browse.html', items=items)


@app.route('/items/search', methods=['POST'])
def search_items():
    keyword = request.form['keyword']

    try:
        keyword_as_int = int(keyword)
        items = Item.query.filter((Item.name.contains(keyword)) | (Item.id == keyword_as_int)).all()
    except ValueError:
        items = Item.query.filter(Item.name.contains(keyword)).all()

    return render_template('browse.html', items=items)


@app.route('/items/add', methods=['GET', 'POST'])
def add_item():
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        image = request.form['image']
        item = Item(name=name, description=description, image=image)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('browse_items'))
    return render_template('add.html')


@app.route('/items/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = Item.query.get(item_id)
    if request.method == "POST":
        item.name = request.form['name']
        item.description = request.form['description']
        item.image = request.form['image']
        db.session.commit()
        return redirect(url_for('browse_items'))
    return render_template('edit.html', item=item)


@app.route('/items/delete/<int:item_id>')
def delete_item(item_id):
    item = Item.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('browse_items'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

