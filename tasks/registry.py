from tasks.fraction_tasks import FRACTION_TASKS
from tasks.integer_tasks import INTEGER_TASKS

TASK_FUNCTIONS = {**INTEGER_TASKS, **FRACTION_TASKS}

DOMAIN_OF_TYPE = {}
for type_name in INTEGER_TASKS:
    DOMAIN_OF_TYPE[type_name] = "integer"
for type_name in FRACTION_TASKS:
    DOMAIN_OF_TYPE[type_name] = "fraction"

ALL_TYPE_NAMES = list(TASK_FUNCTIONS)
