from django.http import HttpResponseForbidden


def more_than_one_portfolio_only(func):
    def check_and_call(request, *args, **kwargs):
        if request.user.portfolios.count() == 1:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return check_and_call
