from django import forms
from . models import register,contractorregister,workerregister,work,services,previous_designs,worker_req,contractor_req,servicescontractor,worker_maintence,contractor_maintence


class RegisterForm(forms.ModelForm):
    Password = forms.CharField(widget=forms.PasswordInput, max_length=12, min_length=5)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    class Meta():

        model = register
        fields = ('First_Name','Last_Name','Email','Password','Phone_No','address','Profile_pic',)


class ContractorregisterForm(forms.ModelForm):
    Password = forms.CharField(widget=forms.PasswordInput, max_length=12, min_length=5)

    class Meta():
        model = contractorregister
        fields = ('First_Name', 'Last_Name', 'Email', 'Password', 'Phone_No', 'Profile_pic', 'Rate','Id_Proof','state','district','city',)


class WorkerregisterForm(forms.ModelForm):
    Password = forms.CharField(widget=forms.PasswordInput, max_length=12, min_length=5)

    class Meta():
        model = workerregister
        fields = ('First_Name', 'Last_Name', 'Email', 'Password', 'Phone_No', 'Profile_pic', 'Wage', 'Id_Proof','state','district','city',)


class LoginForm(forms.ModelForm):
    Password = forms.CharField(widget=forms.PasswordInput, max_length=12, min_length=5)

    class Meta():
        model = register
        fields = ('Email', 'Password',)

# ___________________________________________________________________________________________________________________________________________________________
#PROFILE
class EditadminForm(forms.ModelForm):
    class Meta():
        model = register
        fields = ('First_Name','Last_Name','Password','Phone_No','address','Profile_pic',)


class EditworkerForm(forms.ModelForm):
    class Meta():
        model = workerregister
        fields = ('First_Name', 'Last_Name', 'Email', 'Password', 'Phone_No', 'Profile_pic', 'Wage', 'Id_Proof','state','district','city',)

class EditcontractorForm(forms.ModelForm):
    class Meta():
        model = contractorregister
        fields = ('First_Name', 'Last_Name', 'Email', 'Password', 'Phone_No', 'Profile_pic', 'Rate','Id_Proof','state','district','city',)


class EdituserForm(forms.ModelForm):
    class Meta():
        model = register
        fields = ('First_Name','Last_Name','Email','Password','Phone_No','address','Profile_pic',)



#SERVICES OF WORKER and CONTRACTORS
class addWorkForm(forms.ModelForm):
    CHOICES = [
        ('Small_scale', 'Small_scale'),
        ('Large_scale', 'Large_scale'),
    ]
    work_type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    class Meta():
        model = work
        fields = '__all__'



class editWorkForm(forms.ModelForm):
    CHOICES = [
        ('Small scale', 'Small scale'),
        ('Large scale', 'Large scale'),
    ]
    work_type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    class Meta():
        model = work
        fields = '__all__'

#SERVICE OF CONTRACTOR
class addServicecontractorForm(forms.ModelForm):
    class Meta():
        model = servicescontractor
        fields = ['works','Rate',]

#SERVICE OF WORKER
class addServiceForm(forms.ModelForm):

    class Meta():
        model = services
        fields = ['works','Wage',]
        # widgets = {
        #     'works': forms.CheckboxSelectMultiple,
        # }


# class editWorkForm(forms.ModelForm):
#     CHOICES = [
#         ('Small scale', 'Small scale'),
#         ('Large scale', 'Large scale'),
#     ]
#     work_type = forms.MultipleChoiceField(
#         choices=CHOICES,
#         widget=forms.CheckboxSelectMultiple,
#     )
#
#     class Meta():
#         model = work
#         fields = '__all__'




 # ___________________CONTRACTOR PAGE______________________________________________________________________________________________________________________________________________________



class adddesignForm(forms.ModelForm):
    class Meta():
        model = previous_designs
        fields = '__all__'



class editdesignForm(forms.ModelForm):
    # work_type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    class Meta():
        model = previous_designs
        fields = '__all__'



 # ___________________CUSTOMER PAGE______________________________________________________________________________________________________________________________________________________
#CUSTOMER TO WORKER


class reqWorkerForm(forms.ModelForm):
    # work_type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    class Meta():
        model = worker_req
        fields = ('workId',)


#CUSTOMER TO CONTRACTOR

class reqContractorForm(forms.ModelForm):
    # work_type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    workId = forms.ModelChoiceField(
        queryset=work.objects.filter(work_type="Large scale"),
        label='Select a Service',
        empty_label='Select a Service'
    )
    class Meta():
        model = contractor_req
        fields = ('workId',)



#MAINTENENCE WORKER

class addMaintenanceForm(forms.ModelForm):
    worker_maintenance_image = forms.FileField(required=True)
    class Meta():
        model = worker_maintence
        fields = ('worker_maintenance_image',)

class editMaintenanceForm(forms.ModelForm):
    # work_type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    class Meta():
        model = worker_maintence
        fields = '__all__'

class addcontractorMaintenanceForm(forms.ModelForm):
    contarctor_maintenance_image = forms.FileField(required=True)
    class Meta():
        model = contractor_maintence
        fields = ('contarctor_maintenance_image',)

class editcontractorMaintenanceForm(forms.ModelForm):
    # work_type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    class Meta():
        model = contractor_maintence
        fields = '__all__'


