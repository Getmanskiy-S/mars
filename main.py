from flask import Flask, render_template

app = Flask(__name__)


@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    return render_template('base.html', title=title)


@app.route('/training/<prof>')
def training(prof):
    return render_template('training.html', prof=prof.lower())


@app.route('/list_prof/<lst>')
def list_prof(lst):
    professions = [
        'Астронавт',
        'Астрофизик',
        'Космический инженер',
        'Космический биолог',
        'Космогеолог',
        'Специалист по управлению полетами',
        'Разработчик ракетных двигателей',
        'Специалист по спутниковой связи',
        'Космический архитектор',
        'Космический врач',
        'Специалист по космическому праву',
        'Оператор телескопа',
        'Планетолог',
        'Разработчик скафандров',
        'Техник по обслуживанию космической техники',
        'Специалист по радиационной безопасности в космосе'
    ]
    return render_template('list_prof.html', lst=lst, professions=professions)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
