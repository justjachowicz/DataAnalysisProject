from flask import render_template, Blueprint, request
from . import db

data = Blueprint('data', __name__)


@data.route('/add', methods=["GET", "POST"])
def add():
    """
    add data from form to database
    :return: add html page
    """
    if request.method == "POST":
        table = request.form.get('table')
        country = request.form.get('country')
        year = request.form.get('year')
        index = request.form.get('index')
        index_column_name = ''

        if table == 'life_quality':
            index_column_name = 'life_quality'
        elif table == 'bipolarDisorder':
            index_column_name = 'bipolar_disorder_index'
        elif table == 'depression':
            index_column_name = 'depression_index'
        elif table == 'eatingDisorder':
            index_column_name = 'eating_disorder_index'
        elif table == 'schizophrenia':
            index_column_name = 'schizophrenia_index'

        conn = db.get_db()
        conn.execute(f'INSERT INTO {table} (country, year, {index_column_name}) VALUES (?, ?, ?)',
                     (country, year, index))
        conn.commit()
        conn.close()

    return render_template('add.html', title='Add data')
