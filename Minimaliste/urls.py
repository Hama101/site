from django.urls import path
from . import views as v
from django.contrib.auth import views as auth_views

urlpatterns = [
    #Home Page
    path('',v.home , name="home"),

	#blog
	path('blog/',v.blog,name="blog"),
	path('blog/<str:pk>/',v.viewBlogPage,name="blogPost"),
	path('blog/<str:name>/',v.blogTag,name="blogtag"),

	#shop
	path('shop/',v.shop , name="shop"),
	path('filterByCat/<str:cat>',v.filterbycat , name="filterbycat"),

	#contact
	path('contact/',v.contact,name="contact"),

    #users
    path('login/',v.loginPage , name="login"),
    path('signup/',v.signupPage , name="sign-up"),
    path('logout/',v.logoutUser, name="logout"),
	path('updateToPro/',v.updateToPro , name="updateToPro" ) ,
	path('Profile/<str:pk>/',v.myProfile , name="Profile"),
	path('updateProfile/<str:pk>/',v.updateProfile,name="updateProfile"),
	path('makeProfile/<str:pk>/',v.makeProfile , name="makeProfile"),
	path('myPosts/',v.myposts , name="myPosts"),

    #useresLogic --> resting passwords
	path('rest_password/' ,
						auth_views.PasswordResetView.as_view(template_name="accounts/reset_password.html")
						, name="reset_password"),
	path('rest_password_sent/' ,
    					auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html") ,
        				name="password_reset_done"),
	path('rest/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html")
	, name="password_reset_confirm"),
	path('rest_password_complete/',auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_done.html")
					,name="password_reset_complete"),

	#add Posts
	path('addpost/',v.addPost , name="addPost"),
	path('viewpost/<str:pk>/',v.viewPost , name="viewpost"),
	path('deletepost/<str:pk>/',v.deletePost , name="deletePost"),
	path('submitTopost/<str:pk>/', v.submitToPost , name="submitToPost"),
	path('deleteCom/<str:pk>/',v.deleteCom , name="deleteCom"),
	path('updatePost/<str:pk>/',v.updatePost , name="updatePost"),

	#payment
	path('payment/',v.payment,name="payment"),
	path('testPayment/' , v.testPayment , name="testPayment"),
	path('charge/',v.charge,name="charge"),
	path('success/<str:args>/',v.successMsg , name="success")

]

