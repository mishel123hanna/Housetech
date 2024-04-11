from rest_framework.permissions import BasePermission
from .models import PropertyImages
class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        if isinstance(obj, PropertyImages):
            # Return True if the user is the owner of the associated property
            return obj.property.user == request.user
        # Write permissions are only allowed to the owner of the property.
        return obj.user == request.user