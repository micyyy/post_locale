from flask import Flask, render_template, request, redirect
import json
app = Flask(__name__)

_FILE = 'post_locale.json'
_datas = list()


def file_data_list(filename):
    datas = list()
    with open(filename, encoding='UTF-8') as f:
        datas = f.readlines()
    return datas


def get_cities():
    return file_data_list('cities.dat')


def get_sections():
    return file_data_list('sections.dat')


@app.route('/')
def home():
    return render_template('index.html', cities=get_cities(), sections=get_sections())


@app.route('/query', methods=['POST'])
def query():
    match = False
    city = request.form.get('city')
    road = request.form.get('road')
    section = request.form.get('section')

    if not city:
        return render_template('index.html', cities=get_cities(), sections=get_sections())

    rets = list()
    for data in _datas:
        if data['City'] in city and data['Road'].find((road.rstrip()+section.rstrip()))>=0:
            rets.append(data)
            match = True

    if not match:
        for data in _datas:
            if data['City'] in city and data['Road'].find((road.rstrip()))>=0 and data['Road'].find((section.rstrip()))>=0:            
                rets.append(data)

    return render_template('index.html', cities=get_cities(), sections=get_sections(), rets=rets, input_city=city, input_road=road, input_section=section)


if __name__ == '__main__':
    with open(_FILE) as jfile:
        _datas = json.load(jfile)

    app.run(port=15001, debug=True)
