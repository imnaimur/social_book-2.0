from django.shortcuts import render,redirect
from . models import CustomUser,Post
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model,authenticate
from django.contrib import messages



User = get_user_model
# Create your views here.
@login_required(login_url='signin')
def index(request):

    user_object = CustomUser.objects.get(email = request.user.email)
    img = user_object.profileimg
    posts = Post.objects.all()
    return render(request,'index.html',{'posts':posts,'img':img})



@login_required(login_url='signin')
def settings(request):
    user_obj = CustomUser.objects.get(email = request.user.email)

    if request.method == 'POST':
        image = request.FILES.get('image')
        if request.FILES.get('image') == None:
            image = user_obj.profileimg
        fname = request.POST['fname']
        lname = request.POST['lname']
        bio = request.POST['bio']
        location = request.POST['location']
        occupation = request.POST['occupation']
        # relationship = request.POST['relationship']
        # relationship = request.POST.get('relationship',False)

        user_obj.profileimg = image
        user_obj.first_name = fname
        user_obj.last_name = lname
        user_obj.bio = bio
        user_obj.location = location
        user_obj.occupation = occupation
        # user_obj.relationship = relationship
        user_obj.save()
        
        # return render(request,'setting.html',{"user_obj":user_obj})
        return redirect('settings')

    

    return render(request,'setting.html',{"user_obj":user_obj})

def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        user_name = request.POST['user_name']
        password1 = request.POST['password']
        password2 = request.POST['password2']
        checkbox = request.POST.get('checkbox', False)

        info={
                    "email":email,
                    "user_name":user_name,
                    "password1":password1,
                    "password2":password2
                }

        if (len(password2) or len(password1))<6:
                messages.info(request,"Password requirment doesn't match")
                
                return render(request,'signup.html',info)
    
        if password1 == password2:
            if not checkbox:
                messages.info(request,'Please mark the checkbox')
                return render(request,'signup.html',info)
            if CustomUser.objects.filter(email = email).exists():
                messages.info(request,'User email already exists')
                return redirect('signup')
            # elif User.objects.filter(name == name).exists():
            #     messages.info(request,'User name already exists')
            #     return redirect('signup')
            
            else:
                user = CustomUser.objects.create(email = email,user_name=user_name,password = password1)
                user.set_password(password1)
                user.save()
                return redirect('settings')
                
        
            
        else:
            messages.info(request,'Password do not match')
            return render(request,'signup.html',info)
        
        

    else:
        return render(request,'signup.html')


def signin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        # user = authenticate(request,email=email,password=password)



        if "@" in email:
            # email = request.POST['email']
            user = authenticate(request,email=email,password=password)
        else:
            if CustomUser.objects.filter(user_name = email).exists():

                user_obj = CustomUser.objects.filter(user_name = email)
                for user in user_obj:
                    access = user.email

                user = authenticate(request,email = access,password=password)
                print(user)
            else:
                user = None
            





        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.info(request, 'Credential Invalid')
            return redirect('signin')
    else:
        return render(request,'signin.html')

@login_required(login_url='signin')
def upload(request):
    email = CustomUser.objects.get(email = request.user.email)
    caption = request.POST['caption']
    img = request.FILES.get('uploaded_img')
    new_post = Post.objects.create(email = email,postImage = img ,caption = caption)
    new_post.save()
    return redirect('/')


def logout(request):
    request.session.flush()
    return render(request,'signin.html')