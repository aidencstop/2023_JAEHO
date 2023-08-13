from django.contrib import auth
from django.contrib.auth import authenticate

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def main(request):
    if request.method == 'POST':
        if 'member' in request.POST:
            return redirect('/member/login/')
        if 'trainer' in request.POST:
            return redirect('/trainer/login/')
        if 'manager' in request.POST:
            return redirect('/manager/login/')

    return render(
        request,
        'index.html',
        {
        }
    )
