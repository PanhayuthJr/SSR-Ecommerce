from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from my_app.models import Product, Category

# 🟢 Product List + Search
def index(request):
    if request.method == "POST":
        search_query = request.POST.get('search_item', '').strip()
        products = Product.objects.filter(product_name__icontains=search_query)
    else:
        products = Product.objects.all()

    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {
        "products": page_obj,
        "count_item": products.count()
    }
    return render(request, 'pages/products/index.html', data)


# 🟢 Show Create Form
def show(request):
    categories = Category.objects.all()
    return render(request, "pages/products/create.html", {"categories": categories})


# 🟢 Create Product
def create(request):
    if request.method == "POST":
        product = Product()
        product.product_name = request.POST['product_name']
        product.bar_code = request.POST['bar_code']
        product.sell_price = request.POST['sell_price']
        product.unit_in_stock = request.POST['unit_in_stock']
        product.category_id = request.POST['category_id']
        if 'photo' in request.FILES:
            product.photo = request.FILES['photo']

        product.full_clean()
        product.save()
        messages.success(request, "✅ Product created successfully!")
        return redirect("/product/index")


# 🟢 Delete Product
def delete(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    messages.success(request, "🗑️ Product deleted successfully!")
    return redirect("/product/index")


# 🟢 Edit Product (Display Form)
def edit(request, id):
    product = get_object_or_404(Product, pk=id)
    categories = Category.objects.all()
    return render(request, "pages/products/edit.html", {"product": product, "categories": categories})


# 🟢 Update Product
def update_by_id(request, id):
    product = get_object_or_404(Product, pk=id)

    # Update fields from form
    product.product_name = request.POST['product_name']
    product.bar_code = request.POST['bar_code']
    product.sell_price = request.POST['sell_price']
    product.unit_in_stock = request.POST['unit_in_stock']

    # ✅ Set category using the posted category_id
    product.category_id = request.POST['category_id']

    # Update photo if uploaded
    if 'photo' in request.FILES:
        product.photo = request.FILES['photo']

    # Validate and save
    product.full_clean()
    product.save()
    messages.success(request, "✅ Product updated successfully!")
    return redirect("/product/index")
