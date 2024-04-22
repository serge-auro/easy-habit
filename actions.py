PERIOD = ("month", "week")
FREQUENCY = ("ежедневно", "еженедельно", "ежемесячно")


def init_user(user_id):
    pass


def get_habit_status(user_id):
    pass


def report(user_id, habit_id, period: PERIOD):
    pass


def edit_habit(user_id, habit_id, active: bool, frequency_name: FREQUENCY, frequency_count):
    pass


def mark_habit(user_id, habit_id):
    pass


def user_notify():
    pass
