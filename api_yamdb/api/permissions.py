from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (
                user.is_authenticated and user.is_admin
                or user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
                user.is_authenticated and user.is_admin
                or user.is_superuser
        )


class IsAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                    request.method in permissions.SAFE_METHODS
                    or request.user.is_admin
                    or request.user.is_superuser
            )


class IsAuthorOrModeratorPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
                request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator
        )


class IsAuthorOrModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
                request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator
        )
