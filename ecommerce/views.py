from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import Http404
from django.utils.decorators import method_decorator

from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.views.generic import View, ListView, DetailView, DeleteView, CreateView

from ecommerce.forms import ItemCreationForm, InfoCreationForm, ItemImageForm
from ecommerce.models import *


@method_decorator(login_required, name='dispatch')
class HomeView(View):
    template_name = 'ecommerce/home.html'

    def get(self, request, *args, **kwargs) -> 'HttpResponse':
        user = request.user
        orders = user.order_set.filter(is_paid=True)

        return render(request, self.template_name, {
            'user': user,
            'orders': orders
        })


@method_decorator(login_required, name='dispatch')
class ItemView(DetailView):
    model = Item
    template_name = 'ecommerce/item/item_details.html'
    context_object_name = 'item'

    def post(self, request, *args, **kwargs) -> 'HttpResponse':
        try:
            item = self.get_object()
            if item.quantity == 0 or not item.available:
                return redirect(to='ecommerce.home')
            Item.objects.filter(pk=item.pk).update(quantity=F('quantity') - 1)
        except:
            return redirect(to='ecommerce:home')

        user = request.user
        order = Order(item=item, user=user, cart=user.cart_set.last(), price=item.price)
        order.save()
        return redirect(to='ecommerce:order', pk=order.pk)


@method_decorator(login_required, name='dispatch')
class ItemCreateView(CreateView):
    model = Item
    template_name = 'ecommerce/item/item_create.html'
    form_class = ItemCreationForm

    def form_valid(self, form):
        form.instance.user = User.objects.get(pk=self.request.user.pk)
        form.save()
        return redirect(to='ecommerce:item_create_details', pk=form.instance.id)


@method_decorator(login_required, name='dispatch')
class ItemDetailsView(DetailView):
    model = Item
    template_name = 'ecommerce/item/item_create_details.html'
    context_object_name = 'item'

    def get_queryset(self):
        return self.request.user.item_set


@method_decorator(login_required, name='dispatch')
class ItemCreateInfoView(CreateView):
    model = Info
    template_name = 'ecommerce/item/item_create.html'
    form_class = InfoCreationForm

    def form_valid(self, form) -> 'HttpResponse':
        form.instance.item = self.request.user.item_set.get(pk=self.request.GET.get('item_id'))
        form.save()
        return redirect(to='ecommerce:item_create_details', pk=form.instance.item.pk)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


@method_decorator(login_required, name='dispatch')
class ImageCreationView(CreateView):
    model = ItemImage
    template_name = 'ecommerce/item/item_create.html'
    form_class = ItemImageForm

    def form_valid(self, form) -> 'HttpResponse':
        form.instance.item = self.request.GET.get('item_id')
        form.save()
        return redirect(to='ecommerce:item_create_details', pk=form.instance.item.pk)


@method_decorator(login_required, name='dispatch')
class OrderView(DetailView):
    model = Order
    template_name = 'ecommerce/order/order_details.html'
    context_object_name = 'order'

    # def get_object(self, queryset=None):
    #     try:
    #         obj = super().get_object()
    #     except Http404:
    #         obj = self.request.user.order_set.last()
    #
    #     return obj

    def get_queryset(self):
        return self.request.user.order_set


@method_decorator(login_required, name='dispatch')
class OrderDeleteView(DeleteView):
    model = Order
    success_url = '/ecommerce/'
    template_name = 'ecommerce/order/order_confirm_delete.html'


@method_decorator(login_required, name='dispatch')
class CartDetailsView(View):
    template_name = 'ecommerce/cart/cart_details.html'

    def get(self, request, *args, **kwargs) -> 'HttpResponse':
        cart = get_object_or_404(request.user.cart_set, pk=kwargs['cart_id'])

        if not cart.is_active:
            messages.error(request, 'Invalid access to cart')
            return redirect(to='ecommerce:home')

        return render(request, self.template_name, {
            'cart': cart
        })

    def post(self, request, *args, **kwargs) -> 'HttpResponse':
        user = request.user
        cart = get_object_or_404(user.cart_set, pk=kwargs['cart_id'])

        if not cart.order_set.all():
            messages.error(request, 'Cart is empty')

            return render(request, self.template_name, {
                'cart': cart
            })

        if user.balance >= cart.get_total_price():
            return redirect(to='ecommerce:cart_checkout', cart_id=kwargs['cart_id'])

        messages.error(request, 'Insufficient funds!')

        return render(request, self.template_name, {
            'cart': cart
        })


@method_decorator(login_required, name='dispatch')
class CartCheckoutView(View):
    template_name = 'ecommerce/cart/checkout.html'

    def get(self, request, *args, **kwargs) -> 'HttpResponse':
        user = request.user
        cart = get_object_or_404(user.cart_set, pk=kwargs['cart_id'])

        return render(request, self.template_name, {
            'cart': cart
        })

    def post(self, request, *args, **kwargs) -> 'HttpResponse':
        user = request.user
        cart = get_object_or_404(user.cart_set, pk=kwargs['cart_id'])

        User.objects.filter(pk=user.pk).update(balance=F('balance') - cart.get_total_price())
        messages.success(request, f'Successfully purchased! Total: {cart.get_total_price()}')

        cart.order_set.update(is_paid=True)
        cart.is_active = False
        cart.save()

        user.cart_set.create(user=user)

        return redirect(to='ecommerce:home')


@method_decorator(login_required, name='dispatch')
class StoreView(ListView):
    template_name = 'ecommerce/store.html'
    model = Item
    paginate_by = 4
    context_object_name = 'items'


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    template_name = 'ecommerce/profile.html'

    def get(self, request, *args, **kwargs) -> 'HttpResponse':
        return render(request, self.template_name, {
            'user': request.user
        })


@method_decorator(login_required, name='dispatch')
class InboxView(View):
    template_name = 'ecommerce/inbox.html'

    def get(self, *args, **kwargs) -> 'HttpResponse':
        orders = Order.objects.filter(item__user=self.request.user)
        return render(self.request, self.template_name, {
            'orders': orders
        })

    def post(self, request, *args, **kwargs) -> 'HttpResponse':
        order = get_object_or_404(Order.objects.filter(item__user=request.user),
                                  pk=self.request.POST.get('order_id'))

        order.status = 'Shipped'
        order.save()

        return redirect(to='ecommerce:inbox')
