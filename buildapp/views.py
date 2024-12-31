from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as logouts
from .forms import RegisterForm, ContractorregisterForm, WorkerregisterForm, LoginForm, EditadminForm, EditworkerForm,  \
    EditcontractorForm, addWorkForm, editWorkForm, addServiceForm, adddesignForm, editdesignForm, reqWorkerForm, \
    addServicecontractorForm, reqContractorForm,addMaintenanceForm,editMaintenanceForm,editcontractorMaintenanceForm,addcontractorMaintenanceForm
from django.db.models import Q

from . models import register,contractorregister,workerregister,work,services,previous_designs,worker_req,contractor_req,servicescontractor,worker_maintence,contractor_maintence
from django.contrib import messages
from django.conf import settings
# from django.core.mail import send_mail
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.models import User
from django.core.mail import send_mail


# Create your views here.
def registerfn(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            Email=form.cleaned_data['Email']
            if User.objects.filter(email=Email).exists():
                messages.warning(request,"user already exists")
                return redirect('/register/')
            else:
                form.save()
                useremail = register.objects.get(Email=Email)
                User.objects.create_user(username=useremail, email=Email)
                messages.warning(request, "Registered Successfully")
                return redirect('/register/')
    else:
        form = RegisterForm()
        return render(request, 'main/register.html', {'form1':form})


def Contregister(request):
    if request.method == 'POST':
        form = ContractorregisterForm(request.POST, request.FILES)
        if form.is_valid():
            Email=form.cleaned_data['Email']
            if User.objects.filter(email=Email).exists():
                messages.warning(request,"user already exists")
                return redirect('/contractorReg/')
            else:
                form.save()
                useremail = contractorregister.objects.get(Email=Email)
                User.objects.create_user(username=useremail, email=Email)
                messages.warning(request, "Registered Successfully")
                return redirect('/contractorReg/')
    else:
        form = ContractorregisterForm()
        return render(request, 'main/contractorReg.html', {'form':form} )


def Workerregister(request):
    if request.method == 'POST':
        form = WorkerregisterForm(request.POST, request.FILES)
        if form.is_valid():
            Email = form.cleaned_data['Email']
            if User.objects.filter(email=Email).exists():
                messages.warning(request, "user already exists")
                return redirect('/workerReg/')
            else:
                form.save()
                useremail = workerregister.objects.get(Email=Email)
                User.objects.create_user(username=useremail, email=Email)
                messages.warning(request, "Registered Successfully")
                return redirect('/workerReg/')
    else:
        form = WorkerregisterForm()
        return render(request, 'main/workerReg.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            Email = form.cleaned_data['Email']
            Password = form.cleaned_data['Password']
            try:
                user = register.objects.get(Email=Email)
                if user:
                    try:
                        user1 = register.objects.get(Q(UserId=user.UserId)& Q(Password=Password))
                        if user1:
                            if user.User_Type==2:
                                request.session['session_id'] = user.UserId
                                return redirect('/user_home/%s' % user.UserId)
                            else:
                                request.session['session_id'] = user.UserId
                                return redirect('/admin_home/%s' % user.UserId)
                        else:
                            return redirect('/login/')
                    except register.DoesNotExist:
                        user1 = None
                        messages.warning(request, "Incorrect Password")
                        return redirect('/login/')
            except register.DoesNotExist:
                try:
                    user = contractorregister.objects.get(Email=Email)
                    if user:
                        try:
                            user1 = contractorregister.objects.get(Q(ContractorId=user.ContractorId)& Q(Password=Password))
                            if user1:
                                if user.status == True:
                                    request.session['session_id'] = user.ContractorId
                                    return redirect('/contractor_home/%s' % user.ContractorId)
                                else:
                                    return redirect('/login/')
                        except workerregister.DoesNotExist:
                            user1 = None
                            messages.warning(request, "Incorrect Password")
                            return redirect('/login/')
                except contractorregister.DoesNotExist:
                    try:
                        user = workerregister.objects.get(Email=Email)
                        if user:
                            try:
                                user1 = workerregister.objects.get(Q(workerId=user.workerId)& Q(Password=Password))
                                if user1:
                                    if user.Status == True:
                                        request.session['session_id'] = user.workerId
                                        return redirect('/worker_home/%s' % user.workerId)
                                    else:
                                        return redirect('/login/')
                            except workerregister.DoesNotExist:
                                user1 = None
                                messages.warning(request, "Incorrect Password")
                                return redirect('/login/')
                    except workerregister.DoesNotExist:
                        user1 = None
                        messages.warning(request, "Incorrect Password")
                        return redirect('/login/')

    else:
        form = LoginForm()
        return render(request, "main/login.html", {'form': form})

def logout(request):
    del request.session['session_id']
    logouts(request)
    return redirect('/')





def about(request):
    return render(request,'about.html')


def index(request):
    return render(request,'main/index.html')


def contact(request):
    return render(request,'contact.html')




# USER
def user_home(request,id):
    if request.session.get('session_id'):
        return render(request,'user/user_home.html',{'UserId':id})
    else:
        return redirect('/login/')




#CONTRACTOR

def contractor_home(request,id):
    if request.session.get('session_id'):
        return render(request,'contractor/contractor_home.html',{'ContractorId':id})
    else:
        return redirect('/login/')




#WORKER
def worker_home(request,id):
    if request.session.get('session_id'):
        return render(request,'worker/worker_home.html',{'workerId':id})
    else:
        return redirect('/login/')




#ADMIN
# ____________________________________________________________________ADMIN_______________________________________________________________________________________________________
#CONTRACTOR

def contractor_request(request,id):
    if request.session.get('session_id'):
        contractor = contractorregister.objects.filter(status=False)
        page_num = request.GET.get('page',1)
        paginator = Paginator(contractor,5)
        try:
            page_obj=paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request,'admin/contractor_request.html',{'page_obj':page_obj,'UserId':id})
    else:
        return redirect('/login/')

def contractor_list(request,id):
    if request.session.get('session_id'):
        contractor = contractorregister.objects.filter(status=True)
        page_num = request.GET.get('page',1)
        paginator = Paginator(contractor,5)
        try:
            page_obj=paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request,'admin/contractor_list.html',{'page_obj':page_obj,'UserId':id})
    else:
        return redirect('/login/')


def approve_contractor(request, uid, id):
    if request.session.get('session_id'):
        contractorregister.objects.filter(ContractorId=id).update(status=True)
        return redirect('/contractor_request/%s' % uid)
    else:
        return redirect('/login/')


def reject_contractor(request, uid, id):
    if request.session.get('session_id'):
        contractor = contractorregister.objects.get(ContractorId=id)
        user = User.objects.get(email=contractor.Email)
        user.delete()
        contractorregister.objects.filter(ContractorId=id).delete()
        return redirect('/contractor_request/%s' % uid)
    else:
        return redirect('/login/')

def delete_contractor(request, uid, id):
    if request.session.get('session_id'):
        contractor = contractorregister.objects.get(ContractorId=id)
        user = User.objects.get(email=contractor.Email)
        user.delete()
        contractorregister.objects.filter(ContractorId=id).delete()
        return redirect('/contractor_list/%s' % uid)
    else:
        return redirect('/login/')


# _________________________________________________________________________________________________________________________________________________________________________________
#USER
def user_list(request,id):
    if request.session.get('session_id'):
        user = register.objects.filter(User_Type=2)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(user, 5)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'admin/user_list.html', {'page_obj': page_obj, 'UserId': id})
    else:
        return redirect('/login/')

def delete_user(request, uid, id):
    if request.session.get('session_id'):
        user = register.objects.get(UserId=id)
        user = register.objects.get(email=user.Email)
        user.delete()
        register.objects.filter(UserId=id).delete()
        return redirect('/user_list/%s' % uid)
    else:
        return redirect('/login/')


# ______________________________________________________________________________________________________________________________________________________________________________
 #WORKER
def worker_request(request,id):
    if request.session.get('session_id'):
        worker = workerregister.objects.filter(Status=False)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(worker, 5)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'admin/worker_request.html', {'page_obj': page_obj, 'UserId': id})
    else:
        return redirect('/login/')


def worker_list(request,id):
    if request.session.get('session_id'):
        worker = workerregister.objects.filter(Status=True)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(worker, 5)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'admin/worker_list.html', {'page_obj': page_obj, 'UserId': id})
    else:
        return redirect('/login/')




def approve_worker(request,uid, id):
    if request.session.get('session_id'):
        workerregister.objects.filter(workerId=id).update(Status=True)
        return redirect('/worker_request/%s' % uid)
    else:
        return redirect('/login/')


def reject_worker(request,uid, id):
    if request.session.get('session_id'):
        worker = workerregister.objects.get(workerId=id)
        user = User.objects.get(email=worker.Email)
        user.delete()
        workerregister.objects.filter(workerId=id).delete()
        return redirect('/worker_request/%s' % uid)
    else:
        return redirect('/login/')


def delete_worker(request, uid, id):
    if request.session.get('session_id'):
        worker=workerregister.objects.get(workerId=id)
        user = User.objects.get(email=worker.Email)
        user.delete()
        workerregister.objects.filter(workerId=id).delete()
        return redirect('/worker_list/%s' % uid)
    else:
        return redirect('/login/')

# ------------------------------------------------------------------------------------------------------------------------------------------------------
#WORK


def add_work(request, uid):
    if request.session.get('session_id'):
        if request.method == 'POST':
            form = addWorkForm(request.POST)
            if form.is_valid():
                form.save()
                messages.warning(request, "work Added Successfully")
                return redirect('/add_work/%s' % uid)
        else:
            form_value = addWorkForm()
            return render(request, "admin/add_work.html", {'form_key': form_value, 'UserId': uid})
    else:
        return redirect('/login/')


def list_work(request,id):
    if request.session.get('session_id'):
        works = work.objects.all()
        page_num = request.GET.get('page', 1)
        paginator = Paginator(works, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "admin/list_work.html",{ 'page_obj': page_obj,'UserId':id})
    else:
        return redirect('/login/')



def delete_work(request, uid, id):
    if request.session.get('session_id'):
        work.objects.get(workId=id).delete()
        return redirect('/list_work/%s' % uid)
    else:
        return redirect('/login/')



def edit_work(request, uid, id):
    if request.session.get('session_id'):
        works = work.objects.get(workId=id)
        if request.method == 'POST':
            form = editWorkForm(request.POST, instance=works)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/list_work/%s' % uid)
        else:
            form_value = editWorkForm(instance=works)
            return render(request, "admin/edit_work.html", {'form_key': form_value, 'UserId': uid})
    else:
        return redirect('/login/')






# __________________________________________________________________________________________________________________________________________________________________________
#ADMIN

def admin_home(request,id):
    if request.session.get('session_id'):
        return render(request,'admin/admin_home.html',{'UserId':id})
    else:
        return redirect('/login/')
# __________________________________________________________________________________ADMIN PAGE_______________________________________________________________________
# __________________________________________________________________________________PROFILE____________________________________________________________________________________________
#PROFILE

def admin_profile(request, uid):
    if request.session.get('session_id'):
        admin = register.objects.get(UserId=uid)
        return render(request, "admin/admin_profile.html", {'admin': admin, 'UserId': uid})
    else:
        return redirect('/login/')


def editadmin_profile(request, uid):
    if request.session.get('session_id'):
        admin =register.objects.get(UserId=uid)
        if request.method == 'POST':
            form = EditadminForm(request.POST, instance=admin)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/admin_profile/%s' % uid)

        else:
            form_value = EditadminForm(instance=admin)
            return render(request, "admin/editadmin_profile.html",
                          {'form_key': form_value, 'admin': admin, 'UserId': uid})
    else:
        return redirect('/login/')


def worker_profile(request, uid):
    if request.session.get('session_id'):
        worker = workerregister.objects.get(workerId=uid)
        return render(request, "worker/worker_profile.html", {'worker': worker, 'workerId': uid})
    else:
        return redirect('/login/')


def editworker_profile(request, uid):
    if request.session.get('session_id'):
        worker =workerregister.objects.get(workerId=uid)
        if request.method == 'POST':
            form = EditworkerForm(request.POST, instance=worker)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/worker_profile/%s' % uid)

        else:
            form_value = EditworkerForm(instance=worker)
            return render(request, "worker/editworker_profile.html",
                          {'form_key': form_value, 'worker': worker, 'workerId': uid})
    else:
        return redirect('/login/')


def contractor_profile(request, uid):
    if request.session.get('session_id'):
        contractor = contractorregister.objects.get(ContractorId=uid)
        return render(request, "contractor/contractor_profile.html", {'contractor': contractor, 'ContractorId': uid})
    else:
        return redirect('/login/')


def editcontractor_profile(request, uid):
    if request.session.get('session_id'):
        contractor =contractorregister.objects.get(ContractorId=uid)
        if request.method == 'POST':
            form = EditcontractorForm(request.POST, instance=contractor)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/contractor_profile/%s' % uid)

        else:
            form_value = EditcontractorForm(instance=contractor)
            return render(request, "contractor/editcontractor_profile.html",
                          {'form_key': form_value, 'contractor':contractor , 'ContractorId': uid})
    else:
        return redirect('/login/')


def user_profile(request, uid):
    if request.session.get('session_id'):
        user = register.objects.get(UserId=uid)
        return render(request, "user/user_profile.html", {'users': user, 'UserId': uid})
    else:
        return redirect('/login/')

def edituser_profile(request, uid):
    if request.session.get('session_id'):
        user =register.objects.get(UserId=uid)
        if request.method == 'POST':
            form = EditadminForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/user_profile/%s' % uid)

        else:
            form_value = EditadminForm(instance=user)
            return render(request, "user/edituser_profile.html",
                          {'form_key': form_value, 'user': user, 'UserId': uid})
    else:
        return redirect('/login/')

# ________________________________________________________________________WORKER page______________________________________________________________________________________________
#SERVICES
# WORKER SERVICE

def add_service(request,id):
    if request.session.get('session_id'):
        if request.method == 'POST':
            user = workerregister.objects.get(workerId=id)
            form = addServiceForm(request.POST)
            if form.is_valid():
                works=form.cleaned_data['works']
                Wage=form.cleaned_data['Wage']
                services.objects.create(workerId=user,works=works,Wage=Wage)
                messages.warning(request, "Service Added Successfully")
                return redirect('/add_service/%s' % id)
            else:
                print(form.errors)
                return redirect('/add_service/%s' % id)
        else:
            form_value = addServiceForm()
            return render(request, "worker/add_service.html", {'form_key': form_value, 'workerId': id})
    else:
        return redirect('/login/')



# CONTRACTOR SERVICE

def add_contractorservice(request,id):
    if request.session.get('session_id'):
        user=contractorregister.objects.get(ContractorId=id)
        if request.method == 'POST':
            form = addServicecontractorForm(request.POST)
            if form.is_valid():
                works=form.cleaned_data['works']
                Rate=form.cleaned_data['Rate']
                servicescontractor.objects.create(ContractorId=user,works=works,Rate=Rate)
                messages.warning(request, "Service Added Successfully")
                return redirect('/add_contractorservice/%s' % id)


            else:
                print(form.errors)
                return redirect('/add_contractorservice/%s' % id)
        else:
            form_value = addServicecontractorForm()
            return render(request, "contractor/add_contractorservice.html", {'form_key': form_value, 'ContractorId': id})
    else:
        return redirect('/login/')







#_________________________CONTRACTOR PAGE____________________________________________________________________________________________________________________________________________________



def add_designs(request, uid):
    if request.session.get('session_id'):
        if request.method == 'POST':
            form = adddesignForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                messages.warning(request, "work Added Successfully")
                return redirect('/add_designs/%s' % uid)
        else:
            form_value = adddesignForm()
            return render(request, "contractor/add_designs.html", {'form_key': form_value, 'ContractorId': uid})
    else:
        return redirect('/login/')


def list_designs(request,id):
    if request.session.get('session_id'):
        designs = previous_designs.objects.all()
        page_num = request.GET.get('page', 1)
        paginator = Paginator(designs, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "contractor/list_designs.html",{ 'page_obj': page_obj,'ContractorId':id})
    else:
        return redirect('/login/')



def delete_designs(request, uid, id):
    if request.session.get('session_id'):
        previous_designs.objects.get(designId=id).delete()
        return redirect('/list_designs/%s' % uid)
    else:
        return redirect('/login/')



def edit_designs(request, uid, id):
    if request.session.get('session_id'):
        designs = previous_designs.objects.get(designId=id)
        if request.method == 'POST':
            form = editdesignForm(request.POST,request.FILES, instance=designs)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/list_designs/%s' % uid)
        else:
            form_value = editdesignForm(instance=designs)
            return render(request, "contractor/edit_designs.html", {'form_key': form_value, 'ContractorId': uid})
    else:
        return redirect('/login/')


def view_designs(request, uid):
        if request.session.get('session_id'):
            print("---------------------------------------------------------------------------------------", id)
            req = previous_designs.objects.all()

            return render(request, "user/view_design.html", {'page_obj': req, 'UserId': uid})
        else:
            return redirect('/login/')


# _______________________________________USERS PAGE______________________________________________________________________________________________________________________________
#REQUESTS

#CUSTOMER TO WORKER
def worker_list_user(request,id):
    if request.session.get('session_id'):
        worker = workerregister.objects.filter(Status=True)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(worker, 5)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'user/worker_list.html', {'page_obj': page_obj, 'UserId': id})
    else:
        return redirect('/login/')


def req_worker(request,uid):
    if request.session.get('session_id'):
        user = register.objects.get(UserId=uid)
        if request.method == 'POST':
            workerid = request.POST.get('worker')
            wages= request.POST.get('wages')
            form = reqWorkerForm(request.POST, request.FILES)
            if form.is_valid():
                works=form.cleaned_data['workId']
                WorkerId = workerregister.objects.get(workerId=workerid)
                worker_req.objects.create(Wages=wages,workerId=WorkerId, workId=works, UserId=user)
                return redirect('/req_worker/%s' % uid)
        else:
            form = reqWorkerForm()
        return render(request, 'user/worker_req.html', {'UserId': uid,'form': form })
    else:
        return redirect('/login/')

def get_workers(request):
    if request.session.get('session_id'):
        work = request.GET.get('work')
        data1 = services.objects.filter(works=work).values('Wage','workerId__workerId','workerId__First_Name','workerId__Last_Name')
        return JsonResponse(list(data1), safe=False)
    else:
        return redirect('/login/')



#CUSTOMER TO CONTRACTOR

def contractor_list_user(request,id):
    if request.session.get('session_id'):
        contractor = contractorregister.objects.filter(Status=True)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(contractor, 5)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'user/contractor_list.html', {'page_obj': page_obj, 'UserId': id})
    else:
        return redirect('/login/')



def req_contractor(request,uid):
    if request.session.get('session_id'):
        user = register.objects.get(UserId=uid)
        if request.method == 'POST':
            contractorId = request.POST.get('contractor')
            form = reqContractorForm(request.POST, request.FILES)
            if form.is_valid():
                works=form.cleaned_data['workId']
                Rate=request.POST.get('Rate')
                ContractorId = contractorregister.objects.get(ContractorId=contractorId)
                contractor_req.objects.create(ContractorId=ContractorId, workId=works, UserId=user,Rate=Rate)
                return redirect('/req_contractor/%s' % uid)
        else:
            form = reqContractorForm()
            return render(request, 'user/contractor_req.html', {'UserId': uid,'form': form })
    else:
        return redirect('/login/')



def get_contractors(request):
    if request.session.get('session_id'):
        work = request.GET.get('work')
        data1 = servicescontractor.objects.filter(Q(works=work)).values('Rate','ContractorId__ContractorId','ContractorId__First_Name','ContractorId__Last_Name')
        print(data1)
        return JsonResponse(list(data1), safe=False)
    else:
        return redirect('/login/')


#ACCEPT OR REJECT USER REQ TO WORKER



def user_workerrequest(request,id):
    if request.session.get('session_id'):
        req = worker_req.objects.filter(Q(workerId=id) & Q(Status=True) & Q(workstatus=False))
        page_num = request.GET.get('page', 1)
        paginator = Paginator(req, 5)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'worker/user_req.html', {'page_obj': page_obj, 'workerId': id})
    else:
        return redirect('/login/')


def user_workerlist(request,id):
    if request.session.get('session_id'):
        req = worker_req.objects.filter(Status=True)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(req, 5)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'user/worker_req.html', {'page_obj': page_obj, 'UserId': id})
    else:
        return redirect('/login/')




def user_workerapprove(request,uid, id):
    if request.session.get('session_id'):
        worker_req.objects.filter(ReqId=id).update(workstatus=True)
        req = worker_req.objects.get(ReqId=id)
        name = req.UserId.First_Name
        print(name)
        subject = 'Confirmation'
        message = f'Hi {name}, Your request has been approved.Our officials will contact you soon'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [req.UserId.Email,]
        print(recipient_list)
        send_mail(subject, message, email_from, recipient_list)
        return redirect('/user_req/%s' % uid)
    else:
        return redirect('/login/')

def user_workerreject(request,uid, id):
    if request.session.get('session_id'):
        req = worker_req.objects.get(ReqId=id)
        worker_req.objects.filter(ReqId=id).delete()
        return redirect('/worker_req/%s' % uid)
    else:
        return redirect('/login/')

def user_workerdelete(request, uid, id):
    if request.session.get('session_id'):
        req = worker_req.objects.get(ReqId=id)
        worker_req.objects.filter(ReqId=id).delete()
        return redirect('/worker_req/%s' % uid)
    else:
        return redirect('/login/')


#ACCEPT OR REJECT USER REQ TO CONTRACTOR

def user_contractorrequest(request,id):
    if request.session.get('session_id'):
        req = contractor_req.objects.filter(Q(ContractorId=id) & Q(Status=True) & Q(servicestatus=False))
        page_num = request.GET.get('page', 1)
        paginator = Paginator(req, 5)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'contractor/cuser_req.html', {'page_obj': page_obj, 'ContractorId': id})
    else:
        return redirect('/login/')



#
# def user_contractorlist(request,id):
#     if request.session.get('session_id'):
#         req = contractor_req.objects.filter(Status=True)
#         page_num = request.GET.get('page', 1)
#         paginator = Paginator(req, 5)
#         try:
#             page_obj = paginator.page(page_num)
#         except PageNotAnInteger:
#             page_obj = paginator.page(1)
#         except EmptyPage:
#             page_obj = paginator.page(paginator.num_pages)
#         return render(request, 'user/contractor_req.html', {'page_obj': page_obj, 'UserId': id})
#     else:
#         return redirect('/login/')




def user_contractorapprove(request,uid, id):
    if request.session.get('session_id'):
        contractor_req.objects.filter(ReqId=id).update(servicestatus=True,)
        req = contractor_req.objects.get(ReqId=id)
        name = req.UserId.First_Name
        print(name)
        subject = 'Confirmation'
        message = f'Hi {name}, Your request has been approved.Our officials will contact you soon'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [req.UserId.Email,]
        send_mail(subject, message, email_from, recipient_list)
        return redirect('/cuser_req/%s' % uid)
    else:
        return redirect('/login/')

def user_contractorreject(request,uid, id):
    if request.session.get('session_id'):
        req = contractor_req.objects.get(ReqId=id)
        user = User.objects.get(email=req.Email)
        user.delete()
        contractor_req.objects.filter(ReqId=id).delete()
        return redirect('/contractor_req/%s' % uid)
    else:
        return redirect('/login/')

def user_contractordelete(request, uid, id):
    if request.session.get('session_id'):
        req = contractor_req.objects.get(ReqId=id)
        user = User.objects.get(email=req.Email)
        user.delete()
        contractor_req.objects.filter(ReqId=id).delete()
        return redirect('/contractor_req/%s' % uid)
    else:
        return redirect('/login/')

# ___________________________CURRENTWORKS____________________________________________________________________________________________________________
def worker_currentwork(request,id):
    if request.session.get('session_id'):
        req = worker_req.objects.filter(Q(workerId=id) & Q(Status=True) & Q(workstatus=True))
        page_num = request.GET.get('page', 1)
        paginator = Paginator(req, 5)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'worker/worker_currentwork.html', {'page_obj': page_obj, 'workerId': id})
    else:
        return redirect('/login/')

def user_currentwork(request,id):
    if request.session.get('session_id'):
        req = worker_req.objects.filter(Q(UserId=id) & Q(workstatus=True) & Q(Status=True))
        page_num = request.GET.get('page', 1)
        paginator = Paginator(req, 5)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'user/user_currentwork.html', {'page_obj': page_obj, 'UserId': id})
    else:
        return redirect('/login/')

def uc_currentwork(request,id):
    if request.session.get('session_id'):
        req = contractor_req.objects.filter(Q(UserId=id) & Q(servicestatus=True)&Q(Status=True))
        page_num = request.GET.get('page', 1)
        paginator = Paginator(req, 5)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'user/uc_currentwork.html', {'page_obj': page_obj, 'UserId': id})
    else:
        return redirect('/login/')

def contractor_currentwork(request,id):
    if request.session.get('session_id'):
        req = contractor_req.objects.filter(Q(ContractorId=id) & Q(Status=True) & Q(servicestatus=True))
        page_num = request.GET.get('page', 1)
        paginator = Paginator(req, 5)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'contractor/contractor_currentwork.html', {'page_obj': page_obj, 'ContractorId': id})
    else:
        return redirect('/login/')
# ____________________MAINTENANCE WORK________________________________________________________________________________________________________________________________
# _____________________contractor_________________________________________________________________________________________________
def contractor_maintenance(request,uid,id):
    if request.session.get('session_id'):
        print("----------------------------------------------------------------------------",id)
        if request.method == 'POST':
            form = addcontractorMaintenanceForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.files['contarctor_maintenance_image']
                req_id = contractor_req.objects.get(ReqId=id)
                print(req_id)
                contractor_maintence.objects.create(ReqId = req_id,contarctor_maintenance_image = image)
                messages.warning(request, "Image Added Successfully")
                return redirect('/contractor_maintenance/%s/%s' % (uid,id))
        else:
            form_value = addcontractorMaintenanceForm()
            req = contractor_maintence.objects.filter(ReqId=id)
            page_num = request.GET.get('page', 1)
            paginator = Paginator(req, 5)  # 6 employees per page
            try:
                page_obj = paginator.page(page_num)
            except PageNotAnInteger:
                # if page is not an integer, deliver the first page
                page_obj = paginator.page(1)
            except EmptyPage:
                # if the page is out of range, deliver the last page
                page_obj = paginator.page(paginator.num_pages)
            return render(request, "contractor/contractor_maintenance.html", {'page_obj': page_obj,'form_key': form_value, 'ContractorId': uid})
    else:
        return redirect('/login/')

def listcontractor_maintetanace(request,uid,id):
    if request.session.get('session_id'):
        req = contractor_maintence.objects.filter(ReqId=id)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(req, 8)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "contractor/listcontractor_maintenance.html",{ 'page_obj': page_obj,'ContractorId':uid})
    else:
        return redirect('/login/')



def deletecontractor_maintenance(request, uid, id):
    if request.session.get('session_id'):
        req=contractor_maintence.objects.get(MaintenanceId=id)
        contractor_maintence.objects.get(MaintenanceId=id).delete()
        return redirect('/contractor_maintenance/%s/%s' % (uid,req.ReqId.ReqId))
    else:
        return redirect('/login/')

def contractorpreviousmaintenance(request, uid,id):
    if request.session.get('session_id'):
        req = contractor_maintence.objects.filter(ReqId=id)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(req, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
        # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
         # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "contractor/contractorpreviousmaintenance.html", {'page_obj': page_obj, 'ContractorId': uid})
    else:
            return redirect('/login/')


def contractorpreviouswork(request, uid):
    if request.session.get('session_id'):
        req = contractor_req.objects.filter(Q(ContractorId=uid) & Q(Status=False) & Q(servicestatus=False))
        page_num = request.GET.get('page', 1)
        paginator = Paginator(req, 5)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'contractor/contractorpreviouswork.html', {'page_obj': page_obj, 'ContractorId': uid})
    else:
        return redirect('/login/')

# ______________________worker_________________________________________________________________________________________
def worker_maintenance(request,uid,id):
    if request.session.get('session_id'):
        print("----------------------------------------------------------------------------",id)
        if request.method == 'POST':
            form = addMaintenanceForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.files['worker_maintenance_image']
                req_id = worker_req.objects.get(ReqId=id)
                print(req_id)
                worker_maintence.objects.create(ReqId = req_id,worker_maintenance_image = image)
                messages.warning(request, "Image Added Successfully")
                return redirect('/worker_maintenance/%s/%s' % (uid,id))
        else:
            form_value = addMaintenanceForm()
            req = worker_maintence.objects.filter(ReqId=id)
            page_num = request.GET.get('page', 1)
            paginator = Paginator(req, 5)  # 6 employees per page
            try:
                page_obj = paginator.page(page_num)
            except PageNotAnInteger:
                # if page is not an integer, deliver the first page
                page_obj = paginator.page(1)
            except EmptyPage:
                # if the page is out of range, deliver the last page
                page_obj = paginator.page(paginator.num_pages)
            return render(request, "worker/worker_maintenance.html", {'page_obj': page_obj,'form_key': form_value, 'workerId': uid})
    else:
        return redirect('/login/')

#



def delete_maintenance(request, uid, id):
    if request.session.get('session_id'):
        req=worker_maintence.objects.get(MaintenanceId=id)
        worker_maintence.objects.get(MaintenanceId=id).delete()
        return redirect('/worker_maintenance/%s/%s' % (uid,req.ReqId.ReqId))
    else:
        return redirect('/login/')

def previous_workmaintenance(request, uid,id):
    if request.session.get('session_id'):
        req = worker_maintence.objects.filter(ReqId=id)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(req, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
        # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
         # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "worker/previouswork_maintenance.html", {'page_obj': page_obj, 'workerId': uid})
    else:
            return redirect('/login/')

def previous_work(request, uid):
    if request.session.get('session_id'):
        req = worker_req.objects.filter(Q(workerId=uid) & Q(Status=False) &  Q(workstatus=False))
        page_num = request.GET.get('page', 1)
        paginator = Paginator(req, 5)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'worker/previous_work.html', {'page_obj': page_obj, 'workerId': uid})
    else:
        return redirect('/login/')

def user_maintenance(request,uid,id):
    if request.session.get('session_id'):
        print("---------------------------------------------------------------------------------------",id)
        req = worker_maintence.objects.filter(ReqId=id)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(req, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "user/user_maintenance.html",{'page_obj': page_obj,'UserId': uid})
    else:
        return redirect('/login/')

def user_previouswork(request,uid):
    if request.session.get('session_id'):
        req = worker_req.objects.filter(Q(UserId=uid) & Q(Status=False) & Q(workstatus=False))
        page_num = request.GET.get('page', 1)
        paginator = Paginator(req, 5)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'user/user_previouswork.html', {'page_obj': page_obj, 'UserId': uid})
    else:
        return redirect('/login/')

def user_previousmaintenance(request, uid, id):
        if request.session.get('session_id'):
            print("---------------------------------------------------------------------------------------", id)
            req = worker_maintence.objects.filter(ReqId=id)
            page_num = request.GET.get('page', 1)
            paginator = Paginator(req, 5)  # 6 employees per page
            try:
                page_obj = paginator.page(page_num)
            except PageNotAnInteger:
                # if page is not an integer, deliver the first page
                page_obj = paginator.page(1)
            except EmptyPage:
                # if the page is out of range, deliver the last page
                page_obj = paginator.page(paginator.num_pages)
            return render(request, "user/user_previousmaintenance.html", {'page_obj': page_obj, 'UserId': uid})
        else:
            return redirect('/login/')
# ________________________________usercontractor_________________________________________________________________________
def uc_maintenance(request,uid,id):
    if request.session.get('session_id'):
        print("---------------------------------------------------------------------------------------",id)
        req = contractor_maintence.objects.filter(ReqId=id)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(req, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "user/uc_maintenance.html",{'page_obj': page_obj,'UserId': uid})
    else:
        return redirect('/login/')

def uc_previouswork(request,uid):
    if request.session.get('session_id'):
        req = contractor_req.objects.filter(Q(UserId=uid) & Q(Status=False))
        page_num = request.GET.get('page', 1)
        paginator = Paginator(req, 5)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'user/uc_previouswork.html', {'page_obj': page_obj, 'UserId': uid})
    else:
        return redirect('/login/')

def uc_previousmaintenance(request, uid, id):
        if request.session.get('session_id'):
            print("---------------------------------------------------------------------------------------", id)
            req = contractor_maintence.objects.filter(ReqId=id)
            page_num = request.GET.get('page', 1)
            paginator = Paginator(req, 5)  # 6 employees per page
            try:
                page_obj = paginator.page(page_num)
            except PageNotAnInteger:
                # if page is not an integer, deliver the first page
                page_obj = paginator.page(1)
            except EmptyPage:
                # if the page is out of range, deliver the last page
                page_obj = paginator.page(paginator.num_pages)
            return render(request, "user/uc_previousmaintenance.html", {'page_obj': page_obj, 'UserId': uid})
        else:
            return redirect('/login/')


# def delete_maintenance(request, uid, id):
#     if request.session.get('session_id'):
#         worker_maintenance.objects.get(MaintenanceId=id).delete()
#         return redirect('/list_maintenance/%s' % uid)
#     else:
#         return redirect('/login/')

# _______________________STATUS______________________________________________________________________________________________________________________________
def finish(request,uid,id):
    if request.session.get('session_id'):
        worker_req.objects.filter(ReqId=id).update(Status=False,workstatus=False)
        return redirect('/worker_currentwork/%s' % uid )
    else:
        return redirect('/login/')

def completed(request,uid,id):
    if request.session.get('session_id'):
        contractor_req.objects.filter(ReqId=id).update(Status=False,servicestatus=False)
        return redirect('/contractor_currentwork/%s' % uid )
    else:
        return redirect('/login/')
# ___________________________CALCULATOR_______________________________________________________________________________________
def calculator(request, uid):
    if request.session.get('session_id'):
        return render(request, "user/calculator.html", { 'UserId': uid})
    else:
        return redirect('/login/')
    #


