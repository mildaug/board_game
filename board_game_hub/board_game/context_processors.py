from .models import GameBorrowRequest

def new_requests_count(request):
    if request.user.is_authenticated:
        new_requests_count = GameBorrowRequest.objects.filter(request_status='New', owner=request.user).count()
    else:
        new_requests_count = 0

    return {'new_requests_count': new_requests_count}
