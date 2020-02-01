import json
import requests
from flask import Flask, render_template, url_for, redirect, session, flash
from flask_restful import Api
from flask_wtf import Form
from wtforms import SelectField

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = b'\x8e\xa1#\xefk\x9bw\xaa\xe9\x961-s\xc9/"6x\xb1*\xd9\x05\xe6\xe7'

api = Api(app)


class CategorySelect(Form):
    EventCategories = SelectField(u'Category', choices=[])


class EventSelect(Form):
    Events = SelectField(u'Event', choices=[])


@app.route('/', methods=['GET', 'POST'])
def category():
    # connect to server to fetch information
    url = 'http://localhost:1111'

    # requests json and parse it
    r = requests.get(url)
    data = r.json()


    # checking the response time
    # print ('\n//------------------------------//')
    # print('Response time for Yelp fusion API is: ')
    # print(r.elapsed.total_seconds())
    # print ('//------------------------------//\n')


    # populate the dropdown with info fetched from the api
    items = [(i['id'], i['title']) for i in data]
    form = CategorySelect()
    form.EventCategories.choices = items

    if form.is_submitted():
        chosen_category = form.EventCategories.data

        # save the category and pass it on to next session
        session['chosen_category'] = chosen_category

        return redirect(url_for('event'))

    return render_template('select_category.html', form=form)


@app.route('/event', methods=['GET', 'POST'])
def event():
    url = 'http://api.leedsinspired.co.uk/1.0/events.json'

    user_category = session.get('chosen_category')

    params = {
        'key': 'B8Tn2171l437434M6XvWyA1O77u5HAQ1Oor1E4B5k87Mi',
        'start_date': '22-11-2019',
        'end_date': '29-11-2019',
        'category_id': user_category
    }

    # send a request to api
    r = requests.get(url, params=params)

    # checking the response time
    # print ('\n//------------------------------//')
    # print('Response time for Yelp fusion API is: ')
    # print(r.elapsed.total_seconds())
    # print ('//------------------------------//\n')

    # parsing the json response from the api
    parsed = json.loads(r.text)
    objects = parsed['objects']

    event_list = []

    for i in objects:
        events = {
            'Title': i.get('event_title'),
            'Date': i.get('event_date'),
            'Location': i.get('place_title'),
            'Organiser': i.get('organiser_title'),
            'Description': i.get('description'),
        }

        session['Location'] = events['Location']

        event_list.append(events)

    # assign events to the dropdown - (address on the backend, event title on the front end)
    items = [(i['place_title'], i['event_title']) for i in objects]
    form = EventSelect()
    form.Events.choices = items

    if form.validate_on_submit():
        # so this will now save THE VENUE!!
        chosen_event = form.Events.data

        # save the category and pass it on to next session
        session['chosen_event'] = chosen_event

        return redirect(url_for('yelp'))

    return render_template('list_events.html', form=form, event_list=event_list)


@app.route('/event/yelp', methods=['GET', 'POST'])
def yelp():
    url = "https://api.yelp.com/v3/businesses/search"

    api_key = 'whk7nbgSJ1NudrqZEm9tBX6Wq5OFGYjsWzTzmYcaLQIH2IMPofsU-MeVyRRDI9AFdxeUCrTOzuTRUNutxxfrZiCuJ7gda2PJYJcQiD8Ft6TVpkxAF10J9TV0oFPRXXYx'

    headers = {
        'Authorization': 'Bearer %s' % api_key
    }

    search_term = session.get('chosen_event')

    params = {
        'term': search_term,
        'location': 'Leeds',
        'limit': '5'
    }

    # sending a request to api
    r = requests.get(url, headers=headers, params=params)

    # checking the response time
    # print ('\n//------------------------------//')
    # print('Response time for Yelp fusion API is: ')
    # print(r.elapsed.total_seconds())
    # print ('//------------------------------//\n')

    # parse the json response
    parsed = json.loads(r.text)
    businesses = parsed['businesses']

    business_list = []

    for i in businesses:
        business_info = {
            'Name': i.get('name'),
            'Rating': i.get('rating'),
            'Price': i.get('price'),
            'Address': ", ".join(i['location']['display_address']),
            'Phone': i.get('display_phone'),
        }

        business_list.append(business_info)

    return render_template('yelp_list.html', business_list=business_list, search_term=search_term)


if __name__ == '__main__':
    app.run(port=1234, debug=True)
