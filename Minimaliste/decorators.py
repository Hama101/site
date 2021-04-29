from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request , *args , **kwargs):
        if not request.user.is_authenticated :
            return redirect('login')
        else:
            return view_func(request , *args , **kwargs)

    return wrapper_func

def paied_users(allowed_roles = []):
    def decorator(view_func):
        def wrapper_fucn(request , *args , **kwargs):
            group = None

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles :
                return view_func(request , *args , **kwargs)
            else :
                return redirect('payment')
        return wrapper_fucn
    return decorator