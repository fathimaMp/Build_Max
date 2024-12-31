from django.db import models

# User_choice=[('admin',"ADMIN"),('customer',"CUSTOMER"),('worker',"WORKER"),('contractor',"CONTRACTOR")]

# Create your models here.
class register(models.Model):
    UserId = models.AutoField(primary_key=True)
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Phone_No = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    Password = models.CharField(max_length=8)
    Profile_pic = models.ImageField(upload_to='profile/', null=True, blank=True)
    # User = models.CharField(max_length=12, choices=User_choice, default='CUSTOMER')
    User_Type = models.IntegerField(default=2)


class contractorregister(models.Model):
    ContractorId = models.AutoField(primary_key=True)
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Phone_No = models.CharField(max_length=50)
    Password = models.CharField(max_length=8)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    Profile_pic = models.ImageField(upload_to='profile1/', null=True, blank=True)
    # User = models.CharField(max_length=12, choices=User_choice, default='CONTRACTOR')
    Rate = models.FloatField(max_length=10)
    Id_Proof = models.ImageField(upload_to='proof/', null=True, blank=True)
    status = models.BooleanField(default=False)
    User_Type = models.IntegerField(default=3)
    Active_status = models.BooleanField(default=True)

    def __str__(self):
        return (self.First_Name)


class workerregister(models.Model):
    workerId = models.AutoField(primary_key=True)
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Phone_No = models.CharField(max_length=50)
    Password = models.CharField(max_length=8)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    Status = models.BooleanField(default=False)
    Profile_pic = models.ImageField(upload_to='profile2/', null=True, blank=True)
    # User = models.CharField(max_length=12, choices=User_choice, default='WORKER')
    Wage = models.FloatField(max_length=10)
    Id_Proof = models.ImageField(upload_to='proof/', null=True, blank=True)
    User_Type = models.IntegerField(default=4)
    Active_status = models.BooleanField(default=True)




class work(models.Model):
    workId = models.AutoField(primary_key=True)
    work_type = models.CharField(max_length=100)
    work = models.CharField(max_length=100)

    def __str__(self):
        return (self.work)


class services(models.Model):
    serviceId = models.AutoField(primary_key=True)
    workerId = models.ForeignKey('workerregister',on_delete=models.CASCADE,to_field='workerId')
    works =models.ForeignKey('work',on_delete=models.CASCADE,to_field='workId')
    Wage = models.FloatField(max_length=10)

class servicescontractor(models.Model):
    serviceId = models.AutoField(primary_key=True)
    ContractorId = models.ForeignKey('contractorregister',on_delete=models.CASCADE,to_field='ContractorId')
    works =models.ForeignKey('work',on_delete=models.CASCADE,to_field='workId')
    Rate = models.FloatField(max_length=10)


# ______________________________________CONTRACTOR PAGE_______________________________________________________________________________________________________


class previous_designs(models.Model):
    designId = models.AutoField(primary_key=True)
    ContractorId = models.ForeignKey('contractorregister',on_delete=models.CASCADE,to_field='ContractorId')
    Caption = models.CharField(max_length=25)
    Image = models.ImageField(upload_to='design/', null=True, blank=True)





#__________________________________________CUSTOMER PAGE__________________________________________________________________________________________________________________________
#CUSTOMER TO WORKER
class worker_req(models.Model):
    ReqId = models.AutoField(primary_key=True)
    workerId = models.ForeignKey('workerregister',on_delete=models.CASCADE,to_field='workerId')
    workId = models.ForeignKey('work', on_delete=models.CASCADE, to_field='workId')
    UserId = models.ForeignKey('register', on_delete=models.CASCADE, to_field='UserId')
    Date = models.DateField(auto_now_add=True)
    Wages = models.CharField(max_length=100)
    Status = models.BooleanField(default=True)
    workstatus = models.BooleanField(default=False)
#CUSTOMER TO CONTRACTOR

class contractor_req(models.Model):
    ReqId = models.AutoField(primary_key=True)
    ContractorId = models.ForeignKey('contractorregister',on_delete=models.CASCADE,to_field='ContractorId')
    workId = models.ForeignKey('work', on_delete=models.CASCADE, to_field='workId')
    UserId = models.ForeignKey('register', on_delete=models.CASCADE, to_field='UserId')
    Date = models.DateField(auto_now_add=True)
    Rate = models.CharField(max_length=100)
    Status = models.BooleanField(default=True)
    servicestatus = models.BooleanField(default=False)

# _____________MAINTENANCE WORK__________________________________________________________________________________________________________________________
#MAINTENANCE WORKER

class worker_maintence(models.Model):
    MaintenanceId = models.AutoField(primary_key=True)
    ReqId = models.ForeignKey('worker_req', on_delete=models.CASCADE, to_field='ReqId')
    worker_maintenance_image = models.ImageField(upload_to='worker_maintenance/', null=True, blank=True)
    Status = models.BooleanField(default=True)


class contractor_maintence(models.Model):
    MaintenanceId = models.AutoField(primary_key=True)
    ReqId = models.ForeignKey('contractor_req', on_delete=models.CASCADE, to_field='ReqId')
    contarctor_maintenance_image = models.ImageField(upload_to='contarctor_maintenance/', null=True, blank=True)
    Status = models.BooleanField(default=True)

