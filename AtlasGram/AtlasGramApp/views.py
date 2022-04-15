from django.http import *
from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse
from . models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)


def LikeView(request,pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.post_like.add(request.user)

    return HttpResponseRedirect(reverse('post-detail' , args=[str(pk)]))


class PostListView(ListView):
    model = Post
    template_name = 'AtlasGramApp/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2



class UserPostListView(ListView):
    model = Post
    template_name = 'AtlasGramApp/user_post.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    template_name = 'AtlasGramApp/post_detail.html'
    form = CommentForm



    def post(self,request,*args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()

            return redirect(reverse('post-detail', kwargs={"pk": post.pk}))

    def get_context_data(self, **kwargs):

        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        post_comments_count = PostComment.objects.all().filter(post=self.object.id).count()
        post_comments = PostComment.objects.all().filter(post=self.object.id)
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        context["post_comments"] = post_comments
        context["post_comments_count"] = post_comments_count
        context["total_likes"] = total_likes

        return context


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PostComment
    success_url = '/'

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user:
            return True
        return False




class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']
    
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False





def about(request):
    return render(request, 'AtlasGramApp/About.html')

def calendar(request):
    return render(request, 'AtlasGramApp/calendar.html')

def contacts(request):
    return render(request, 'AtlasGramApp/contacts.html')

def news(request):
    return render(request, 'AtlasGramApp/news.html')
