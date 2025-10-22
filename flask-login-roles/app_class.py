from flask import Flask, request, redirect, url_for, render_template_string, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, login_required,
    current_user, logout_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask.views import MethodView
from functools import wraps

# =====================================================
# Flask Setup
# =====================================================
app = Flask(__name__)
app.config["SECRET_KEY"] = "super-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# =====================================================
# Role Bit Flags
# =====================================================
class Roles:
    USER = 1 << 0
    EDITOR = 1 << 1
    ADMIN = 1 << 2
    SUPERUSER = 1 << 3

# =====================================================
# User Model
# =====================================================
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    roles = db.Column(db.Integer, default=Roles.USER)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role):
        return (self.roles & role) != 0

    def add_role(self, role):
        self.roles |= role

    def remove_role(self, role):
        self.roles &= ~role


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# =====================================================
# Role Decorator
# =====================================================
def roles_required(*required_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if not any(current_user.has_role(role) for role in required_roles):
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# =====================================================
# Views (Class-Based)
# =====================================================

class LoginView(MethodView):
    def get(self):
        return render_template_string("""
            <form method="post">
                <input name="username" placeholder="Username" required><br>
                <input type="password" name="password" placeholder="Password" required><br>
                <button type="submit">Login</button>
            </form>
        """)

    def post(self):
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("dashboard"))
        return "Invalid credentials", 401


class LogoutView(MethodView):
    decorators = [login_required]

    def get(self):
        logout_user()
        return redirect(url_for("login"))


class DashboardView(MethodView):
    decorators = [login_required, roles_required(Roles.USER, Roles.EDITOR, Roles.ADMIN)]

    def get(self):
        return f"<h1>Dashboard for {current_user.username}</h1>"


class AdminPanelView(MethodView):
    decorators = [login_required, roles_required(Roles.ADMIN, Roles.SUPERUSER)]

    def get(self):
        return f"<h1>Admin Panel — Access granted to {current_user.username}</h1>"


class HomeView(MethodView):
    def get(self):
        if current_user.is_authenticated:
            return render_template_string("""
                <h1>Welcome, {{ current_user.username }}!</h1>
                <p>Your role value: {{ current_user.roles }}</p>
                <a href="{{ url_for('dashboard') }}">Dashboard</a><br>
                <a href="{{ url_for('admin_panel') }}">Admin Panel</a><br>
                <a href="{{ url_for('logout') }}">Logout</a>
            """)
        return redirect(url_for("login"))

# =====================================================
# Register URL routes
# =====================================================
app.add_url_rule("/", view_func=HomeView.as_view("home"))
app.add_url_rule("/login", view_func=LoginView.as_view("login"))
app.add_url_rule("/logout", view_func=LogoutView.as_view("logout"))
app.add_url_rule("/dashboard", view_func=DashboardView.as_view("dashboard"))
app.add_url_rule("/admin", view_func=AdminPanelView.as_view("admin_panel"))

# =====================================================
# CLI command to initialize DB
# =====================================================
@app.cli.command("initdb")
def initdb():
    db.drop_all()
    db.create_all()

    user = User(username="user")
    user.set_password("user")

    editor = User(username="editor")
    editor.set_password("editor")

    admin = User(username="admin")
    admin.set_password("admin")

    superuser = User(username="superuser")
    superuser.set_password("superuser")

    db.session.add_all([user, editor, admin, superuser])
    db.session.commit()

    user.add_role(Roles.USER)
    editor.add_role(Roles.EDITOR)
    admin.add_role(Roles.ADMIN)
    superuser.add_role(Roles.SUPERUSER)
    db.session.commit()

    print("✅ Database initialized with demo users:")
    print("user / user (USER)")
    print("editor / editor (EDITOR)")
    print("admin / admin (ADMIN)")
    print("superuser / superuser (SUPERUSER)")

# =====================================================
# Run
# =====================================================
if __name__ == "__main__":
    app.run(debug=True)
