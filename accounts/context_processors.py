def user_background_color(request):
    if request.user.is_authenticated:
        background_color = request.user.background_color
    else:
        background_color = '#357e40'
    return {'user_background_color': background_color}
