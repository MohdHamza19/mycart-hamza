from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Order, OrderUpdate, Review, Signup, CurrentUser
from math import ceil
import json
import re


# Create your views here.
def index(request):
    products = Product.objects.all()
    prd = []
    for i in range(len(products)):
        prd.append(products[i])
    # print(prd)
    prd1 = []
    [prd1.append(i) for i in prd[::-1]]
    # print(prd1)
    prd2 = prd1[:8]
    # print(prd2)
    prd3 = prd1[:6]
    # print(prd2)
    # for i in range(len(prd[-1:])):
    #     prd1.append(i)
    # print(prd1)
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    categ = ['Phones', 'Laptops', 'Smart watches', 'Headphones', 'Vaccum Cleaners', 'Mixers', 'Refrigerators', 'Lamps', 'Tables', 'Sofa sets']
    # categs={'categ' : categ}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - n // 4)
        allProds.append([prod, range(1, nSlides), nSlides])
    # print(allProds)
    params = {'allProds': allProds, 'categ': categ, 'prd2': prd2, 'prd3': prd3}
    return render(request, 'shop/index.html', params)


def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.desc or query in item.product_name or query in item.category:
    # if query in item.product_name.lower() or query in item.category.lower() or query in item.product_name or query in item.category:
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    # print(query)
    allProds = []
    catprods = Product.objects.values('category', 'id')
    # print(catprods)
    cats = {item['category'] for item in catprods}
    # print(cats)
    categ = ['Phones', 'Laptops', 'Smart watches', 'Headphones', 'Vaccum Cleaners', 'Mixers',  'Refrigerators', 'Lamps', 'Tables', 'Sofa sets']
    # categs={'categ' : categ}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - n // 4)
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
            # print(allProds)
    params = {'allProds': allProds, 'categ': categ, 'msg': '', 'query': query}
    if len(allProds) == 0:
        params = {'msg': "No products were found matching your selection."}
    return render(request, 'shop/search.html', params)


def productView(request, myid):
    product = Product.objects.filter(id=myid)
    num = product[0].Number_of_images
    stock = product[0].stock
    # print(stock)
    # print(num)
    reshow = Review.objects.all()
    # print(reshow)
    res = []
    nu = []
    counter = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    # print(counter)
    categ = ['Phones', 'Laptops', 'Smart watches', 'Headphones', 'Vaccum Cleaners', 'Mixers', 'Refrigerators', 'Lamps', 'Tables', 'Sofa sets']
    for item in reshow:
        if item.revid == myid:
            res.append([item.review, item.rating, item.name, item.timestamp])
            # print(item.rating)
            counter[item.rating] = counter.get(item.rating) + 1
    print(counter)
    print(counter.get(5))
    print(counter.get(4))
    print(counter.get(3))
    print(counter.get(2))
    print(counter.get(1))
    try:
        wa = ((5 * counter.get(5)) + (4 * counter.get(4)) + (3 * counter.get(3)) + (2 * counter.get(2)) + (
                1 * counter.get(1))) / \
             (counter.get(5) + counter.get(4) + counter.get(3) + counter.get(2) + counter.get(1))
    except:
        print("division by zero error")
        wa = 0
    nu.append([num])

    return render(request, 'shop/productView.html',
                  {'product': product[0], 'res': res, 'categ': categ, 'num': num, 'stock': stock, 'wa': wa})


def login(request):
    categ = ['Phones', 'Laptops', 'Smart watches', 'Headphones', 'Vaccum Cleaners', 'Mixers', 'Refrigerators', 'Lamps', 'Tables', 'Sofa sets']
    if request.method == "POST":
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        mail = email
        signupp = Signup.objects.all()
        print(signupp)
        for item in signupp:
            if item.email == email and item.password == password:
                login = True
                curr = CurrentUser(email=email, password=password)
                curr.save()
                return render(request, 'shop/login.html', {'login': login, 'categ': categ, 'mail': mail})
        login = False
        return render(request, 'shop/login.html', {'login': login, 'categ': categ})
    return render(request, 'shop/login.html', {'categ': categ})


def category(request, cat):
    categ = ['Phones', 'Laptops', 'Smart watches', 'Headphones', 'Vaccum Cleaners', 'Mixers', 'Refrigerators', 'Lamps', 'Tables', 'Sofa sets']
    catprods = Product.objects.filter(category=cat)
    categoryy = cat
    print(catprods)
    for i in catprods:
        print(i)
    return render(request, 'shop/productbycategory.html', {'catprods': catprods, 'categ': categ, 'categoryy':categoryy})


# width: 270px;
# height: 250px;


#     function updatePopover(cart) {
# //        console.log('We are inside updatePopover');
#         var popStr = "";
#         popStr = popStr + "<div style='display: flex; justify-content: center;'><h5> Your Cart </h5></div><div class='mx-2 my-2'>";
#         var i = 1;
#         for (var item in cart) {
#             popStr = popStr + "<b>" + i + "</b>. ";
# //            na=document.getElementById('name' + item).innerHTML.length;
# //            console.log(na);
#             if (document.getElementById('name' + item).innerHTML.length>17){
#                 popStr = popStr + document.getElementById('name' + item).innerHTML.slice(0, 17) + "... | Qty: " + cart[item][0] + '<br>';
#             }
#             else if (document.getElementById('name' + item).innerHTML.length<17){
#                 popStr = popStr + document.getElementById('name' + item).innerHTML.slice(0, 17) + " | Qty: " + cart[item][0] + '<br>';
#             }
# //            popStr = popStr + document.getElementById('name' + item).innerHTML.slice(0, 19) + "... Qty: " + cart[item][0] + '<br>';
#             i = i + 1;
#         }
#         popStr = popStr + "</div> <a href='/shop/checkout'><button class='btn btn-primary' id ='checkout'>Checkout</button></a> <button class='btn btn-primary' onclick='clearCart()' id ='clearCart'>Clear Cart</button>"
#         document.getElementById('popcart').setAttribute('data-content', popStr);
#         if (screen.width>991)
#         {
#             $('#popcart').popover('show');
#         }
#         else
#         {
#             $('#popcart').popover();
#         }
#     }


def about(request):
    categ = ['Phones', 'Laptops', 'Smart watches', 'Headphones', 'Vaccum Cleaners', 'Mixers', 'Refrigerators', 'Lamps', 'Tables', 'Sofa sets']
    return render(request, 'shop/about.html', {'categ': categ})


def signout(request):
    categ = ['Phones', 'Laptops', 'Smart watches', 'Headphones', 'Vaccum Cleaners', 'Mixers', 'Refrigerators', 'Lamps', 'Tables', 'Sofa sets']
    if request.method == "POST":
        cu=CurrentUser.objects.all()
        cu.delete()
        out=True
        # print(cu)
        return render(request, 'shop/signout.html', {'categ': categ, 'out':out})
    return render(request, 'shop/signout.html', {'categ': categ})


def signup(request):
    categ = ['Phones', 'Laptops', 'Smart watches', 'Headphones', 'Vaccum Cleaners', 'Mixers', 'Refrigerators', 'Lamps', 'Tables', 'Sofa sets']
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        password = request.POST.get('password', '')
        # print(name, email, phone, desc)
        signup = Signup(name=name, email=email, phone=phone, password=password)
        signup.save()
        signedup = True
        # return render(request, 'shop/contact.html', {'thank': thank, 'categ': categ})
        return render(request, 'shop/signup.html', {'signedup': signedup, 'categ': categ})
    return render(request, 'shop/signup.html', {'categ': categ})


def contact(request):
    thank = False
    categ = ['Phones', 'Laptops', 'Smart watches', 'Headphones', 'Vaccum Cleaners', 'Mixers', 'Refrigerators', 'Lamps', 'Tables', 'Sofa sets']
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        # print(name, email, phone, desc)
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank': thank, 'categ': categ})


def yourOrders(request):
    categ = ['Phones', 'Laptops', 'Smart watches', 'Headphones', 'Vaccum Cleaners', 'Mixers', 'Refrigerators', 'Lamps', 'Tables', 'Sofa sets']
    current = CurrentUser.objects.all()
    print(current[0].email)
    # try:
    #     filt = Order.objects.filter(email=current[0].email)
    # except:
    #     logged=False
    #     return render(request, 'shop/yourOrders.html', {'categ': categ, 'logged':logged})
    filt = Order.objects.filter(email=current[0].email)
    print(filt)
    itm = []
    # ts=[]
    # for k in filt:
    #     ts.append(k.timestamp)
    # print(ts)
    for i in filt:
        itm.append("")
        itm.append(i.timestamp)
        itm.append(i.p_name1)
        itm.append(i.p_id1)
        itm.append(i.p_quantity1)
        if i.p_name2 != "":
            itm.append(i.p_name2)
        if i.p_id2 != "":
            itm.append(i.p_id2)
        if i.p_quantity2 != "":
            itm.append(i.p_quantity2)
        if i.p_name3 != "":
            itm.append(i.p_name3)
        if i.p_id3 != "":
            itm.append(i.p_id3)
        if i.p_quantity3 != "":
            itm.append(i.p_quantity3)
        if i.p_name4 != "":
            itm.append(i.p_name4)
        if i.p_id4 != "":
            itm.append(i.p_id4)
        if i.p_quantity4 != "":
            itm.append(i.p_quantity4)
        if i.p_name5 != "":
            itm.append(i.p_name5)
        if i.p_id5 != "":
            itm.append(i.p_id5)
        if i.p_quantity5 != "":
            itm.append(i.p_quantity5)
        if i.p_name6 != "":
            itm.append(i.p_name6)
        if i.p_id6 != "":
            itm.append(i.p_id6)
        if i.p_quantity6 != "":
            itm.append(i.p_quantity6)

    print(itm)
    itez = itm[1:]
    print(itez)
    rest = [[]]
    cnt = 1
    for i in itez:
        if not i:
            rest.append([])
            cnt += cnt
        else:
            rest[-1].append(i)
    print(rest)
    print(cnt)
    # for j in itm:
    #     print(j)
    #     cnt = j.count('"pr')
    # waa=re.findall(re.escape('p') + "(.*)" + re.escape('item:1'), j)
    # print(waa)
    # wab=re.findall(re.escape(':') + "(.*)" + re.escape(']'), str(waa))
    # print(wab)
    # wac = re.findall(re.escape('[') + "(.*)" + re.escape(']'), str(wab))
    # print(wac)
    # wad_id = re.findall(re.escape('r') + "(.*)" + re.escape('":['), str(waa))
    # print(wad_id)
    # wae = re.findall(re.escape(',') + "(.*)" + re.escape('"'), str(wac))
    # print(wae)
    # wad_name = re.findall(re.escape('"') + "(.*)" + re.escape('"'), str(wae))
    # print(wad_name)

    # print("The count is:", cnt)
    return render(request, 'shop/yourOrders.html', {'categ': categ, 'rest': rest, 'cnt': cnt})


def tracker(request):
    categ = ['Phones', 'Laptops', 'Smart watches', 'Headphones', 'Vaccum Cleaners', 'Mixers', 'Refrigerators', 'Lamps', 'Tables', 'Sofa sets']
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                # print(update)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(updates, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')
    return render(request, 'shop/tracker.html', {'categ': categ})


# def tracker(request):
#     if request.method=="POST":
#         orderId = request.POST.get('orderId', '')
#         email = request.POST.get('email', '')
#         try:
#             order = Order.objects.filter(order_id=orderId, email=email)
#             if len(order)>0:
#                 update = OrderUpdate.objects.filter(order_id=orderId)
#                 updates = []
#                 for item in update:
#                     updates.append({'text': item.update_desc, 'time': item.timestamp})
#                     response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
#                 return HttpResponse(response)
#             else:
#                 return HttpResponse('{"status":"noitem"}')
#         except Exception as e:
#             return HttpResponse('{"status":"error"}')
#
#     return render(request, 'shop/tracker.html')


def review(request, rid):
    product = Product.objects.filter(id=rid)
    categ = ['Phones', 'Laptops', 'Smart watches', 'Headphones', 'Vaccum Cleaners', 'Mixers', 'Refrigerators', 'Lamps', 'Tables', 'Sofa sets']
    if request.method == "POST":
        revid = request.POST.get('revid', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        rating = request.POST.get('rating', '')
        review = request.POST.get('review', '')
        curev = Order.objects.filter(email=email)
        cure = []
        # # print(curev[0].name)
        for item in curev:
            cure.append(item.email)
        # print(cure)
        review = Review(revid=revid, name=name, email=email, rating=rating, review=review)
        # review = Review(name=name, email=email,rating=rating,review=review)
        if email in cure:
            review.save()
        thank = True
        return render(request, 'shop/review.html', {'thank': thank, 'categ': categ})
    # print(product)
    return render(request, 'shop/review.html', {'product': product[0], 'categ': categ})


def checkout(request):
    categ = ['Phones', 'Laptops', 'Smart watches', 'Headphones', 'Vaccum Cleaners', 'Mixers', 'Refrigerators', 'Lamps', 'Tables', 'Sofa sets']
    if request.method == "POST":
        name = request.POST.get('name', '')
        itemsJson = request.POST.get('itemsJson', '')
        print(itemsJson)
        # print(itemsJson[4:5])
        # print(itemsJson[8:9])

        count = itemsJson.count('"pr')

        # print count
        print("The count is:", count)

        ite1 = itemsJson[:17]
        # print(ite1)
        b3 = re.findall(re.escape('"') + "(.*)" + re.escape(','), ite1)[0]
        # print(b3)
        b4 = re.findall(re.escape('p') + "(.*)" + re.escape(':'), b3)[0]
        # print(b4)
        prod1 = re.findall(re.escape('r') + "(.*)" + re.escape('"'), b4)[0]
        print("prod1:" + prod1)
        q1 = re.findall(re.escape(':') + "(.*)" + re.escape(','), ite1)[0]
        # print(q1)
        quan1 = re.findall(re.escape(':') + "(.*)" + re.escape(','), ite1)[0]
        # print(quan1)
        quant1 = re.findall(re.escape('[') + "(.*)" + re.escape(''), quan1)[0]
        name12 = re.findall(re.escape(',"') + "(.*)" + re.escape('item:1'), itemsJson)[0]
        # print(name12)
        name1 = re.findall(re.escape('') + "(.*)" + re.escape('",'), name12)[0]
        print("name1:" + name1)

        try:
            if len(quant1) > 1:
                quant1 = re.findall(re.escape('') + "(.*)" + re.escape(','), quant1)[0]

        except:
            print("the stringified number is in range > 9 and <99")
        print("quant1:" + quant1)

        p1 = int(prod1)
        q1 = int(quant1)

        prr1 = Product.objects.filter(id=p1)
        ps1 = prr1[0].stock
        pchange1 = (int(ps1) - q1)
        Product.objects.filter(id=p1).update(stock=pchange1)
        # print(gp)
        # print(gp[3:5])  # prod1
        # a2=gp[3:5]
        # print(a2)

        if count == 2:
            st2 = itemsJson
            result = re.search('item:1"],(.*)"item:2', st2)
            c3 = result.group(1)
            # print(c3)
            c4 = re.findall(re.escape('p') + "(.*)" + re.escape(':'), c3)[0]
            # print(c4)
            prod2 = re.findall(re.escape('r') + "(.*)" + re.escape('"'), c4)[0]
            print("prod2:" + prod2)
            quant2 = re.findall(re.escape(':[') + "(.*)" + re.escape(',"'), c3)[0]
            print("quant2:" + quant2)
            name22 = re.findall(re.escape('item:1') + "(.*)" + re.escape('item:2'), itemsJson)[0]
            # print(name22)
            name23 = re.findall(re.escape(',"') + "(.*)" + re.escape('",'), name22)[0]
            # print(name23)
            name2 = re.findall(re.escape(',"') + "(.*)" + re.escape(''), name23)[0]
            print("name2:" + name2)

            p2 = int(prod2)
            q2 = int(quant2)

            prr2 = Product.objects.filter(id=p2)
            ps2 = prr2[0].stock
            pchange2 = (int(ps2) - q2)
            Product.objects.filter(id=p2).update(stock=pchange2)

        if count == 3:
            st2 = itemsJson
            result = re.search('item:1"],(.*)"item:2', st2)
            c3 = result.group(1)
            # print(c3)
            c4 = re.findall(re.escape('p') + "(.*)" + re.escape(':'), c3)[0]
            # print(c4)
            prod2 = re.findall(re.escape('r') + "(.*)" + re.escape('"'), c4)[0]
            print("prod2:" + prod2)
            quant2 = re.findall(re.escape(':[') + "(.*)" + re.escape(',"'), c3)[0]
            print("quant2:" + quant2)
            name22 = re.findall(re.escape('item:1') + "(.*)" + re.escape('item:2'), itemsJson)[0]
            # print(name22)
            name23 = re.findall(re.escape(',"') + "(.*)" + re.escape('",'), name22)[0]
            # print(name23)
            name2 = re.findall(re.escape(',"') + "(.*)" + re.escape(''), name23)[0]
            print("name2:" + name2)

            st3 = itemsJson
            result2 = re.search('item:2"],(.*)"item:3', st3)
            d3 = result2.group(1)
            # print(d3)
            d4 = re.findall(re.escape('p') + "(.*)" + re.escape(':'), d3)[0]
            # print(d4)
            prod3 = re.findall(re.escape('r') + "(.*)" + re.escape('"'), d4)[0]
            print("prod3:" + prod3)
            quant3 = re.findall(re.escape(':[') + "(.*)" + re.escape(',"'), d3)[0]
            print("quant3:" + quant3)
            name32 = re.findall(re.escape('item:2') + "(.*)" + re.escape('item:3'), itemsJson)[0]
            # print(name22)
            name33 = re.findall(re.escape(',"') + "(.*)" + re.escape('",'), name32)[0]
            # print(name23)
            name3 = re.findall(re.escape(',"') + "(.*)" + re.escape(''), name33)[0]
            print("name3:" + name3)

            p2 = int(prod2)
            q2 = int(quant2)

            prr2 = Product.objects.filter(id=p2)
            ps2 = prr2[0].stock
            pchange3 = (int(ps2) - q2)
            Product.objects.filter(id=p2).update(stock=pchange3)

            p3 = int(prod3)
            q3 = int(quant3)

            prr3 = Product.objects.filter(id=p3)
            ps3 = prr3[0].stock
            pchange3 = (int(ps3) - q3)
            Product.objects.filter(id=p3).update(stock=pchange3)

        if count == 4:
            st2 = itemsJson
            result = re.search('item:1"],(.*)"item:2', st2)
            c3 = result.group(1)
            # print(c3)
            c4 = re.findall(re.escape('p') + "(.*)" + re.escape(':'), c3)[0]
            # print(c4)
            prod2 = re.findall(re.escape('r') + "(.*)" + re.escape('"'), c4)[0]
            print("prod2:" + prod2)
            quant2 = re.findall(re.escape(':[') + "(.*)" + re.escape(',"'), c3)[0]
            print("quant2:" + quant2)
            name22 = re.findall(re.escape('item:1') + "(.*)" + re.escape('item:2'), itemsJson)[0]
            # print(name22)
            name23 = re.findall(re.escape(',"') + "(.*)" + re.escape('",'), name22)[0]
            # print(name23)
            name2 = re.findall(re.escape(',"') + "(.*)" + re.escape(''), name23)[0]
            print("name2:" + name2)

            st3 = itemsJson
            result2 = re.search('item:2"],(.*)"item:3', st3)
            d3 = result2.group(1)
            # print(d3)
            d4 = re.findall(re.escape('p') + "(.*)" + re.escape(':'), d3)[0]
            # print(d4)
            prod3 = re.findall(re.escape('r') + "(.*)" + re.escape('"'), d4)[0]
            print("prod3:" + prod3)
            quant3 = re.findall(re.escape(':[') + "(.*)" + re.escape(',"'), d3)[0]
            print("quant3:" + quant3)
            name32 = re.findall(re.escape('item:2') + "(.*)" + re.escape('item:3'), itemsJson)[0]
            # print(name22)
            name33 = re.findall(re.escape(',"') + "(.*)" + re.escape('",'), name32)[0]
            # print(name23)
            name3 = re.findall(re.escape(',"') + "(.*)" + re.escape(''), name33)[0]
            print("name3:" + name3)

            st4 = itemsJson
            result3 = re.search('item:3"],(.*)"item:4', st4)
            e3 = result3.group(1)
            # print(d3)
            e4 = re.findall(re.escape('p') + "(.*)" + re.escape(':'), e3)[0]
            # print(d4)
            prod4 = re.findall(re.escape('r') + "(.*)" + re.escape('"'), e4)[0]
            print("prod4:" + prod4)
            quant4 = re.findall(re.escape(':[') + "(.*)" + re.escape(',"'), e3)[0]
            print("quant4:" + quant4)
            name42 = re.findall(re.escape('item:3') + "(.*)" + re.escape('item:4'), itemsJson)[0]
            # print(name22)
            name43 = re.findall(re.escape(',"') + "(.*)" + re.escape('",'), name42)[0]
            # print(name23)
            name4 = re.findall(re.escape(',"') + "(.*)" + re.escape(''), name43)[0]
            print("name4:" + name4)

            p2 = int(prod2)
            q2 = int(quant2)

            prr2 = Product.objects.filter(id=p2)
            ps2 = prr2[0].stock
            pchange3 = (int(ps2) - q2)
            Product.objects.filter(id=p2).update(stock=pchange3)

            p3 = int(prod3)
            q3 = int(quant3)

            prr3 = Product.objects.filter(id=p3)
            ps3 = prr3[0].stock
            pchange3 = (int(ps3) - q3)
            Product.objects.filter(id=p3).update(stock=pchange3)

            p4 = int(prod4)
            q4 = int(quant4)

            prr4 = Product.objects.filter(id=p4)
            ps4 = prr4[0].stock
            pchange4 = (int(ps4) - q4)
            Product.objects.filter(id=p4).update(stock=pchange4)

        if count == 5:
            st2 = itemsJson
            result = re.search('item:1"],(.*)"item:2', st2)
            c3 = result.group(1)
            # print(c3)
            c4 = re.findall(re.escape('p') + "(.*)" + re.escape(':'), c3)[0]
            # print(c4)
            prod2 = re.findall(re.escape('r') + "(.*)" + re.escape('"'), c4)[0]
            print("prod2:" + prod2)
            quant2 = re.findall(re.escape(':[') + "(.*)" + re.escape(',"'), c3)[0]
            print("quant2:" + quant2)
            name22 = re.findall(re.escape('item:1') + "(.*)" + re.escape('item:2'), itemsJson)[0]
            # print(name22)
            name23 = re.findall(re.escape(',"') + "(.*)" + re.escape('",'), name22)[0]
            # print(name23)
            name2 = re.findall(re.escape(',"') + "(.*)" + re.escape(''), name23)[0]
            print("name2:" + name2)

            st3 = itemsJson
            result2 = re.search('item:2"],(.*)"item:3', st3)
            d3 = result2.group(1)
            # print(d3)
            d4 = re.findall(re.escape('p') + "(.*)" + re.escape(':'), d3)[0]
            # print(d4)
            prod3 = re.findall(re.escape('r') + "(.*)" + re.escape('"'), d4)[0]
            print("prod3:" + prod3)
            quant3 = re.findall(re.escape(':[') + "(.*)" + re.escape(',"'), d3)[0]
            print("quant3:" + quant3)
            name32 = re.findall(re.escape('item:2') + "(.*)" + re.escape('item:3'), itemsJson)[0]
            # print(name22)
            name33 = re.findall(re.escape(',"') + "(.*)" + re.escape('",'), name32)[0]
            # print(name23)
            name3 = re.findall(re.escape(',"') + "(.*)" + re.escape(''), name33)[0]
            print("name3:" + name3)

            st4 = itemsJson
            result3 = re.search('item:3"],(.*)"item:4', st4)
            e3 = result3.group(1)
            # print(d3)
            e4 = re.findall(re.escape('p') + "(.*)" + re.escape(':'), e3)[0]
            # print(d4)
            prod4 = re.findall(re.escape('r') + "(.*)" + re.escape('"'), e4)[0]
            print("prod4:" + prod4)
            quant4 = re.findall(re.escape(':[') + "(.*)" + re.escape(',"'), e3)[0]
            print("quant4:" + quant4)
            name42 = re.findall(re.escape('item:3') + "(.*)" + re.escape('item:4'), itemsJson)[0]
            # print(name22)
            name43 = re.findall(re.escape(',"') + "(.*)" + re.escape('",'), name42)[0]
            # print(name23)
            name4 = re.findall(re.escape(',"') + "(.*)" + re.escape(''), name43)[0]
            print("name4:" + name4)

            st5 = itemsJson
            result4 = re.search('item:4"],(.*)"item:5', st5)
            f3 = result4.group(1)
            # print(d3)
            f4 = re.findall(re.escape('p') + "(.*)" + re.escape(':'), f3)[0]
            # print(d4)
            prod5 = re.findall(re.escape('r') + "(.*)" + re.escape('"'), f4)[0]
            print("prod5:" + prod5)
            quant5 = re.findall(re.escape(':[') + "(.*)" + re.escape(',"'), f3)[0]
            print("quant5:" + quant5)
            name52 = re.findall(re.escape('item:4') + "(.*)" + re.escape('item:5'), itemsJson)[0]
            # print(name22)
            name53 = re.findall(re.escape(',"') + "(.*)" + re.escape('",'), name52)[0]
            # print(name23)
            name5 = re.findall(re.escape(',"') + "(.*)" + re.escape(''), name53)[0]
            print("name5:" + name5)

            p2 = int(prod2)
            q2 = int(quant2)

            prr2 = Product.objects.filter(id=p2)
            ps2 = prr2[0].stock
            pchange3 = (int(ps2) - q2)
            Product.objects.filter(id=p2).update(stock=pchange3)

            p3 = int(prod3)
            q3 = int(quant3)

            prr3 = Product.objects.filter(id=p3)
            ps3 = prr3[0].stock
            pchange3 = (int(ps3) - q3)
            Product.objects.filter(id=p3).update(stock=pchange3)

            p4 = int(prod4)
            q4 = int(quant4)

            prr4 = Product.objects.filter(id=p4)
            ps4 = prr4[0].stock
            pchange4 = (int(ps4) - q4)
            Product.objects.filter(id=p4).update(stock=pchange4)

            p5 = int(prod5)
            q5 = int(quant5)

            prr5 = Product.objects.filter(id=p5)
            ps5 = prr5[0].stock
            pchange5 = (int(ps5) - q5)
            Product.objects.filter(id=p5).update(stock=pchange5)

        if count == 6:
            st2 = itemsJson
            result = re.search('item:1"],(.*)"item:2', st2)
            c3 = result.group(1)
            # print(c3)
            c4 = re.findall(re.escape('p') + "(.*)" + re.escape(':'), c3)[0]
            # print(c4)
            prod2 = re.findall(re.escape('r') + "(.*)" + re.escape('"'), c4)[0]
            print("prod2:" + prod2)
            quant2 = re.findall(re.escape(':[') + "(.*)" + re.escape(',"'), c3)[0]
            print("quant2:" + quant2)
            name22 = re.findall(re.escape('item:1') + "(.*)" + re.escape('item:2'), itemsJson)[0]
            # print(name22)
            name23 = re.findall(re.escape(',"') + "(.*)" + re.escape('",'), name22)[0]
            # print(name23)
            name2 = re.findall(re.escape(',"') + "(.*)" + re.escape(''), name23)[0]
            print("name2:" + name2)

            st3 = itemsJson
            result2 = re.search('item:2"],(.*)"item:3', st3)
            d3 = result2.group(1)
            # print(d3)
            d4 = re.findall(re.escape('p') + "(.*)" + re.escape(':'), d3)[0]
            # print(d4)
            prod3 = re.findall(re.escape('r') + "(.*)" + re.escape('"'), d4)[0]
            print("prod3:" + prod3)
            quant3 = re.findall(re.escape(':[') + "(.*)" + re.escape(',"'), d3)[0]
            print("quant3:" + quant3)
            name32 = re.findall(re.escape('item:2') + "(.*)" + re.escape('item:3'), itemsJson)[0]
            # print(name22)
            name33 = re.findall(re.escape(',"') + "(.*)" + re.escape('",'), name32)[0]
            # print(name23)
            name3 = re.findall(re.escape(',"') + "(.*)" + re.escape(''), name33)[0]
            print("name3:" + name3)

            st4 = itemsJson
            result3 = re.search('item:3"],(.*)"item:4', st4)
            e3 = result3.group(1)
            # print(d3)
            e4 = re.findall(re.escape('p') + "(.*)" + re.escape(':'), e3)[0]
            # print(d4)
            prod4 = re.findall(re.escape('r') + "(.*)" + re.escape('"'), e4)[0]
            print("prod4:" + prod4)
            quant4 = re.findall(re.escape(':[') + "(.*)" + re.escape(',"'), e3)[0]
            print("quant4:" + quant4)
            name42 = re.findall(re.escape('item:3') + "(.*)" + re.escape('item:4'), itemsJson)[0]
            # print(name22)
            name43 = re.findall(re.escape(',"') + "(.*)" + re.escape('",'), name42)[0]
            # print(name23)
            name4 = re.findall(re.escape(',"') + "(.*)" + re.escape(''), name43)[0]
            print("name4:" + name4)

            st5 = itemsJson
            result4 = re.search('item:4"],(.*)"item:5', st5)
            f3 = result4.group(1)
            # print(d3)
            f4 = re.findall(re.escape('p') + "(.*)" + re.escape(':'), f3)[0]
            # print(d4)
            prod5 = re.findall(re.escape('r') + "(.*)" + re.escape('"'), f4)[0]
            print("prod5:" + prod5)
            quant5 = re.findall(re.escape(':[') + "(.*)" + re.escape(',"'), f3)[0]
            print("quant5:" + quant5)
            name52 = re.findall(re.escape('item:4') + "(.*)" + re.escape('item:5'), itemsJson)[0]
            # print(name22)
            name53 = re.findall(re.escape(',"') + "(.*)" + re.escape('",'), name52)[0]
            # print(name23)
            name5 = re.findall(re.escape(',"') + "(.*)" + re.escape(''), name53)[0]
            print("name5:" + name5)

            st6 = itemsJson
            result5 = re.search('item:5"],(.*)"item:6', st6)
            g3 = result5.group(1)
            # print(d3)
            g4 = re.findall(re.escape('p') + "(.*)" + re.escape(':'), g3)[0]
            # print(d4)
            prod6 = re.findall(re.escape('r') + "(.*)" + re.escape('"'), g4)[0]
            print("prod6:" + prod6)
            quant6 = re.findall(re.escape(':[') + "(.*)" + re.escape(',"'), g3)[0]
            print("quant6:" + quant6)
            name62 = re.findall(re.escape('item:5') + "(.*)" + re.escape('item:6'), itemsJson)[0]
            # print(name22)
            name63 = re.findall(re.escape(',"') + "(.*)" + re.escape('",'), name62)[0]
            # print(name23)
            name6 = re.findall(re.escape(',"') + "(.*)" + re.escape(''), name63)[0]
            print("name6:" + name6)

            p2 = int(prod2)
            q2 = int(quant2)

            prr2 = Product.objects.filter(id=p2)
            ps2 = prr2[0].stock
            pchange3 = (int(ps2) - q2)
            Product.objects.filter(id=p2).update(stock=pchange3)

            p3 = int(prod3)
            q3 = int(quant3)

            prr3 = Product.objects.filter(id=p3)
            ps3 = prr3[0].stock
            pchange3 = (int(ps3) - q3)
            Product.objects.filter(id=p3).update(stock=pchange3)

            p4 = int(prod4)
            q4 = int(quant4)

            prr4 = Product.objects.filter(id=p4)
            ps4 = prr4[0].stock
            pchange4 = (int(ps4) - q4)
            Product.objects.filter(id=p4).update(stock=pchange4)

            p5 = int(prod5)
            q5 = int(quant5)

            prr5 = Product.objects.filter(id=p5)
            ps5 = prr5[0].stock
            pchange5 = (int(ps5) - q5)
            Product.objects.filter(id=p5).update(stock=pchange5)

            p6 = int(prod6)
            q6 = int(quant6)

            prr6 = Product.objects.filter(id=p6)
            ps6 = prr6[0].stock
            pchange6 = (int(ps6) - q6)
            Product.objects.filter(id=p6).update(stock=pchange6)

        """
        groups = text.split('_')
        '_'.join(groups[:n]), '_'.join(groups[n:])
        
        string = "20_231_myString_234"
        occur = 2  # on which occourence you want to split
        
        indices = [x.start() for x in re.finditer("_", string)]
        part1 = string[0:indices[occur-1]]
        part2 = string[indices[occur-1]+1:]
        
        print (part1, ' ', part2)
        |||||||||||||||||||||||||||||||||||||||||||||||||||||||
        s = gp
        start = '"'
        end = '"'
        reslt = re.search('%s(.*)%s' % (start, end), s).group(1)
        print(reslt)

        listte=["10","11","12","13","14","15","16","17","18","19","20","21","22"]
        if a2 in listte:
            print(gp[8:9])
        else:
            print(gp[7:8])
        |||||||||||||||||||||||||||||||||||||||||||||||||||||||
        indices = [x.start() for x in re.finditer(",", itemsJson)]
        part1 = itemsJson[0:indices[3 - 1]]
        par2 = itemsJson[indices[3 - 1] + 1:]
        gp = str(part2)
        print(gp)
        a3 = re.findall(re.escape('"') + "(.*)" + re.escape('"'), gp)[0]
        # print(a3)
        a4 = re.findall(re.escape('p') + "(.*)" + re.escape('"'), a3)[0]
        # print(a4)
        prod2 = re.findall(re.escape('r') + "(.*)" + re.escape('"'), a4)[0]
        print("prod2:" + prod2)
        quant2 = re.findall(re.escape('[') + "(.*)" + re.escape(','), a4)[0]
        print("quant2:" + quant2)

        """
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        landmark = request.POST.get('landmark', '')
        phone = request.POST.get('phone', '')
        if count == 1:
            order = Order(itemsJson=itemsJson, name=name, amount=amount, email=email, phone=phone, address=address,
                          city=city,
                          zip_code=zip_code, state=state, landmark=landmark, p_name1=name1, p_id1=prod1,
                          p_quantity1=quant1)
        elif count == 2:
            order = Order(itemsJson=itemsJson, name=name, amount=amount, email=email, phone=phone, address=address,
                          city=city,
                          zip_code=zip_code, state=state, landmark=landmark, p_name1=name1, p_id1=prod1,
                          p_quantity1=quant1, p_name2=name2, p_id2=prod2, p_quantity2=quant2)
        elif count == 3:
            order = Order(itemsJson=itemsJson, name=name, amount=amount, email=email, phone=phone, address=address,
                          city=city,
                          zip_code=zip_code, state=state, landmark=landmark, p_name1=name1, p_id1=prod1,
                          p_quantity1=quant1, p_name2=name2, p_id2=prod2, p_quantity2=quant2, p_name3=name3,
                          p_id3=prod3, p_quantity3=quant3)
        elif count == 4:
            order = Order(itemsJson=itemsJson, name=name, amount=amount, email=email, phone=phone, address=address,
                          city=city,
                          zip_code=zip_code, state=state, landmark=landmark, p_name1=name1, p_id1=prod1,
                          p_quantity1=quant1, p_name2=name2, p_id2=prod2, p_quantity2=quant2, p_name3=name3,
                          p_id3=prod3, p_quantity3=quant3, p_name4=name4, p_id4=prod4, p_quantity4=quant4)
        elif count == 5:
            order = Order(itemsJson=itemsJson, name=name, amount=amount, email=email, phone=phone, address=address,
                          city=city,
                          zip_code=zip_code, state=state, landmark=landmark, p_name1=name1, p_id1=prod1,
                          p_quantity1=quant1, p_name2=name2, p_id2=prod2, p_quantity2=quant2, p_name3=name3,
                          p_id3=prod3, p_quantity3=quant3, p_name4=name4, p_id4=prod4, p_quantity4=quant4,
                          p_name5=name5, p_id5=prod5, p_quantity5=quant5)
        elif count == 6:
            order = Order(itemsJson=itemsJson, name=name, amount=amount, email=email, phone=phone, address=address,
                          city=city,
                          zip_code=zip_code, state=state, landmark=landmark, p_name1=name1, p_id1=prod1,
                          p_quantity1=quant1, p_name2=name2, p_id2=prod2, p_quantity2=quant2, p_name3=name3,
                          p_id3=prod3, p_quantity3=quant3, p_name4=name4, p_id4=prod4, p_quantity4=quant4,
                          p_name5=name5, p_id5=prod5, p_quantity5=quant5, p_name6=name6, p_id6=prod6,
                          p_quantity6=quant6)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id, 'categ': categ})
    return render(request, 'shop/checkout.html', {'categ': categ})
