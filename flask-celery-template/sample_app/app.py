from flask import Flask, render_template, session, jsonify
from celery import Celery, Task

from config import Config

from routes.sample import sample_bp
from tasks.sample_tasks import sample_task


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)
    celery_app = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery_app.Task = FlaskTask
    celery_app.conf.from_object(Config)
    app.extensions['celery'] = celery_app
    # celery_app = Celery( app.name, broker=app.config['CELERY_BROKER_URL'], task_cls=FlaskTask )
    # celery_app.conf.update(app.config)
    # celery_app.set_default()
    return celery_app

f_app = Flask(__name__)
f_app.config.from_object(Config)
celery_app = celery_init_app(f_app)


f_app.register_blueprint(sample_bp, url_prefix='/sample')


@f_app.route('/', methods=['GET'])
def route_index():
    return render_template('index.html')


@f_app.route('/celery_results', methods=['GET'])
def celery_results():
    tasks_data = {
        'sample_tasks': [],
    }

    if session.get('sample_tasks'):
        sample_tasks_ids = session.get('sample_tasks').strip(',').split(',')
        for task_id in sample_tasks_ids:
            result = sample_task.AsyncResult(task_id)
            tasks_data['sample_tasks'].append({
                'state': result.state,
                'successful': result.successful(),
                'value': result.result if result.ready() else None,
                'info': result.info
            })

    return jsonify(tasks_data)


if __name__ == '__main__':
    f_app.run(port=5000, debug=True)
