from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, ProductImage
from .forms import ProductForm, CategoryForm, ProductImageForm
from django.db.models import Count, Q

def index(request):
    product_form = ProductForm()
    category_form = CategoryForm()

    if request.method == 'POST':
        if 'product_form' in request.POST:
            product_form = ProductForm(request.POST, request.FILES)
            if product_form.is_valid():
                product = product_form.save(commit=False)
                product.save()

                for img in request.FILES.getlist('images'):
                    ProductImage.objects.create(product=product, image=img)

                product_form.save_m2m()
                return redirect('index')
        elif 'add_category' in request.POST:
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
                return redirect('index')
        elif 'remove_category' in request.POST:
            category_id = request.POST.get('remove_category')
            category = get_object_or_404(Category, pk=category_id)
            category.delete()
            return redirect('index')

    # Search and filter logic
    query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_images = request.GET.get('min_images')
    max_images = request.GET.get('max_images')
    category_ids = request.GET.getlist('categories')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if min_images:
        products = products.annotate(image_count=Count('images')).filter(image_count__gte=min_images)

    if max_images:
        products = products.annotate(image_count=Count('images')).filter(image_count__lte=max_images)

    if category_ids:
        products = products.filter(categories__id__in=category_ids).distinct()

    categories = Category.objects.all()

    return render(request, 'index.html', {
        'products': products,
        'product_form': product_form,
        'category_form': category_form,
        'categories': categories,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'min_images': min_images,
        'max_images': max_images,
        'selected_categories': category_ids,
    })

def remove_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product.delete()
    return redirect('index')

def remove_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        category.delete()
    return redirect('index')

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {
        'product': product,
    })
