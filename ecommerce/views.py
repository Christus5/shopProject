from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.utils.decorators import method_decorator

from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.views.generic import View, DetailView, CreateView

from rest_framework import status, mixins
from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response

from ecommerce.forms import ItemCreationForm, InfoCreationForm, ItemImageForm
from ecommerce.models import *
from ecommerce.serializers import ItemSerializer, OrderSerializer


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
class ItemCreateView(CreateView):
    model = Item
    template_name = 'ecommerce/item/item_create.html'
    form_class = ItemCreationForm

    def form_valid(self, form):
        form.instance.user = User.objects.get(pk=self.request.user.pk)
        form.save()
        return redirect(to='ecommerce:item_create_details', pk=form.instance.id)


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


class ItemCreateAPIView(generics.CreateAPIView):
    queryset = Item.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ItemSerializer


class ItemAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ItemSerializer

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = request.user.item_set.get(pk=self.get_object().pk)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Item.DoesNotExist:
            return Response({
                'error': "Item either doesn't exist or user has no permission"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, *args, **kwargs):
        try:
            instance = request.user.item_set.get(pk=self.get_object().pk)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist:
            return Response({
                'error': "Item either doesn't exist or user has no permission"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)


@method_decorator(login_required, name='dispatch')
class ImageCreationView(CreateView):
    model = ItemImage
    template_name = 'ecommerce/item/item_create.html'
    form_class = ItemImageForm

    def form_valid(self, form) -> 'HttpResponse':
        form.instance.item = self.request.GET.get('item_id')
        form.save()
        return redirect(to='ecommerce:item_create_details', pk=form.instance.item.pk)


class OrderAPIView(generics.RetrieveDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        self.queryset = self.request.user.order_set.all()
        return super().get_queryset()

    def delete(self, request, *args, **kwargs) -> Response:
        order = self.get_object()
        if order.is_paid:
            return Response("can't remove already paid order", status=405)

        Item.objects.filter(pk=order.item.pk).update(quantity=F('quantity') + 1)
        return super().delete(request, *args, **kwargs)


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
    success_url = 'ecommerce:home'

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

        return redirect(to=self.success_url)


class StoreAPIView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]


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
        orders_q = Q(item__user=self.request.user) & Q(is_paid=True)

        orders = Order.objects.filter(orders_q)
        return render(self.request, self.template_name, {
            'orders': orders
        })

    def post(self, request, *args, **kwargs) -> 'HttpResponse':
        orders_q = Q(item__user=request.user) & Q(is_paid=True)
        order = get_object_or_404(
            Order.objects.filter(orders_q),
            pk=self.request.POST.get('order_id')
        )

        order.status = 'Shipped'
        order.save()

        return redirect(to='ecommerce:inbox')
