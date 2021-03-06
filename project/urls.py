"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from products_app.views import (UserLoginView, RegisterView, LogoutView, MainView, LikeProduct, DislikeProduct,
                                ProductView, ProductCommentView, CategoryView, DeleteCommentView,
                                BestRatedView, FrequentlyCommentedView)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user_login', UserLoginView.as_view(), name="user_login"),
    url(r'^register', RegisterView.as_view(), name='register'),
    url(r'^logout', LogoutView.as_view(), name="logout"),
    url(r'^products$', MainView.as_view(), name="main"),
    url(r'^products/like/(?P<my_id>(\d)+)/$', LikeProduct.as_view(), name='like_product'),
    url(r'^products/dislike/(?P<my_id>(\d)+)/$', DislikeProduct.as_view(), name='dislike_product'),
    url(r'^product/(?P<my_id>(\d)+)/$', ProductView.as_view(), name="product"),
    url(r'^product/(?P<my_id>(\d)+)/comments/$', ProductCommentView.as_view(), name='product_comment'),
    url(r'^category/(?P<name>([-A-Za-ząćęłńóśźżĄĘŁŃÓŚŹŻ])+)/', CategoryView.as_view(), name='category'),
    url(r'^comments/(?P<comment_id>(\d)+)$', DeleteCommentView.as_view(), name='delete_comment'),
    url(r'^bestrated/$', BestRatedView.as_view(), name="best_rated"),
    url(r'^frequentlycommented/$', FrequentlyCommentedView.as_view(), name="frequently_commennted"),

]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

