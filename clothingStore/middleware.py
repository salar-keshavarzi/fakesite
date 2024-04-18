from basket.models import Basket


class BasketMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    # def __call__(self, request):
    #     basket_id = request.COOKIES.get('basket_id', None)
    #     if basket_id:
    #         if Basket.objects.filter(id=basket_id).exists():
    #             basket = basket_id
    #         else:
    #             basket = Basket.objects.create().id
    #     else:
    #         basket = Basket.objects.create().id
    #     basket_quantities = Basket.objects.get(id=basket).get_total_quantity()
    #     response = self.get_response(request)
    #     response.set_cookie('basket_id', basket, max_age=7776000)
    #     response.set_cookie('basket_quantities', basket_quantities, max_age=7776000)
    #     return response

    def __call__(self, request):
        basket_id = request.COOKIES.get('basket_id', None)
        if basket_id:
            try:
                basket = Basket.objects.get(id=basket_id)
            except:
                basket = Basket.objects.create()
        else:
            basket = Basket.objects.create()
        response = self.get_response(request)
        basket_quantities = basket.get_total_quantity()
        response.set_cookie('basket_id', basket.id, max_age=7776000)
        response.set_cookie('basket_quantities', basket_quantities, max_age=7776000)
        return response
