from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render

import json

from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.views import View

from .models import Product, Order, Customer, OrderItem
from .forms import CustomerForm
from .filters import CustomerFilter
from Home.decorators import unauthenticated_user, allowed_users


def shop(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop.html', context)


@allowed_users(allowed_roles=['staff'])
def takes_order(request):
    customer = Customer.objects.all().order_by('-id')
    myFilter = CustomerFilter(request.GET, queryset=customer)
    customer = myFilter.qs
    context = {'customer': customer, 'myFilter': myFilter}
    return render(request, 'customer.html', context)


@allowed_users(allowed_roles=['staff'])
def create_customer(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order')

    context = {'form': form}
    return render(request, 'create_customer.html', context)


@allowed_users(allowed_roles=['staff'])
def manage_order(request, pk):
    customer = Customer.objects.get(id=pk)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems, 'customer': customer}
    return render(request, 'staff_shop.html', context)


@allowed_users(allowed_roles=['staff'])
def cart(request, pk):
    customer = Customer.objects.get(id=pk)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'customer': customer}
    return render(request, 'cart.html', context)


@allowed_users(allowed_roles=['staff'])
def checkout(request, pk):
    customer = Customer.objects.get(id=pk)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
    context = {'items': items, 'order': order, 'customer': customer, 'cartItems': cartItems}
    return render(request, 'checkout.html', context)


@allowed_users(allowed_roles=['staff'])
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    pk = data['pk']
    customer = Customer.objects.get(id=pk)
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = orderItem.quantity + 1
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class DownloadPDF(View):
    def get(self, request, pk, *args, **kwargs):
        customer = Customer.objects.get(id=pk)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        context = {'items': items, 'order': order, 'customer': customer, 'cartItems': cartItems}

        pdf = render_to_pdf('invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" % order.transaction_id
            content = "inline; filename=%s" % filename
            download = request.GET.get("download")
            if download:
                content = "attachment; filename=%s" % filename
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


def process_order(request):
    data = json.loads(request.body)
    pk = data['pk']
    customer = Customer.objects.get(id=pk)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    total = float(data['total'])

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    return JsonResponse("Order Done", safe=False)
