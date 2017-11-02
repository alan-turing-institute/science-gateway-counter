# This contains the standard config that all other configs inherit from

# A dictionary of URI stems for the various API actions
URI_STEMS = {'status': '/api/status'}
SECRET_KEY = 'my_precious'

MIDDLEWARE_ONLY_JOB_FIELDS = [
    'status',
]
