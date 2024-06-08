from flask import Flask, render_template, request, jsonify, url_for, redirect

from db import Session, ToDo, Done

app = Flask(__name__)


class SessionSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.session = Session()


@app.route('/')
def index():
    return redirect(url_for('show_tasks'))


@app.route('/show_tasks')
def show_tasks():
    session = SessionSingleton()
    todo = session.session.query(ToDo).all()
    done = session.session.query(Done).all()
    return render_template('base.html', todo_tasks=todo, done_tasks=done)


@app.route('/move_task', methods=['POST'])
def move_task():
    data = request.json
    id = data.get('id')
    session = SessionSingleton()
    record = session.session.query(ToDo).get(id)

    new_task = Done(task=record.task, description=record.description, from_date=record.from_date,
                    due_date=record.due_date)

    session.session.delete(record)
    session.session.commit()

    session.session.add(new_task)
    session.session.commit()

    return jsonify({'status': 'success'})


@app.route('/delete_task', methods=['POST'])
def delete_task():
    data = request.json
    if data:
        data_dict = dict(data)
        id = data_dict.get('id')
        session = SessionSingleton()
        if data_dict["table"] == "ToDo":
            record = session.session.query(ToDo).get(id)
        elif data_dict["table"] == "Done":
            record = session.session.query(Done).get(id)
        session.session.delete(record)
        session.session.commit()
    return jsonify({'status': 'success'})


@app.route('/save_task', methods=['POST'])
def save_task():
    data = request.json
    task = data.get('task')
    description = data.get('description')
    from_date = data.get('from_date')
    due_date = data.get('due_date')

    new_task = ToDo(task=task, description=description, from_date=from_date, due_date=due_date)

    session = SessionSingleton()
    session.session.add(new_task)
    session.session.commit()

    return jsonify({'status': 'success', 'message': 'Task saved successfully'})


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()