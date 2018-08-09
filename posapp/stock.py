from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
#from posapp.auth import login_required
from posapp.db import get_db

bp = Blueprint('stock', __name__)
databaseName="public"
@bp.route('/')
def index():
    """Get all records from stockstatus table."""
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT stockstatus.*, product.productName, product.stock_low_threshold  FROM " + databaseName + ".stockstatus " +
                    "LEFT JOIN " + databaseName + ".product ON stockstatus.productId = product.productId;")
    items = cur.fetchall()

    return render_template('stock/index.html', items=items)

@bp.route('/stock')
def getStockTransactions():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT stock.* , product.productName FROM " +
                            databaseName + ".stock " +
                            "LEFT JOIN " + databaseName + ".product ON stock.productId = product.productId;")
    items = cur.fetchall()
    return render_template('stock/stock.html',items=items)