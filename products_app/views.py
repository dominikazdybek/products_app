from .forms import LoginForm, RegisterForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views import View
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from .models import Product, LikeDislike, Comment
from django.shortcuts import render_to_response, render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core import serializers


# Create your views here.


class UserLoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, "user_login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"],
                                password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                # return HttpResponseRedirect('/logout')
                return HttpResponseRedirect("/products")

        return render(request, "user_login.html", {"form": form, "blad": True})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/user_login")


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = "/user_login"

    def form_valid(self, form):
        #dodawanie
        u = User()
        u.username = form.cleaned_data['username']
        u.first_name = form.cleaned_data['first_name']
        u.last_name = form.cleaned_data['last_name']
        u.email = form.cleaned_data['email']
        u.set_password(form.cleaned_data["password1"])
        u.save()

        return super(RegisterView, self).form_valid(form)


class MainView(LoginRequiredMixin, View):

    def get(self, request):
        products = Product.objects.all()
        like_dislike_user = LikeDislike.objects.filter(author=request.user)
        user = None
        if request.user.is_authenticated():
            user = request.user
            for product in products:
                like_dislike = product.likedislike_set.filter(author=user).last()
                if like_dislike is not None:
                    product.like_dislike_user = like_dislike.liked

        return render_to_response('main.html', {'products': products,
                                                'user': user})


class LikeProduct(View):

    def post(self, request, my_id):
        p = Product.objects.get(pk=my_id)
        u = request.user
        obj, created = LikeDislike.objects.update_or_create(author=u, product=p,
                                                            defaults={'liked': True})

        return HttpResponse(created)


class DislikeProduct(View):

    def post(self, request, my_id):
        p = Product.objects.get(pk=my_id)
        u = request.user
        obj, created = LikeDislike.objects.update_or_create(author=u, product=p,
                                                            defaults={'liked': False})
        return HttpResponse(created)


class ProductView(View):

    def get(self, request, my_id):
        user = request.user
        form = CommentForm()
        product = Product.objects.get(pk=my_id)
        like_dislike_user = LikeDislike.objects.filter(author=request.user)
        comments = Comment.objects.filter(product=product)
        user = request.user
        like_dislike = product.likedislike_set.filter(author=user).last()
        if like_dislike is not None:
            product.like_dislike_user = like_dislike.liked

        return render_to_response('product.html', {'product': product,
                                                   'comments': comments,
                                                   'user': user,
                                                   "form": form})


class ProductCommentView(View):

    def post(self, request, my_id):
        p = Product.objects.get(pk=my_id)
        comment = request.body
        u = request.user
        if comment:
            # content = form.cleaned_data['content']
            new_comment = Comment.objects.create(content=comment, author=u, product=p)
            return JsonResponse({
                'author': new_comment.author.username,
                'date': new_comment.date,
                'comment': str(new_comment.content.decode('utf-8')),
                'id': new_comment.id
            })




class CategoryView(View):

    def get(self,request,  name):
        products = Product.objects.filter(name=name)
        user = request.user
        like_dislike_user = LikeDislike.objects.filter(author=request.user)
        for product in products:
            like_dislike = product.likedislike_set.filter(author=user).last()
            if like_dislike is not None:
                product.like_dislike_user = like_dislike.liked
        return render_to_response('category.html', {'products': products,
                                                    'user':user})


class DeleteCommentView(View):

    def delete(self, request, comment_id):
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()
        return HttpResponse(status=204)
