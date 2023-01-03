from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login as loginuser,logout as logoutuser
from task.forms import TodoForm
from task.models import Todo
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login')
def home(request):
    if request.user.is_authenticated:
        user=request.user
        form=TodoForm()
        todos=Todo.objects.filter(user=user).order_by("priority")

        context={'form':form,'todos':todos}

        return render(request,'index.html',context)


@login_required(login_url='/login')
def add_todo(request):
    if request.user.is_authenticated:
        user=request.user
        form=TodoForm(request.POST)
        if form.is_valid():
            todo=form.save(commit=False)
            todo.user=user
            todo.save()
            return redirect('/')

        else:
            return render(request,'index.html',{"form":form})

def delete_todo(request,id):
    Todo.objects.get(pk=id).delete()
    return redirect('/')

def change_status(request, id, status):
    todo=Todo.objects.get(pk=id)
    todo.status=status
    todo.save()
    return redirect('/')

def signup(request):
    if request.method=="GET":
        f = UserCreationForm()
        content = {'form':f}
        return render(request,'signup.html',content)

    else:
        f=UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect('/login')
        else:
            f = UserCreationForm(request.POST)
            content = {'form':f}
            return render(request,'signup.html',content)

def login(request):
    if request.method=='GET':

        f = AuthenticationForm()
        content = {'form':f}
        return render(request,'login.html',content)

    else:
        f=AuthenticationForm(data=request.POST)
        if f.is_valid():
            username=f.cleaned_data.get('username')
            password=f.cleaned_data.get('password')
            user=authenticate(username=username, password=password)
            if user is not None:
                loginuser(request,user)
                return redirect('/')
            
            else:
                return redirect('/login')
       
        else:
            f = AuthenticationForm(data=request.POST)
            content = {'form':f}
            return render(request,'login.html',content)
            # return redirect('/login')


def logout(request):
    logoutuser(request)
    return redirect('/login')