from django.contrib.auth import authenticate

from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(request.user.is_authenticated)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('posts:post-list')

        else:
            return redirect('members:login')

    else:
        return render(request, 'members/login.html')


def logout_view(request):
        logout(request)
        return redirect('posts:post-list')


def signup(request):
    # context에 dic형식으로 담아서 에러메시지를 출력
    context = {
        'errors': [],
    }
    # 회원가입 양식은 post 방식으로 받아서
    # request.POST 내용을 각각의(username, email, password, password2에 담아냄)
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # context에 POST로 받아온 username, email을 담아냄
        context['username'] = username
        context['email'] = email

        # 만약 username이 이미 존재한다면
        if User.objects.filter(username=username).exists():
            # context에 아래와 같은 에러를 context에 append함
            context['errors'].append('이미 존재합니다')
        if password != password2:
            context['errors'].append('패스워드가 일치하지 않습니다')

        # 만약에 errors가 없다면 user를 생성하여 로그인을 함
        if not context['errors']:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            login(request, user)
            # 여기까지 왔다면 메인 페이지인 post-list로 이동
            return redirect('posts:post-list')
    # 그게 아니라면 get 방식인데 회원가입 창을 보여줌
    return render(request, 'members/signup.html', context)
