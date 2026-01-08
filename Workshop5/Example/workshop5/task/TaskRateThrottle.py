from rest_framework.throttling import UserRateThrottle

class TaskRateThrottle(UserRateThrottle):
    scope = 'tasks'