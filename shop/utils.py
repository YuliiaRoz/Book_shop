def show_toolbar_to_superuser(request):
    if hasattr(request, 'user'):
        return request.user.is_superuser
    else:
        return False