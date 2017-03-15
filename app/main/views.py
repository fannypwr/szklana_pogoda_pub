from flask import render_template, flash
from flask_login import login_required
from sqlalchemy import func

from app.main import main as main_bl
from app.main.forms import *
from app.models import Temperature, Place

ALL_THE_TEMPS = 'All the records regarding {} in our db'
PLACE_NOT_FOUND = 'Place not found'
TEMPERATURES_NOT_FOUND = 'No temperature records found for {}.'
TEMP_IN_C = 'Temperature *C'


@main_bl.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = SearchForm()
    kwargs = {}
    if form.validate_on_submit():
        pl = Place.query.filter(func.lower(Place.name) == func.lower(form.address.data)).first()
        if pl:
            address = pl.name
            temperature_objs = Temperature.query.filter_by(place_id=pl.id).order_by(Temperature.day).all()
            if temperature_objs:
                temperatures = [t.grades for t in temperature_objs]
                days = [t.day for t in temperature_objs]
            else:
                flash(TEMPERATURES_NOT_FOUND.format(address))
            try:
                series = [{"name": address, "data": [[[i[0].year, i[0].month, i[0].day], i[1]] for i in zip(days, temperatures)]}]
                chart_id = 'chart_1'
                chart = {'renderTo': 'container', 'type': 'spline', 'height': 350}
                x_axis = {
                    'type': 'datetime',
                    'title': {
                        'text': 'Date'
                    }
                }
                y_axis = {'plotLines': [{
                                         'value': 0,
                                         'width': 1,
                                         'color': '#808080'
                                      }],
                         'ordinal': 'false',
                         'title': {'text': TEMP_IN_C}}
                title = {'text': ALL_THE_TEMPS.format(address)}
                kwargs = dict(series_py=series, chart=chart, chart_id=chart_id, xAxis=x_axis, yAxis=y_axis, title=title)
            except Exception as ex:
                print(ex)
        else:
            flash(PLACE_NOT_FOUND)
    return render_template('main/dashboard.html', form=form, **kwargs)

