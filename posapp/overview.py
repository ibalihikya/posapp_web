from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
#from posapp.auth import login_required
from posapp.db import get_db

bp = Blueprint('overview', __name__)
databaseName="public"
@bp.route('/overview')
def index():
    """Display a summary of sales and stock."""

    query = "SELECT sum(total) AS totalrevenue  FROM " + databaseName + ".transaction  \
                left join " + databaseName +  ".receipt on transaction.receiptId = receipt.receiptId \
                WHERE lastmodifieddate::timestamp >= current_timestamp - interval '24 hour';"
    past24 = getTotalSales(query)

    query = "SELECT sum(total) AS totalrevenue, EXTRACT(WEEK FROM CURRENT_TIMESTAMP) as week FROM " + databaseName + ".transaction  \
                left join " + databaseName +  ".receipt on transaction.receiptId = receipt.receiptId \
                WHERE EXTRACT(WEEK FROM lastmodifieddate::timestamp) = EXTRACT(WEEK FROM CURRENT_TIMESTAMP);"  
    current_week = getTotalSales(query)

    query = "SELECT sum(total) AS totalrevenue, EXTRACT(MONTH FROM CURRENT_TIMESTAMP) as month FROM " + databaseName + ".transaction  \
                left join " + databaseName +  ".receipt on transaction.receiptId = receipt.receiptId \
                where EXTRACT(MONTH FROM lastmodifieddate::timestamp) = EXTRACT(MONTH FROM CURRENT_TIMESTAMP);"
    current_month = getTotalSales(query)

    query = "SELECT sum(total) AS totalrevenue, EXTRACT(QUARTER FROM CURRENT_TIMESTAMP) as quarter FROM " + databaseName + ".transaction  \
                left join " + databaseName +  ".receipt on transaction.receiptId = receipt.receiptId \
                where EXTRACT(QUARTER FROM lastmodifieddate::timestamp) = EXTRACT(QUARTER FROM CURRENT_TIMESTAMP);"
    current_quarter = getTotalSales(query)

    low_stock_Items = getStockLowItems()


    return render_template('overview/index.html', past24=past24, current_week = current_week,
                current_month = current_month, current_quarter = current_quarter, low_stock_Items = low_stock_Items)

def getTotalSales(query):
    """Get total sales by day, month, quarter, year"""
    db = get_db()
    cur = db.cursor()
    cur.execute(query)          
    total = cur.fetchone()
    
    return total

def getStockLowItems():
    """Get all items that are low in stock."""
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT stockstatus.*, product.productName, product.stock_low_threshold  FROM " + databaseName + ".stockstatus " +
                    "LEFT JOIN " + databaseName + ".product ON stockstatus.productId = product.productId \
                    WHERE stockstatus.quantity <= product.stock_low_threshold;")
    items = cur.fetchall()

    return items