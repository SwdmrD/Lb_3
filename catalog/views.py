import os
from datetime import date, timedelta

from django.contrib import messages
from django.db import connection
from django.db.models import Avg, Count, Max, Min, Q, Subquery, Sum
from django.db.utils import OperationalError
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.urls import reverse
from django.views.generic import CreateView, DeleteView
from django.views.generic.edit import UpdateView
from django.db import connection
from django.shortcuts import render

from .forms import *
from .models import *


def sales_of_item(request):
    sql_query = """
        SELECT 
        catalog_item.id_item,
            catalog_item.type,
            catalog_item.price,
            catalog_supplier.company_name,
            COUNT(catalog_receipt.id_receipt) AS SALES_COUNT,
            SUM(catalog_receipt.the_item_cost) as SALES_TOTAL
        FROM 
            catalog_item 
        left JOIN 
            catalog_receipt ON catalog_item.id_item = catalog_receipt.id_item_id
        left JOIN
            catalog_supplier ON catalog_item.supplier_id = catalog_supplier.id_supplier
        GROUP BY 
            catalog_item.id_item,
            catalog_item.type,
            catalog_item.price,
            catalog_supplier.company_name
        ORDER BY 
            catalog_item.id_item;
        """
    items = Item.objects.raw(sql_query) 
    return render(request, 'catalog/table.html', {'items':items})


def call_insert_item_procedure(supplier_id, fabric_id, type, brand, size, gender, color, chemical_treatment, seasonality, state, price):
    supplier = supplier_id.id_supplier
    fabric = fabric_id.id_fabric
    with connection.cursor() as cursor:
        cursor.execute("""
            EXEC InsertItem
                @SupplierID = %s, 
                @FabricID = %s, 
                @Type = %s, 
                @Brand = %s, 
                @Size = %s, 
                @Gender = %s, 
                @Color = %s, 
                @ChemicalTreatment = %s, 
                @Seasonality = %s, 
                @State = %s, 
                @Price = %s;
        """, [supplier, fabric, type, brand, size, gender, color, chemical_treatment, seasonality, state, price])


def add_item(request):
    if request.method == 'POST':
            form = ItemForm(request.POST)
            if form.is_valid():
                supplier_id = form.cleaned_data['supplier']
                fabric_id = form.cleaned_data['fabric']
                type = form.cleaned_data['type']
                brand = form.cleaned_data['brand']
                size = form.cleaned_data['size']
                gender = form.cleaned_data['gender']
                color = form.cleaned_data['color']
                chemical_treatment = form.cleaned_data['chemical_treatment']
                seasonality = form.cleaned_data['seasonality']
                state = form.cleaned_data['state']
                price = form.cleaned_data['price']

                call_insert_item_procedure(
                    supplier_id, fabric_id, type, brand, size, gender, color, 
                    chemical_treatment, seasonality, state, price
                )
                return render(request, 'catalog/table.html')
    else:
        form = ItemForm()

    return render(request, 'catalog/add_item.html', {'form': form})


def table_function(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM GetPricePerSupplier();")
        results = cursor.fetchall()

    columns = ['company_name', 'average_price', 'total_price']
    data = [dict(zip(columns, row)) for row in results]

    return render(request, 'catalog/table_function.html', {'results':data})


def scalar_function(request):
    return render(request, 'catalog/table.html')


def statistics(request):
    # Середня ціна речей кожного бренду
    average_price_per_brand = Item.objects.values('brand').annotate(average_price=Avg('price'))
    # Кількість речей кожного бренду
    count_per_brand = Item.objects.values('brand').annotate(count=Count('id_item'))
    # Кількість речей за кожним постачальником
    count_per_supplier = Item.objects.values('supplier__company_name').annotate(count=Count('id_item'))
    # Середня ціна речей кожного постачальника
    average_price_per_supplier = Item.objects.values('supplier__company_name').annotate(average_price=Avg('price'))
    # Постачальники, у яких найбільше поставок
    most_deliveries = count_per_supplier.aggregate(Max('count'))['count__max']
    most_deliveries_suppliers = count_per_supplier.filter(count=most_deliveries)
    # Постачальники, у яких найменше поставок
    least_deliveries = count_per_supplier.aggregate(Min('count'))['count__min']
    least_deliveries_suppliers = count_per_supplier.filter(count=least_deliveries)
    # сума кожного чека
    start_of_last_week = datetime.now() - timedelta(days=datetime.now().weekday() + 7)
    end_of_last_week = start_of_last_week + timedelta(days=6)
    receipt_totals = Receipt.objects.filter(date_of_purchase__range=[start_of_last_week, end_of_last_week]).values(
        'number_of_receipt').annotate(total=Sum('the_item_cost'))
    # Найбільший чек
    biggest_receipt =receipt_totals.aggregate(Max('total'))['total__max']
    biggest_receipts = receipt_totals.filter(total=biggest_receipt)
    # Найменший чек
    smallest_receipt = receipt_totals.aggregate(Min('total'))['total__min']
    smallest_receipts = receipt_totals.filter(total=smallest_receipt)
    # Середня вартість товарів кожного типу тканини
    average_price_per_fabric_type = Item.objects.values('fabric__fabric_name').annotate(average_price=Avg('price'))

    context = {'average_price_per_brand': average_price_per_brand,
               'count_per_brand': count_per_brand,
               'count_per_supplier': count_per_supplier,
               'average_price_per_supplier': average_price_per_supplier,
               'most_deliveries_suppliers': most_deliveries_suppliers,
               'least_deliveries_suppliers': least_deliveries_suppliers,
               'biggest_receipts': biggest_receipts,
               'smallest_receipt': smallest_receipt,
               'smallest_receipts': smallest_receipts,
               'average_price_per_fabric_type': average_price_per_fabric_type,
               'receipt_totals': receipt_totals,
               }
    return render(request, 'catalog/Statistics.html', context)