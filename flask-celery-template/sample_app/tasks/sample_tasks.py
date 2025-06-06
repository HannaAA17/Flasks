import datetime
from celery import shared_task


@shared_task(bind=True, ignore_result=False)
def sample_task(self_):
    start_state = {
        'id':self_.id,
        'type': 'alpha',
        'started_on': datetime.datetime.now().timestamp()
    }
    
    self_.update_state( state='PROGRESS', meta=start_state )
    
    try:
        ...
    except Exception as e:
        return {
            **start_state, 
            'error': str(e), 
            'finished_on': datetime.datetime.now().timestamp(),
        }

    return {
        **start_state, 
        'result': 'finished successfully', 
        'finished_on': datetime.datetime.now().timestamp(),
    }
# end task_

# task = sample_task.delay()