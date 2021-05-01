from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item, Order, OrderItem
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages
# Create your views here.


class HomeView(ListView):
    model = Item
    template_name = "home-page.html"

class ProductView(DetailView):
    model = Item
    template_name = "product-page.html"


def checkoutpage(request):
    context = {}
    return render (request, "checkout-page.html", context)

# Add product to the cart
@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Your item quantity was updated")
            return redirect("core:product", slug=slug)
        else:
            messages.info(request, "Your item was added to the cart")
            order.items.add(order_item)
            return redirect("core:product", slug=slug)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Your item was added to the cart")
        return redirect("core:product", slug=slug)

    return redirect("core:product", slug=slug)

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.quantity -= 1
            order_item.save()
            messages.info(request, "Your item is removed from the cart")
            return redirect("core:product", slug=slug)
        else:
            messages.info(request, "Your item was not in your cart")
            return redirect("core:product", slug=slug)

    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


def login_view(request):
    context={}
    return render (request, "account/login.html", context)


class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context= {
                'iron': order
            }
            return render(self.request, 'cart.html', context)

        except ObjectDoesNotExist:
            messages.error(self.request, "you do not have an active order")
            return redirect("/")
         