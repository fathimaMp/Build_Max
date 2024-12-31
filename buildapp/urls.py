from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.registerfn, name='register'),
    path('contractorReg/',views.Contregister, name='contractorReg'),
    path('workerReg/',views.Workerregister, name='workerReg'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),


    #USER
    path('user_home/<int:id>', views.user_home, name='user_home'),



    #CONTRACTOR
    path('contractor_home/<int:id>', views.contractor_home,name='contractor_home'),


    #WORKER
    path('worker_home/<int:id>', views.worker_home, name='worker_home'),
# ______________________________________________________________ADMIN PAGE_________________________________________________________________________
    #ADMIN
    path('admin_home/<int:id>', views.admin_home,name='admin_home'),
    path('contractor_request/<int:id>', views.contractor_request, name='contractor_request'),
    path('contractor_list/<int:id>', views.contractor_list, name='contractor_list'),
    path('user_list/<int:id>', views.user_list, name='user_list'),
    path('delete_user/<int:uid>/<int:id>', views.delete_user, name='delete_user'),
    path('worker_request/<int:id>', views.worker_request, name='worker_request'),
    path('approve_contractor/<int:uid>/<int:id>', views.approve_contractor, name='approve_contractor'),
    path('reject_contractor/<int:uid>/<int:id>', views.reject_contractor, name='reject_contractor'),
    path('delete_contractor/<int:uid>/<int:id>', views.delete_contractor, name='delete_contractor'),
    path('delete_worker/<int:uid>/<int:id>', views.delete_worker, name='delete_worker'),
    path('approve_worker/<int:uid>/<int:id>', views.approve_worker, name='approve_worker'),
    path('reject_worker/<int:uid>/<int:id>', views.reject_worker, name='reject_worker'),
    path('worker_list/<int:id>', views.worker_list, name='worker_list'),

#WORK
    path('work/<int:id>', views.work, name='work'),
    path('list_work/<int:id>', views.list_work, name='list_work'),
    path('add_work/<int:uid>', views.add_work, name='add_work'),
    path('edit_work/<int:uid>/<int:id>', views.edit_work, name='edit_work'),
    path('delete_work/<int:uid>/<int:id>', views.delete_work, name='delete_work'),

# ____________________________________________________PROFILE OF ALL USERS_________________________________________________________________________________________________________
    #PROFILE
    path('delete_worker/<int:uid>/<int:id>', views.delete_worker, name='rej_worker'),
    path('admin_profile/<int:uid>',views.admin_profile,name='admin_profile'),
    path('editadmin_profile/<int:uid>',views.editadmin_profile,name='editadmin_profile'),
    path('worker_profile/<int:uid>', views.worker_profile, name='worker_profile'),
    path('editworker_profile/<int:uid>', views.editworker_profile, name='editworker_profile'),
    path('contractor_profile/<int:uid>', views.contractor_profile, name='contractor_profile'),
    path('editcontractor_profile/<int:uid>', views.editcontractor_profile, name='editcontractor_profile'),
    path('user_profile/<int:uid>', views.user_profile, name='user_profile'),
    path('edituser_profile/<int:uid>', views.edituser_profile, name='edituser_profile'),

# ____________________________________WORKER PAGE_________________________________________________________________________________________________________________________________


#SERVICES
    # path('service/<int:id>', views.service, name='service'),
    path('add_service/<int:id>', views.add_service, name='add_service'),
    path('add_contractorservice/<int:id>', views.add_contractorservice, name='add_contractorservice'),

    # ____________________________________CONTRACTOR PAGE_________________________________________________________________________________________________________________________________
#POST
    path('list_designs/<int:id>', views.list_designs, name='list_designs'),
    path('add_designs/<int:uid>', views.add_designs, name='add_designs'),
    path('edit_designs/<int:uid>/<int:id>', views.edit_designs, name='edit_designs'),
    path('delete_designs/<int:uid>/<int:id>', views.delete_designs, name='delete_designs'),
    path('view_designs/<int:uid>', views.view_designs, name='view_designs'),

    # ____________________________________CUSTOMER PAGE_________________________________________________________________________________________________________________________________
#CUSTOMER TO WORKER
    path('worker_list_user/<int:id>', views.worker_list_user, name='worker_list_user'),
    path('req_worker/<int:uid>', views.req_worker, name='req_worker'),
#     jquery
    path('get_workers/', views.get_workers, name='get_workers'),

#CUSTOMER TO CONTRACTOR
    path('contractor_list_user/<int:id>', views.contractor_list_user, name='for contractor_list_user'),
    path('req_contractor/<int:uid>', views.req_contractor, name='req_contractor'),
    # jquery
    path('get_contractors/', views.get_contractors, name='get_contractors'),


# ________________________________ACCEPT OR REJECT USER REQ TO WORKER_________________________________________________________________________________________________________
    path('user_req/<int:id>', views.user_workerrequest, name='user_req'),
    path('delete_user_req/<int:uid>/<int:id>', views.user_workerdelete, name='delete_user_req'),
    path('approve_user_req/<int:uid>/<int:id>', views.user_workerapprove, name='approve_user_req'),
    path('reject_user_req/<int:uid>/<int:id>', views.user_workerreject, name='reject_user_req'),

# ________________________________ACCEPT OR REJECT USER REQ TO WORKER_________________________________________________________________________________________________________
    path('cuser_req/<int:id>', views.user_contractorrequest, name='cuser_req'),
    path('delete_user_creq/<int:uid>/<int:id>', views.user_contractordelete, name='delete_user_creq'),
    path('approve_user_creq/<int:uid>/<int:id>', views.user_contractorapprove, name='approve_user_creq'),
    path('reject_user_creq/<int:uid>/<int:id>', views.user_contractorreject, name='reject_user_creq'),

#________________________________________CURRENT WORK ______________________________________________________________________________________________________________
    path('user_currentwork/<int:id>', views.user_currentwork, name='user_currentwork'),
    path('worker_currentwork/<int:id>', views.worker_currentwork, name='worker_currentwork'),
    path('contractor_currentwork/<int:id>', views.contractor_currentwork, name='contractor_currentwork'),
    path('uc_currentwork/<int:id>', views.uc_currentwork, name='uc_currentwork'),

    #________________________________________MAINTENANCE WORK ______________________________________________________________________________________________________________
# _______________________________________WORKER_______________________________________________________
    path('worker_maintenance/<int:uid>/<int:id>', views.worker_maintenance, name='worker_maintenance'),
    path('finish/<int:uid>/<int:id>', views.finish, name='finish'),
    path('delete_maintenance/<int:uid>/<int:id>', views.delete_maintenance, name='delete_maintenance'),
    path('previous_workmaintenance/<int:uid>/<int:id>', views.previous_workmaintenance, name='previous_workmaintenance'),
    path('previous_work/<int:uid>', views.previous_work, name='previous_work'),
# _______________________________________CONTRACTOR_______________________________________________________
    path('contractor_maintenance/<int:uid>/<int:id>', views.contractor_maintenance, name='contractor_maintenance'),
    path('completed/<int:uid>/<int:id>', views.completed, name='completed'),
    path('deletecontractor_maintenance/<int:uid>/<int:id>', views.deletecontractor_maintenance, name='deletecontractor_maintenance'),
    path('contractorpreviousmaintenance/<int:uid>/<int:id>', views.contractorpreviousmaintenance, name='contractorpreviousmaintenance'),
    path('contractorpreviouswork/<int:uid>', views.contractorpreviouswork, name='contractorpreviouswork'),
    # ____________________________________________USER__________________________________________________
    path('user_maintenance/<int:uid>/<int:id>', views.user_maintenance, name='user_maintenance'),
    path('user_previousmaintenance/<int:uid>/<int:id>', views.user_previousmaintenance, name='user_previousmaintenance'),
    path('user_previouswork/<int:uid>', views.user_previouswork, name='user_previouswork'),
# _________________________usercontrctr maintenance_________________________________________________________________________
    path('uc_maintenance/<int:uid>/<int:id>', views.uc_maintenance, name='uc_maintenance'),
    path('uc_previouswork/<int:uid>', views.uc_previouswork, name='uc_previouswork'),
    path('uc_previousmaintenance/<int:uid>/<int:id>', views.uc_previousmaintenance, name='uc_previousmaintenance'),

# _________________________CALCULATOR_________________________________________________________________________
    path('calculator/<int:uid>', views.calculator, name='calculator'),

]
