# This contains the standard config that all other configs inherit from

# A dictionary of URI stems for the various API actions
URI_STEMS = {'status': '/api/status'}

MIDDLEWARE_ONLY_JOB_FIELDS = [
    'status',
]
