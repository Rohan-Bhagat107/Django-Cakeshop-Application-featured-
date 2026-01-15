from django.shortcuts import render,redirect
from django.http import HttpResponse
from AdminApp.models import *
from UserApp.models import *
from django.contrib import messages
from datetime import timedelta,date
from django.utils import timezone
# Create your views here.
#Function for home page
def home(request):
    if request.method=="GET":
        cats=Category.objects.all() # Getting categories
        cakes=Cake.objects.all() #Getting Cake objects
        return render(request,"home.html",{"cats":cats,"cakes":cakes})

#Function for displaying cakes along with thier info like image, name, price etc
def viewCakes(request,cid):
    cats=Category.objects.all()
    cat=Category.objects.get(id=cid)
    cakes=Cake.objects.filter(category=cat)
    return render(request,"home.html",{"cats":cats,"cakes":cakes})
#Function for viewing details of cake and adding it to cart with required quantity
def viewDetails(request,cake_id):
    if request.method=="GET":
        cats=Category.objects.all()
        cake=Cake.objects.get(id=cake_id)
        return render(request, "viewDetails.html",{"cats":cats,"cake":cake})
    else:
        if "uname" in request.session: #Checking user is logged in or not
            cake_id=request.POST["cake_id"]
            qty=request.POST["qty"]
            user=request.session["uname"]
            cake=Cake.objects.get(id=cake_id)
            user=UserInfo.objects.get(username=user)

            try:
                cart=MyCart.objects.get(cake=cake,user=user,qty=qty) #IF exception is thrown means that cake is not present in the cart with same quantity so add that cake in cart
            except:
                cart=MyCart(cake=cake,user=user,qty=qty) #adding new cake in cart
                cart.save()
                return redirect(showCart)
            else:
                messages.warning(request,"Item already present in cart")
                return redirect(showCart) #if cake is already present in cart then returning response
            
        else:
            return redirect(logIn)
#Function for signing Up or Registering to our application
def signUp(request):
    if request.method=="GET":
        cats=Category.objects.all()
        return render(request,"signUp.html",{"cats":cats})
    else:
        uname=request.POST["uname"]
        email=request.POST["email"]
        pwd=request.POST["pwd"]
        try:
            user=UserInfo.objects.get(username=uname)
        except:
            u1=UserInfo(username=uname,email=email,password=pwd)
            u1.save()
            return redirect(home)
        else:
            return HttpResponse("User Already Exists!")
#Once the user is signedup/Registerd the function fro Login
def logIn(request):
    if request.method=="GET":
        cats=Category.objects.all()
        return render(request, "logIn.html",{"cats":cats})
    else:
        uname=request.POST["uname"] #Getting username
        pwd=request.POST["pwd"] #password
        try:
            user=UserInfo.objects.get(username=uname, password=pwd) # Identifying user from its username and password 
        except:
            return redirect(logIn)
        else:
            # if user is valid adding user to session
            request.session["uname"]=uname
            request.session.set_expiry(0)  # expires when browser closes
            return redirect(home)

def logOut(request):
    request.session.flush()
    return redirect(home)
#Function for showing cart to the user
def showCart(request):
    if request.method=="GET":
        if "uname" in request.session:
            cats=Category.objects.all()
            username=UserInfo.objects.get(username=request.session["uname"]) #getting user object
            cart_items=MyCart.objects.filter(user=username)#Getting cart objects associated with logedIn user
            total=0 #Variable for storing price of cart items(total price)
            for one_cake in cart_items: #Iterating over all items one by one and calculating price of cart
                total+=one_cake.cake.price*one_cake.qty
            request.session["cart_price"]=total
            return render(request,"myCart.html",{"cats":cats,"cart_items":cart_items,"total":total})
#If user want to change the quantity of selected item.
def editCartItem(request,item_id):
    if "uname" in request.session:
        if request.method=="GET":
            cats=Category.objects.all()
            item=MyCart.objects.get(id=item_id) #Getting cart object(item) based on item id
            return render(request,"editItem.html",{"cats":cats,"item":item})
        else:
            if "uname" in request.session:
                cart=MyCart.objects.get(id=item_id)
                qty=request.POST["qty"]
                cart.qty=qty #Updating quantity of item/cake
                cart.save()
                return redirect(showCart)
#Function for deleting particular item/cake from cart based on its cart_id
def deleteCartItem(request, item_id):
    MyCart.objects.filter(id=item_id).delete()
    return redirect(showCart)
#Function for removing all items from cart based on username
def clearCart(request):
    if "uname" in request.session:
        if request.method=="GET":
            cats=Category.objects.all()
            user=request.session["uname"]
            MyCart.objects.filter(user=user).delete()
            return redirect(showCart)

#Function for ordering single item based on its cart id
def orderSingleCake(request,cart_id,price):
    if request.method=="GET":
        if "uname" in request.session:
            cats=Category.objects.all()
            cart=MyCart.objects.get(id=cart_id) #Getting particular cake/item from the MyCart table

            if int(price)<500:
                    messages.warning(request, "Minimum order value is ₹500. Please increase quantity.")
                    return redirect(home)
            else:
                try:
                    #Fetching user's card details from previous oroder 
                    card=CardDetails.objects.filter(user=request.session["uname"]) #If details not found exception is thrown
                except:
                    messages.warning(request, "Card details not found! Please fill the form manually")
                    return render(request, "makePayment.html",{"cart":cart,"amt":price,"cats":cats})
                else: #Otherwise we fetch the card details and autofill the payment details. 
                    card=CardDetails.objects.filter(user=request.session["uname"]).last()
                    messages.info(request,"Previous payment details restored!")
                    return render(request, "makePayment.html",{"cart":cart,"amt":price,"cats":cats,"card":card})
        else:
            return redirect(logIn)
    else:
        #getting user card details
        card_no=request.POST["card_no"]
        holders_name=request.POST["holders_name"]
        expiry=request.POST["expiry"]
        cvv=request.POST["cvv"]
        amt=request.POST["amt"]
        fields_required=[card_no,holders_name,expiry,cvv]
        if not all(fields_required):
            messages.warning("Required fields are missing!")
            return redirect(MyCart)
        else:
            if "uname" in request.session:
                user=UserInfo.objects.get(username=request.session["uname"]) # Getting user object
            card_details=CardDetails.objects.create(
                user=user,
                card_no=card_no,
                cvv=cvv,
                expiry_date=expiry
                )
            card_details.save()
# -------------------------------------------------------
            cart = MyCart.objects.get(id=cart_id) #Getting cart object based on cart id
            #Creating new object of OrderHistory table to add the order details into DB
            
            order=OrderHistory.objects.create(
                user=user,
                cake_name=cart.cake.cake_name,
                cake_price=cart.cake.price,
                quantity=cart.qty,
                amount=cart.cake.price * cart.qty,
                card_no=card_no,
                delivery_date=timezone.now().date() + timedelta(days=5)
                )
            cart.delete()   #Removing orderd cake from MyCart
            order.save() #Saving the order info into DB
        # ------------------------------------------
            messages.warning(request, "🎉Order Placed Successfully!")
            return redirect(showCart)
            

#Function for ordering all items present in cart in one stroke based on username
def orderWholeCart(request,price):
    if request.method=="GET":
        if "uname" in request.session:
            cats=Category.objects.all()
            user=request.session["uname"]
            cart=MyCart.objects.filter(user=user)
            if int(price)<500:
                    messages.warning(request, "Minimum order value is ₹500. Please add more items.")
                    return redirect(home)
            else:
                try:
                    card=CardDetails.objects.filter(user=request.session["uname"])
                except:
                    messages.warning(request, "Card details not found! Please fill the form manually")
                    return render(request, "makePayment.html",{"cart":cart,"amt":price,"cats":cats})
                else:
                    if int(price)<500:
                        messages.warning(request, "Minimum order value is ₹500. Please add more items.")
                        return redirect(home)
                    else:
                        card=CardDetails.objects.filter(user=request.session["uname"]).first()
                        messages.info(request, "Previous payment details restored!")
                        return render(request, "makePayment.html",{"cart":cart,"amt":price,"cats":cats,"card":card})
    else:
        #Getting cart details 
        if "uname" in request.session:
            card_no=request.POST["card_no"]
            holders_name=request.POST["holders_name"]
            expiry=request.POST["expiry"]
            cvv=request.POST["cvv"]
            amt=request.POST["amt"]
            user=UserInfo.objects.get(username=request.session["uname"])
            cart_items=MyCart.objects.filter(user=user) #Filtering MyCart objects based on username
            # order=OrderHistory(user=user,order_item=cart,amount=amt,card_no=card_no)
            # order.save()
            fields_required=[card_no,holders_name,expiry,cvv]
            if not all(fields_required):
                messages.warning(request, "Required fields are missing!")
                return redirect(MyCart)
            else:
                card_details=CardDetails.objects.create(
                    user=user,
                    card_no=card_no,
                    cvv=cvv,
                    expiry_date=expiry
                    )
                card_details.save()
                for item in cart_items: #Iterating over all items in cart and creating its object for adding them into OrderHistory table.
                    order=OrderHistory.objects.create(
                        user=user,
                        cake_name=item.cake.cake_name,
                        cake_price=item.cake.price,
                        quantity=item.qty,
                        amount=item.cake.price * item.qty,
                        card_no=card_no,
                        delivery_date=date.today() + timedelta(days=5)
                    )
                
                cart_items.delete() #Deleting all items from cart
                messages.info(request, "🎉Order Placed Successfully!")
                return redirect(home)


#Function for getting order history based on username
def getOrderHistory(request):
    if request.method=="GET":
        if "uname" in request.session:
            user=UserInfo.objects.get(username=request.session["uname"])
            orders=OrderHistory.objects.filter(user=user)
            return render(request,"viewOrderHistory.html",{"orders":orders})

#function for resetting the password
def resetPassword(request):
    if request.method=="GET":
        return render(request,"resetPassword.html",{})
    else:
        uname=request.POST["username"]
        email=request.POST["email"]
        pwd=request.POST["pwd"]
        try:
            user=UserInfo.objects.get(username=uname,email=email)
        except:
            return redirect(signUp)
        else:
            user.password=pwd
            user.save()
            return redirect(logIn)
#Function for clearing the order history
def clearHistory(request):
    if request.method=="GET":
        if "uname" in request.session:
            OrderHistory.objects.filter(user=request.session["uname"]).delete()
            return redirect(getOrderHistory)
# Function for filyering the cakes based on price
def get_FilterCakesByPrice(request):
    price=request.GET.get("price_range")
    if price !="above 1000":
        price=price.split("-")
        # print(starting_price,ending_price)
        filtered_cakes=Cake.objects.filter(price__gte=int(price[0]),price__lte=int(price[1]))
        return render(request, "home.html",{"cakes":filtered_cakes})
    else:
        filterd_cakes=Cake.objects.filter(price_gte=1000)
        return render(request, "home.html",{"cakes":filterd_cakes})

