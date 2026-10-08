from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .models import Product, Category
from .forms import ProductForm


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, "login.html")


@login_required
def dashboard(request):
    total_products = Product.objects.count()

    active_products = Product.objects.filter(
        status=True
    ).count()

    inactive_products = Product.objects.filter(
        status=False
    ).count()

    low_stock_products = Product.objects.filter(
        stock__lte=5
    ).count()

    context = {
        "total_products": total_products,
        "active_products": active_products,
        "inactive_products": inactive_products,
        "low_stock_products": low_stock_products,
    }

    return render(
        request,
        "dashboard.html",
        context
    )


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def product_list(request):

    products = Product.objects.all().order_by("-created_at")

    search = request.GET.get("search", "")
    category = request.GET.get("category", "")
    status = request.GET.get("status", "")

    if search:
        products = products.filter(
            name__icontains=search
        )

    if category:
        products = products.filter(
            category_id=category
        )

    if status == "active":
        products = products.filter(
            status=True
        )

    elif status == "inactive":
        products = products.filter(
            status=False
        )

    paginator = Paginator(products, 5)

    page_number = request.GET.get("page")

    products = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        "products": products,
        "categories": categories,
        "search": search,
        "selected_category": category,
        "selected_status": status,
    }

    return render(
        request,
        "product_list.html",
        context
    )


@login_required
def product_create(request):

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Product added successfully."
            )

            return redirect("product_list")

    else:

        form = ProductForm()

    return render(
        request,
        "product_form.html",
        {
            "form": form,
            "title": "Add Product"
        }
    )


@login_required
def product_detail(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    return render(
        request,
        "product_detail.html",
        {
            "product": product
        }
    )


@login_required
def product_edit(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Product updated successfully."
            )

            return redirect("product_list")

    else:

        form = ProductForm(
            instance=product
        )

    return render(
        request,
        "product_form.html",
        {
            "form": form,
            "title": "Edit Product"
        }
    )


@login_required
def product_delete(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    if request.method == "POST":

        product.delete()

        messages.success(
            request,
            "Product deleted successfully."
        )

        return redirect("product_list")

    return render(
        request,
        "product_confirm_delete.html",
        {
            "product": product
        }
    )