from django.shortcuts import render, redirect
from django.shortcuts import  get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
import re
from .models import Event, places, venue
from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils import timezone


def signup(request):
    if request.method=='POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        pass2 = request.POST.get('pass2')
        enteropt = request.POST.get('otp')
        opt = 'sit'
        
        if enteropt != opt:
            messages.warning(request, 'keyword is wrong')
            return redirect('signup.html')
        
        if password != pass2:
            messages.warning(request, 'Email already exists.')
            return redirect('signup.html')
            
        try:
            if User.objects.get(username=email):
                messages.info(request, 'Email already exists.')
                return redirect('signup.html') 
        except User.DoesNotExist:
            pass
        
        myuser = User.objects.create_user(username=email, password=password)  
        myuser.save()
        messages.success(request, 'Account created successfully.')
        return redirect('login')  
    return render(request, 'signup.html')

@login_required
def update(request, myuser_id):
    try:
        events = Event.objects.filter(myuser=myuser_id)
        return render(request, 'option.html', {'events': events})
    except Event.DoesNotExist:
        return redirect('book', myuser_id=myuser_id)
    
def login(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        myuser = authenticate(username=email, password=password)
        
        if myuser is not None:
            auth_login(request, myuser)
            return redirect('update', myuser_id=myuser.id) 
        else:
            messages.warning(request, 'invalid')
            return render(request, 'login.html')
    return render(request, 'login.html')


def handlelogout(request):
    logout(request)
    return redirect('index')


def index(request):
    places_queryset = places.objects.all().order_by('id')
    return render(request, 'index.html', {'place': places_queryset})

def contact(request):
    if request.method == 'POST':
        fname = request.POST.get('name')
        feedback = request.POST.get('feedback')
        from_email = request.POST.get('email', None)
        if from_email is not None and re.match(r'^[\w\.-]+@[\w\.-]+$', from_email):
                email = EmailMessage(
                subject=f'User {fname} sent a feedback ',
                body=f'{feedback}',
                from_email=settings.EMAIL_HOST_USER,
                to=['snapship43@gmail.com'],
                cc=[],
               )
                email.send()
                return render(request, 'index.html')
        else:
                return HttpResponse('Invalid email address.')
    
    else:
        return render(request, 'contact.html') 

def gallery(request, place_id):
    place = get_object_or_404(places, pk=place_id)  # Retrieve the Place object
    return render(request, 'gallery-single.html', {'place': place})

def display(request, event_id):
    event= get_object_or_404(Event, pk=event_id)  # Retrieve the Place object
    return render(request, 'gallery.html', {'event': event})

@login_required
def book(request, myuser_id):
    if request.method == 'POST': 
        place_id = request.POST.get('place')
        event = request.POST.get('event')
        from_email = request.POST.get('email')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        duration = int(request.POST.get('duration'))  
        img = request.FILES.get('photo')
        dis = request.POST.get('message')
        
        myuser = User.objects.get(username=from_email)
        place = venue.objects.get(id=place_id)
        
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        time = datetime.strptime(time_str, '%H:%M').time()
        
        start_datetime = timezone.make_aware(datetime.combine(date, time))
        end_datetime = start_datetime + timedelta(hours=duration)
        
        if start_datetime <= timezone.now():
            messages.info(request, "Invalid Date and Time")
            all_places = venue.objects.all().order_by('id')
            myuser= User.objects.get(pk=myuser_id)
            return render(request, 'book.html', {'place': all_places,'myuser_id':myuser})

        overlapping_bookings = Event.objects.filter(place=place, date=date, start_time__lt=end_datetime, end_time__gt=start_datetime)
        if overlapping_bookings.exists():
            email = EmailMessage(
                subject=f'Slot already booked for this time',
                body=f'We are sorry,it seems that the {date} and {start_datetime} you have entered for your event are already booked. Please select a different time or date, or contact us for further assistance. Thank you for your understanding. ',
                from_email=settings.EMAIL_HOST_USER,
                to=[from_email],
                cc=[],
            )
            email.send()
            all_places = venue.objects.all().order_by('id')
            
            myuser= User.objects.get(pk=myuser_id)
            messages.info(request, "Slot already booked for this time")
            return render(request, 'book.html', {'place': all_places,'myuser_id':myuser})

        if re.match(r'^[\w\.-]+@[\w\.-]+$', from_email):
            event = Event.objects.create( myuser= myuser, email=from_email, event=event, date=date,location=place.name, start_time=start_datetime, end_time=end_datetime, image=img, discription=dis, place=place)
            email = EmailMessage(
                subject=f'Event has been booked by email {from_email}',
                body=f'This is to inform you that an event has been booked by email {from_email} on the following {date} and {start_datetime}. ',
                from_email=settings.EMAIL_HOST_USER,
                to=['snapship43@gmail.com'],
                cc=[],
            )
            if img:
                email.attach(img.name, img.read(), img.content_type)
            email.send()
            touseremail = EmailMessage(
                subject=f'Your booking is confirmed',
                body=f'Your booking is confirmed, and we look forward to welcoming you at the event. If you have any questions or need further assistance, feel free to reach out to us. Thank you for choosing us, and we hope you have a fantastic experience!',
                from_email=settings.EMAIL_HOST_USER,
                to=[from_email],
                cc=[],
            )
            touseremail.send()
            HttpResponse('Your booking is confirmed')
            return redirect('/event')
        else:
            messages.warning(request, "Invalid email address")
            all_places = venue.objects.all().order_by('id')
            return render(request, 'book.html', {'place': all_places})
    else:
        all_places = venue.objects.all().order_by('id') 
        myuser= User.objects.get(pk=myuser_id)
        return render(request, 'book.html', {'place': all_places,'myuser_id':myuser})

def event(request):
    events = Event.objects.all().order_by('start_time')
    
    current_time = timezone.now()
    
    future_events = []
    
    for event in events:
        if event.start_time >= current_time:
            future_events.append(event)
  
    for event in events:
        if event not in future_events:
            event.delete()
            
    return render(request, 'event.html', {'events': future_events})

@login_required
def deleteit(request,event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.delete()
    return redirect('update', myuser_id=event.myuser_id)

@login_required
def do_update(request, event_id):
    if request.method == 'POST':
        event = request.POST.get('event') 
        img = request.FILES.get('photo')
        dis = request.POST.get('message')
        update = Event.objects.get(pk=event_id)
        update.event = event
        update.discription = dis
        if img is not None:
            update.image = img
        update.save() 
        return redirect('update', myuser_id=update.myuser_id)

    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'do_update.html', {'event': event})

