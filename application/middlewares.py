from django.contrib.sessions.models import Session
from django.contrib.auth import logout
from django.utils import timezone
from django.shortcuts import redirect

class SessionTimeoutMiddleware:
    def process_request(self, request):
        now = timezone.now()
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity', now)
            if (now - last_activity).total_seconds() > 240:
                logout(request)
                return redirect("login_page")
        request.session['last_activity'] = now

class OneSessionPerUserMiddleware:
    # Called only once when the web server starts
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print(request.user)
        
        if request.user.is_authenticated:
            print("authication-----------------------")
            # Gets the user's session_key from the database
            current_session_key = request.user.logged_in_user.session_key
            # If the session_key exists in the db and it is different from the browser's session
            if current_session_key and current_session_key != request.session.session_key:
                Session.objects.filter(session_key=current_session_key).delete()
            # Update the user's session_key in the db
            request.user.logged_in_user.session_key = request.session.session_key
            request.user.logged_in_user.save()

        response = self.get_response(request)

        # This is where you add any extra code to be executed for each request/response after
        # the view is called.
        # For this tutorial, we're not adding any code so we just return the response

        return response