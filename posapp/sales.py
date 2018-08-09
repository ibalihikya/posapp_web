from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
#from posapp.auth import login_required
from posapp.db import get_db
from datetime import datetime

bp = Blueprint('sales', __name__)
databaseName="public"


@bp.route('/sales', methods=('GET','POST'))
def getSalesTransactions():
    """Query sales based on different criteria"""
    #products to populate dropdown list
    products = getproducts() 
    if request.method == 'POST':
        start_date = request.form['start_date']
        start_time = request.form['start_time']
        end_date = request.form['end_date']
        end_time = request.form['end_time']
        productid = request.form['products']
        view = request.form['view']
        
        
        error = None

        if not start_date:
            error = 'Start date is required'

        if not start_time:
            start_time = "00:00"

        if not end_time:
            end_time = "23:59"

        if error is not None:
            flash(error)
        else:
            start_date_time = start_date + " " + start_time
            if end_date:
                end_date_time = end_date + " " + end_time
            db = get_db()
            cur = db.cursor()
            query=""
            
            if view == "summary" :
                cur.execute("select product.productname, sum(transaction.total) as sum, sum(transaction.quantity)\
                 as productcount from " + databaseName + ".transaction left join " + databaseName + ".product on \
                 transaction.productid = product.productid GROUP BY product.productname;")
                
                itemsummary = cur.fetchall()
                return render_template('sales/sales.html', itemsummary=itemsummary)

            if productid == "" :
                if end_date:
                    query = "select transaction.*,  receipt.*, product.productName from " + databaseName +".transaction  \
                        left join " + databaseName +  ".receipt on transaction.receiptId = receipt.receiptId  \
                        left join " + databaseName + ".product on transaction.productId = product.productId \
                        WHERE receipt.lastModifiedDate > %(start_date_time)s AND receipt.lastModifiedDate < %(end_date_time)s;"
                    cur.execute(query, {'start_date_time':start_date_time, 'end_date_time':end_date_time})
                else:
                    query = "select transaction.*,  receipt.*, product.productName from " + databaseName +".transaction  \
                        left join " + databaseName +  ".receipt on transaction.receiptId = receipt.receiptId  \
                        left join " + databaseName + ".product on transaction.productId = product.productId \
                        WHERE receipt.lastModifiedDate > %(start_date_time)s;"
                    cur.execute(query, {'start_date_time':start_date_time})
            else:
                query = "select transaction.*,  receipt.*, product.productName from " + databaseName +".transaction  \
                        left join " + databaseName +  ".receipt on transaction.receiptId = receipt.receiptId  \
                        left join " + databaseName + ".product on transaction.productId = product.productId where \
                        receipt.lastModifiedDate > %(start_date_time)s AND receipt.lastModifiedDate < %(end_date_time)s \
                        AND transaction.productid= %(productid)s;"
                cur.execute(query, {'start_date_time':start_date_time, 'end_date_time':end_date_time, 'productid':productid})

            items = cur.fetchall()
            return render_template('sales/sales.html', items=items, products=products)
    return render_template('sales/sales.html', products=products)


def getproducts():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT product.* , category.* FROM " + databaseName + ".product " +
                                "LEFT JOIN " + databaseName + ".category ON product.categoryId = category.categoryId \
                                ORDER BY product.dateCreated;")
    products = cur.fetchall()
    return products

                          

