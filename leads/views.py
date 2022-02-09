from django.shortcuts import render, redirect 
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadForm #will be used by lead_create 
# Create your views here.
#views all about handling web requests and returning responses



def home_page(request): #function takes a request
    #return HttpResponse("Hello world") #when someone make a request we return hello world
    
    return render(request, "leads/home_page.html") #we tell sjango about request, name of the template 

def second_page(request):
    #this second_page.html we created in the root, unlike the home_page.html
    # since we created in the root, we must tell django about it by going to setting-->template-->DIR [] and putting DIR[BASE_DIR/"templates"] 
    return render(request, "second_page.html") #now we can just name the .html without naming a directory

def third_page(request):
    # context={ #context, dictionary of information,  is used to pass information into django template by doing providing the key inside {{}}
    #     "name":"Joe",
    #     "age":35
    # }
    leads = Lead.objects.all()
    context = {
        "leads": leads
    }
    return render(request, "third_page.html", context)

def random_page(request):
    return HttpResponse("what made you want to come here?")

def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads
    }
    return render(request, "leads/lead_list.html", context)

def lead_detail(request, pk): #fetch specific instance of a model 
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead,
    }
    return render(request, "leads/lead_detail.html", context)

def lead_create(request): #creating lead
    form = LeadForm() #leadForm() method is in our forms module
    if request.method == "POST":  #request.method can be found in lead_create.html 
        print("Reciving a post request")
        form = LeadForm(request.POST)#insert the POST into the leadForm function 
        if form.is_valid():#will check if every field is correctly filled
            print("form looks goods")
            print(form.cleaned_data) #to make our submitted data into clean dictionatry format
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            agent = Agent.objects.first()
            Lead.objects.create(
                first_name = first_name,
                last_name = last_name,
                age = age,
                agent = agent 
            )
            print("lead is created")
            return redirect('/leads')
    context = { #we will pass the form into the context to render out into the template lead_create.html
        "form": form 
    }
    return render(request, "Leads/lead_create.html", context)#render will take in the context to render it into kead_Create.html 
