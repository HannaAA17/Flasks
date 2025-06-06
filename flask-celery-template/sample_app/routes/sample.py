from flask import Blueprint, render_template


sample_bp = Blueprint('sample', __name__, template_folder='../templates')

@sample_bp.route("/", methods=["GET"])
def sample_index():
    return render_template('sample/index.html')
