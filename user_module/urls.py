from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
	path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True),name="login"),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
	path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
	path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
	path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
	# View url patters
	path('staff/create/',createstaffview,name='create_staff'),
	path('staffs/all/',allstaffview,name='view_all_staff'),
	path('staff/details/<int:id>/',staffdetailview,name='staff_detail'),

	path('my_account/', MyAccountView.as_view(), name="my_account"),
	path('my_account/edit/<int:id>', AccountEditView.as_view(), name="account_edit"),

]