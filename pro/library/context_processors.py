from library.models import *

def getcart(request):
    categ= BookCategory.objects.all()
    if request.user.is_authenticated:
        user = request.user
        order,created=UserOrder.objects.get_or_create(user=user,completed=False)
        items=order.orderitems_set.all()  
        cartItems=order.get_cart_items
        useradddres=UserAddress.objects.filter(user=request.user)
    else:
        items=[]
        order = {'get_cart_total':0,'get_cart_items':0}
        cartItems=0
        useradddres=[]
    return {"items":items,"order":order,"cartItems":cartItems,"useradddres":useradddres,"category":categ}