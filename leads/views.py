from ast import Del
from email import message
from unicodedata import category
from django.contrib import messages
from re import template
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import Lead, Agent, Category
from django.views import generic # generic will hold different module for quickly creating different template
from django.core.mail import send_mail 
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm #will be used by lead_create
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import organizerAndLoginRequiredMixin 
#views are all about handling web requests and returning responses
#CRUD - Create, Retrieve, Update, and Delete

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    def get_success_url(self):
        return reverse("login")


class LandingPageView(generic.TemplateView): #class based view help us become less redundant 
    template_name = "landing.html"  

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

class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"
    def get_queryset(self):
        user = self.request.user
        #initially queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organization = user.userprofile, agent__isnull=False)
        
        else:
            queryset = Lead.objects.filter(organization = user.agent.organization, agent__isnull=False)
            #filter based on agent that is logged in 
            queryset = queryset.filter(agent__user = user)
        queryset = queryset.filter(agent__user = user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization = user.userprofile, 
                agent__isnull=True
                )
            context.update({
                "unassigned_leads": queryset
            })
        return context

def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads
    }
    return render(request, "leads/lead_list.html", context)

class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        #initially queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organization = user.userprofile)
        
        else:
            queryset = Lead.objects.filter(organization = user.agent.organization)
            #filter based on agent that is logged in 
            queryset = queryset.filter(agent__user = user)
        queryset = queryset.filter(agent__user = user)
        return queryset


def lead_detail(request, pk): #fetch specific instance of a model 
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead,
    }
    return render(request, "leads/lead_detail.html", context)

"""def lead_create(request): #creating lead, theres easier way to do it (shown below) but this gets us grounded in the fundamental
    #important note this function does not follow a sequence it goes from line 50 to to 67 to 68,69,70, then jumps back upto 51 and continutes
    form = LeadForm() #leadForm() method is in our forms module
    if request.method == "POST":  #checking for 'POST' from request.method which can be found in lead_create.html 
        print("Reciving a post request")
        form = LeadForm(request.POST)#insert the POST into the leadForm function 
        if form.is_valid():#will check if every field is correctly filled
            print(form.cleaned_data) #to make our submitted data into clean dictionatry format
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            agent = Agent.objects.first() #grabbing the first agent from the database 
            Lead.objects.create( #data can be passed into object manager where .create is called to create new lead with the specified paramater  
                first_name = first_name,
                last_name = last_name,
                age = age,
                agent = agent 
            )
            return redirect('/leads') #after everything is confirmed we will redirect the user
    context = { #we will pass the form into the context to render out into the template lead_create.html
        "form": form 
    }
    return render(request, "Leads/lead_create.html", context)#render will take in the context to render it into kead_Create.html 
"""
class LeadCreateView(organizerAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    def get_success_url(self):
        return reverse("leads:lead-list")
    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organization = self.request.user.userprofile
        lead.save()
        send_mail(
            subject = "A lead has been created", 
            message = "Go to the site to see the new lead",
            from_email = "test@test.com",
            recipient_list=["test2@test.com"] 
        )
        messages.success(self.request, "You have successfully created a lead")
        return super(LeadCreateView, self).form_valid(form)  #Here we tell django we are going to utilize form_valid how we want to after that you can continue normally with form_valid 

def lead_create(request): #reimplementing form with LeadModelForm()
    form = LeadModelForm() #leadmodelForm() method is in our forms module
    if request.method == "POST":  
        print("Reciving a post request")
        form = LeadModelForm(request.POST)
        if form.is_valid(): 
            #all the data passed into the form will be saved as a new model in database 
            form.save() #the reason we can do this is b/c we specify what model we are working with in the forms.py module
            return redirect('/leads') 
    context = { 
        "form": form 
    }
    return render(request, "leads/lead_create.html", context)




"""def lead_update(request, pk): #easier way to do it shown below
    lead = Lead.objects.get(id=pk)
    form = LeadForm() #leadForm() method is in our forms module
    if request.method == "POST":  #checking for 'POST' from request.method which can be found in lead_create.html 
        form = LeadForm(request.POST)#insert the POST into the leadForm function 
        if form.is_valid():#will check if every field is correctly filled
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            lead.first_name = first_name
            lead.last_name = last_name
            lead.age = age
            lead.save()
            return redirect('/leads') #after everything is confirmed we will redirect the user
    
    context = {
        "form": form,
        "lead": lead

    }
    return render(request, "Leads/lead_update.html", context)
"""
class LeadUpdateView(organizerAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    def get_queryset(self):
        user = self.request.user
        #initially queryset of leads for the entire organization
        return Lead.objects.filter(organization = user.userprofile)
    def get_success_url(self):
        return reverse("leads:lead-list")

def lead_update(request, pk): #same as above "lead_update" method with this one being shorter 
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead) #instance = single instance of the model that we want to update
    if request.method == "POST":  
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid(): 
            form.save() #the reason we can do this is b/c we specify what model we are working with in the forms.py module
            return redirect('/leads') 
    
    context = {
        "form": form,
        "lead": lead

    }
    return render(request, "Leads/lead_update.html", context)

class LeadDeleteView(organizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"
    queryset = Lead.objects.all()
    
    def get_success_url(self) -> str:
        return reverse('leads:lead-list')
    def get_queryset(self):
        user = self.request.user
        #initially queryset of leads for the entire organization
        return Lead.objects.filter(organization = user.userprofile)

def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete() #allows you to delete model from database
    return redirect("/leads")


def landing_page(request):
    return render(request, "landing.html")

class AssignAgentView(organizerAndLoginRequiredMixin, generic.FormView):
    
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm
    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse('leads:lead-list')
    
    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent 
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/categroy_list.html"
    context_object_name = "category_list"
    
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organization = user.userprofile)
        
        else:
            queryset = Lead.objects.filter(organization = user.agent.organization)
        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context
    def get_queryset(self):
        user = self.request.user
        #initially queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Category.objects.filter(organization = user.userprofile)
        
        else:
            queryset = Category.objects.filter(organization = user.agent.organization)
        return queryset

class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"


    def get_queryset(self):
        user = self.request.user
        #initially queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Category.objects.filter(organization = user.userprofile)
        
        else:
            queryset = Category.objects.filter(organization = user.agent.organization)
        return queryset

class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm


    def get_queryset(self):
        user = self.request.user
        #initially queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organization = user.userprofile)
        
        else:
            queryset = Lead.objects.filter(organization = user.agent.organization)
            #filter based on agent that is logged in 
            queryset = queryset.filter(agent__user = user)
        queryset = queryset.filter(agent__user = user)
        return queryset
    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk":self.get_object().id})