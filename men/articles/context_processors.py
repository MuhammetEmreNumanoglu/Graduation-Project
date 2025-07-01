from .models import Profile

def profile_pic(request):
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        if not profile:
            profile = Profile.objects.create(user=request.user)
        return {'profilePic': profile}
    return {'profilePic': None} 