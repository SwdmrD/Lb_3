from django.contrib import messages
from django.db import connection
from django.shortcuts import redirect, render
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
    with connection.cursor() as cursor:
        cursor.execute("SELECT  dbo.LESS_THAN_AVG();")
        result = cursor.fetchone() #повертає кортеж, тому для результату треба використати перше значення
    return render(request, 'catalog/scalar_function.html', {'result':result[0]}) 


def update_item__price_procedure(id_item, price):
    with connection.cursor() as cursor:
        cursor.execute("""
            EXEC UpdatePrice
                @id = %s, 
                @Price = %s;
        """, [id_item, price])


def exception(request):
    if request.method == 'POST':
        form = UpdatePriceForm(request.POST)
        if form.is_valid():
            id_item = form.cleaned_data['id_item']
            price = form.cleaned_data['price']
            try:
                update_item__price_procedure(id_item, price)
                messages.success(request, 'Ціна успішно оновлена!')
                redirect('home')
            except Exception as e:
                clean_message = str(e).split(']')[-1].strip()
                clean_message = clean_message.split('(')[0].strip()
                messages.error(request, f'Помилка: {clean_message}')
    else:
        form = UpdatePriceForm()
    return render(request, 'catalog/exception.html', {'form': form})
