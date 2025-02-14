from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from functools import wraps

app = Flask(__name__, static_folder='static')
app.secret_key = "your_secret_key"  # Change this to a secure key

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # Database instance
admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')  # Admin panel

# Database Models
class User(db.Model):  # Model for storing users
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Product(db.Model):  # Model for storing products
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    image = db.Column(db.String(200))

# Add models to 
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Product, db.session))

# Routes for your web pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Signup successful!')
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/products')
def products():
    all_products = Product.query.all()
    return render_template('product.html', products=all_products)
@app.route('/tech')
def tech():
    return render_template('tech.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Authenticate user (example logic)
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id  # Store user ID in session
            session['user_email'] = user.email
            flash('Login successful!', 'success')
            return redirect(url_for('index'))  # Redirect to homepage or dashboard
        else:
            flash('Invalid email or password!', 'danger')
    return render_template('login.html')  

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to log in first!', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function 



if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables in the database
    app.run(debug=True)