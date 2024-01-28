from sqlite3 import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from houserent.models import FlatsAvailable,Flat,Booking
from .forms import UserRegistrationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.db.models import Sum

from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.http import HttpResponse





# Create your views here.
def index (request):
    first = FlatsAvailable.objects.latest('id')
    latests = FlatsAvailable.objects.all().exclude(id=first.id)
    ads = FlatsAvailable.objects.all()

    # Order the queryset by the 'title' field
    flats = FlatsAvailable.objects.all().order_by('title')

    p = Paginator(flats, 4)
    page = request.GET.get('page')
    flats = p.get_page(page)

    return render(request, 'index.html', {"ads": ads, 'latest': latests, 'first': first, 'flats': flats})
def register(request):
    if request.method == 'POST':
         form = UserRegistrationForm(request.POST)
         if form.is_valid():
             form.save()
             user = form.cleaned_data.get('username')
             messages.success(request, 'Account was created for ' + user)
             return redirect('login')
    else:
        form=UserRegistrationForm()

    context = {'form':form}
    
    return render(request, 'register.html',context)
    
def user_login(request):
    
    if request.method == "POST":
        username = request.POST['Username']
        password = request.POST['Password']
        user_data = authenticate(username=username, password=password)
        if user_data is  None:
            messages.error(request,'Incorrect Username or Password');
        if user_data is not None:
           

            login(request, user_data)
            uname=user_data.get_username
            messages.success(request,'Logged in Sucessfully');
            return redirect('index')
            

    if request.user.is_authenticated==True:
        return redirect('index')
        
    else:
        return render(request, 'login.html')  


@login_required
def logout_user(request):
    if User.is_authenticated:
        logout(request)
        messages.error(request,'Logged out Sucessfully')
        return redirect('index')        

@login_required
def postad(request):
    if request.method=="POST":
        title=request.POST['ad_title']
        description= request.POST['description']
        price=request.POST['rent']
        location=request.POST['location']
        bedroom=request.POST['bedroom']
        livingroom=request.POST['living_room']
        bathroom=request.POST['bathroom']
        kitchen=request.POST['kitchen']
        contact_number=request.POST['contact_number']
        images=request.FILES['flat_image']
        post=FlatsAvailable(uid=request.user,title=title,description=description,price=price,location=location,bedroom=bedroom,livingroom=livingroom,bathroom=bathroom,kitchen=kitchen,contact_number=contact_number,images=images)
        post.save()
        return redirect('index')
    else:
         return render(request, 'postad.html',{})
    

def adDetail(request,slugs,id):
    data=FlatsAvailable.objects.get(slugs=slugs)

    others=FlatsAvailable.objects.exclude(id=id)

    if request.method=="POST":
        flat_id=request.POST['flat-id']
        user_id=request.user
        print(flat_id)
        flat_instance=FlatsAvailable.objects.get(id=flat_id)
        try:
            res=Booking(user=user_id,flat=flat_instance)
            res.save()
        except Exception as e:
            return render(request,'adviews.html',{'d':data,'o':others,'message':"Already Booked"}) 
        return redirect('index')
    

    return render(request,'adviews.html',{'d':data,'o':others})

# Search Flat

def binary_search_flats(all_flats, search_keyword):
    found_flats = []

    # Sorting the flats by title for binary search
    sorted_flats = sorted(all_flats, key=lambda x: x.title.lower())

    left, right = 0, len(sorted_flats) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_flat = sorted_flats[mid]

        if search_keyword.lower() in mid_flat.title.lower():
            found_flats.append(mid_flat)
            # Check for other matches to the left
            for i in range(mid - 1, left - 1, -1):
                if search_keyword.lower() in sorted_flats[i].title.lower():
                    found_flats.insert(0, sorted_flats[i])
                else:
                    break
            # Check for other matches to the right
            for i in range(mid + 1, right + 1):
                if search_keyword.lower() in sorted_flats[i].title.lower():
                    found_flats.append(sorted_flats[i])
                else:
                    break
            return found_flats
        elif search_keyword.lower() < mid_flat.title.lower():
            right = mid - 1
        else:
            left = mid + 1

    return found_flats


def search_flat(request):
    if request.method == "POST":
        search_keyword = request.POST.get('search')
        all_flats = FlatsAvailable.objects.all()

        # Perform binary search
        found_flats = binary_search_flats(all_flats, search_keyword)

        context = {'search': search_keyword, 'flats': found_flats}
        return render(request, 'search_flat.html', context)
    else:
        return render(request, 'search_flat.html', {})

        
# profile page
@login_required
def profile(request):
    post_history=FlatsAvailable.objects.filter(uid=request.user)
    Bookings=Booking.objects.filter(user=request.user)
    # pagination
    paginator_d=Paginator(post_history,10)
    pg_num_d=request.GET.get('page')
    pg_obj_d=paginator_d.get_page(pg_num_d)

    res_msg=""
    if request.method == 'POST':
     
        
            try:
                booking_id = request.POST['book-id']
                res = Booking.objects.get(id=booking_id)
                res.delete()
                res_msg="booking success"
                return redirect(request.path)
            except Exception as e:
                flat_id=request.POST['flat-id']
                res=FlatsAvailable.objects.get(id=flat_id)
                res.delete()
                res_msg="flat post deleted"
                return redirect(request.path)


    return render(request,'profile.html',{'rd':pg_obj_d,'bookings':Bookings,"msg":res_msg})


def flat_detail(request, flat_id):
    flat = Flat.objects.get(pk=flat_id)
    user = request.user
    # booking_status = Booking.objects.filter(user=user, flat=flat).exists()

    context = {
        'flat': flat,
        # 'booking_status': booking_status,
    }

    return render(request, 'flat_detail.html', context)

def book_flat(request, flat_id):
    flat = Flat.objects.get(pk=flat_id)
    user = request.user

    
    if Booking.objects.filter(user=user, flat=flat).exists():
        message = "This flat is already booked."
    else:
        # Attempt to create a new booking
        booking = Booking.objects.create(user=user, flat=flat)
        message = f"Booking successful: {booking}"

    return redirect('flat_detail', flat_id=flat_id, message=message)

#filter

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0].price
        less = [flat for flat in arr[1:] if flat.price <= pivot]
        greater = [flat for flat in arr[1:] if flat.price > pivot]
        return quicksort(less) + [arr[0]] + quicksort(greater)

def filter_flats(request):
    flats = None

    if request.method == 'POST':
        price_min = request.POST.get('priceMin')
        price_max = request.POST.get('priceMax')

      
        if price_min is not None and price_max is not None:
            all_flats = FlatsAvailable.objects.filter(price__gte=price_min, price__lte=price_max)

            
            all_flats = quicksort(list(all_flats))

          
            paginator = Paginator(all_flats, 4)
            page = request.GET.get('page', 1)  \

            try:
                flats = paginator.page(page)
            except PageNotAnInteger:
                flats = paginator.page(1)
            except EmptyPage:
                flats = paginator.page(paginator.num_pages)

    else:
        # Handle other cases or return all flats if no filter values are provided
        all_flats = FlatsAvailable.objects.all()

        # Use QuickSort for sorting
        all_flats = quicksort(list(all_flats))

        # Paginate the results
        paginator = Paginator(all_flats, 4)
        page = request.GET.get('page', 1)  # Set a default page number of 1

        try:
            flats = paginator.page(page)
        except PageNotAnInteger:
            flats = paginator.page(1)
        except EmptyPage:
            flats = paginator.page(paginator.num_pages)

    context = {'flats': flats}
    return render(request, 'filter_flat.html', context)

