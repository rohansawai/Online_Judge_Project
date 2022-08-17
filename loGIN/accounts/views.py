from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from django.http import JsonResponse 
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from multiprocessing import context
from .forms import FileSubmission
from django.utils import timezone
from .models import Problem
from .models import Solution
import subprocess
from django.contrib import messages

# Create your views here.
def indexView(request):
    p1 = {
        'Problem_List' : Problem.objects.order_by('-problem_level')[:2]
    }
    return render(request, 'index.html', p1)


    
@login_required
def dashboardView(request):
    return render(request, 'dashboard.html')

def registerView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_url')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form':form})

@login_required
def details(request,problem_id):
    problem = get_object_or_404(Problem,pk=problem_id)
    return render(request,'details.html',{'problem': problem })

@login_required
def submission(request, problem_id):
    if request.method == 'POST':
        file = request.FILES.get('problem_code')
        if file != None:
            filename = file.name
            if filename.endswith('.cpp'):
                with open(f'accounts/codeFiles/sample.cpp', 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                compile_com = "g++ accounts\codeFiles\sample.cpp -o accounts\codeFiles\output.exe"
                run_com = "accounts\codeFiles\sample.exe"
                try:
                    subprocess.run(compile_com, shell=True,
                                       check=True, timeout=3)
                    try:
                        testcases = TestCase.objects.all().filter(problem_id=problem_id)
                        flag = True
                        for testcase in testcases:
                            op = subprocess.run(run_com, input=testcase.input, capture_output=True, check=True, timeout=1, text=True)
                            sample_out = testcase.output
                            curr_op = op.stdout.strip()
                            curr_op = ' '.join(curr_op.splitlines())
                            print(curr_op)
                            if(curr_op!=sample_out):
                                flag = False
                                break
                        # flag = True
                        # for i in range(0,len(sample_out)):
                        #     if curr_op[i] != '\n':
                        #         if(curr_op[i] != sample_out[i]):
                        #             flag = False
                        # for i in range(0,len(sample_out)):
                        #     print("curr_op: ",curr_op[i]," ", "sample_out: ",sample_out[i])
                        #     print()
                        # print(sample_out)
                        # print(curr_op)
                        if(flag):
                            print("Correct Answer")
                            verdict = "AC"
                        else:
                            print("Wrong Answer")
                            verdict="WA"
                    except subprocess.TimeoutExpired:
                        print("Timeout (TLE)")
                        verdict = "TLE"

                except subprocess.CalledProcessError as e:
                    if e.returncode != 0:
                        print("Compilation Error")
                        verdict = "Compilation Error"
                finally:
                    sol = Solution()
                    sol.user = request.user
                    sol.problem_id = Problem.objects.get(pk=problem_id)
                    with open(f'accounts/codeFiles/sample.cpp', 'r') as destination:
                        sol.problem_code = destination.read()
                    sol.submitted_at = timezone.now()
                    sol.Verdict = verdict
                    sol.save()
                    messages.success(request, "File Uploaded Succesfully")
                    return HttpResponseRedirect(reverse('leaderboard'))
            else:
                messages.warning(request, "Wrong File Uploaded")
                return HttpResponseRedirect(f'/accounts/{problem_id}/')

        else:
            messages.error(request, "File not added")
            return HttpResponseRedirect(f'/accounts/{problem_id}/')


@login_required
def leaderboard(request):
    p2 = {
        'sol' : Solution.objects.all().order_by('-submitted_at')[:10],
    }
    return render(request,'finalpage.html', p2)



