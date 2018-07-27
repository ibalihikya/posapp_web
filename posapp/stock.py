from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from posapp.auth import login_required
from posapp.db import get_db

bp = Blueprint('stock', __name__)

@bp.route('/')
def index():
    db = get_db()
    cur = db.cursor()
    databaseName="public"
    cur.execute("SELECT stockstatus.*, product.productName  FROM " + databaseName + ".stockstatus " +
                            "LEFT JOIN " + databaseName + ".product ON stockstatus.productId = product.productId;")
    posts = cur.fetchall()

    return render_template('stock/index.html', posts=posts)