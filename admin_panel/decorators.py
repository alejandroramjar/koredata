from functools import wraps
from rest_framework.response import Response
from rest_framework import status
import logging


logger = logging.getLogger(__name__)
def superuser_required(func):
    @wraps(func)
    def wrapped(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            logger.warning(f'El usuario {request.user.username} no tiene permitido ejecutar esta acción.')
            return Response({'error': 'El usuario no tiene permitido ejecutar esta acción.'},
                            status=status.HTTP_403_FORBIDDEN)
        return func(self, request, *args, **kwargs)
    return wrapped
