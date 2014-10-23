# -*- coding: utf-8 -*-
# Import the reverse lookup function
from django.core.urlresolvers import reverse

# view imports
# from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from django.views.generic import CreateView

# Only authenticated users can access views using this.
from braces.views import LoginRequiredMixin

# Import the form from users/forms.py
from .forms import AgentForm
from .forms import AgentIdCardForm
from .forms import AgentAddressForm
from .forms import PoleEmploiForm
from .forms import CertificationsFormHelper
from .forms import AgentCertificationsForm
from .forms import AgentProCardForm

# Import the customized User model
from .models import Agent
from .models import AgentCertification
from .models import AgentIdCard
from .models import AgentAddress
from .models import AgentProCard
# from .models import AGENT_FORM_STATE

# Various imports
from django.http import HttpResponseRedirect
from extra_views import ModelFormSetView

# import messages
from django.contrib import messages




def AddAgentContextProcessor(self, request):
    try:
        user = self.user.request
        agent = user.Agent
        return {'agent': agent}
    except Agent.DoesNotExist:
        print"super pb"
        return {'marchepas': 'dededede'}


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})


class AgentCertificationsCreateView(LoginRequiredMixin, ModelFormSetView):
    template_name = 'agent/agent_certification_form.html'
    model = AgentCertification
    fields = ('certification', 'start_date', 'end_date', 'picture')
    can_delete = True
    extra = 3
    max_num = 3
    form_class = AgentCertificationsForm

    def get_queryset(self):
        queryset = AgentCertification.objects.filter(agent=self.request.user.agent)
        return queryset


    def get_context_data(self, **kwargs):
        context = super(AgentCertificationsCreateView, self).get_context_data(**kwargs)
        context['helper'] = CertificationsFormHelper
        return context

    def formset_valid(self, formset):
        self.user = self.request.user
        new_instances = formset.save(commit=False)
        for i in new_instances:
            i.agent = self.user.agent
        formset.save()
        obj = Agent.objects.get(user=self.request.user)
        AGENT_FORM_STATE = obj.form_state
        AGENT_FORM_STATE['CERTIFICATIONS'] = 1
        Agent.objects.filter(user = self.request.user).update(form_state = AGENT_FORM_STATE)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("agent:~agent_certification",)


class AgentView(LoginRequiredMixin, UpdateView):

    form_class = AgentForm
    model = Agent
    template_name = 'agent/profile.html'

    def get_object(self, queryset=None):
        obj, created = Agent.objects.get_or_create(user=self.request.user)
        return obj

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("agent:~agent")

    def form_valid(self, form):
        form.save()
        obj = Agent.objects.get(user=self.request.user)
        AGENT_FORM_STATE = obj.form_state
        AGENT_FORM_STATE['AGENT'] = 1
        Agent.objects.filter(user = self.request.user).update(form_state = AGENT_FORM_STATE)
        messages.add_message(self.request, messages.INFO, u'Informations sauvegardées avec succès.')
        return HttpResponseRedirect(self.get_success_url())

class PoleEmploiUpdateView(LoginRequiredMixin, UpdateView):

    form_class = PoleEmploiForm
    model = Agent
    template_name = 'agent/poleemploi_form.html'

    def get_object(self, queryset=None):
        return Agent.objects.get(user=self.request.user)

    def form_valid(self, form):
            obj = form.save(commit=False)
            obj.user = self.request.user
            obj.save()
            return HttpResponseRedirect(self.get_success_url())

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})


class AgentIdCardView(LoginRequiredMixin, UpdateView):

    form_class = AgentIdCardForm
    model = AgentIdCard
    template_name = 'agent/profile.html'

    def get_object(self, queryset=None):
        obj, created = AgentIdCard.objects.get_or_create(agent=self.request.user.agent)
        return obj

    def form_valid(self, form):
        form.save()
        obj = Agent.objects.get(user=self.request.user)
        AGENT_FORM_STATE = obj.form_state
        AGENT_FORM_STATE['PAPIERS_IDENTITE'] = 1
        Agent.objects.filter(user = self.request.user).update(form_state = AGENT_FORM_STATE)
        messages.add_message(self.request, messages.INFO, u'Informations sauvegardées avec succès.')
        return HttpResponseRedirect(self.get_success_url())

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("agent:~agent_id_card",)


class AgentAddressView(LoginRequiredMixin, UpdateView):

    form_class = AgentAddressForm
    model = AgentAddress
    template_name = 'agent/profile.html'

    def get_object(self, queryset=None):
        obj, created = AgentAddress.objects.get_or_create(agent=self.request.user.agent)
        return obj

    def form_valid(self, form):
        form.save()
        obj = Agent.objects.get(user=self.request.user)
        AGENT_FORM_STATE = obj.form_state
        AGENT_FORM_STATE['COORDONNEES'] = 1
        Agent.objects.filter(user = self.request.user).update(form_state = AGENT_FORM_STATE)
        messages.add_message(self.request, messages.INFO, u'Informations sauvegardées avec succès.')
        return HttpResponseRedirect(self.get_success_url())

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("agent:~agent_id_card",)


class AgentProCardView(LoginRequiredMixin, UpdateView):

    form_class = AgentProCardForm
    model = AgentProCard
    template_name = 'agent/profile.html'

    def get_object(self, queryset=None):
        obj, created = AgentProCard.objects.get_or_create(agent=self.request.user.agent)
        return obj

    def form_valid(self, form):
        form.save()
        obj = Agent.objects.get(user=self.request.user)
        AGENT_FORM_STATE = obj.form_state
        AGENT_FORM_STATE['CARTE_PRO'] = 1
        print "dadadaa", AGENT_FORM_STATE
        Agent.objects.filter(user = self.request.user).update(form_state = AGENT_FORM_STATE)
        messages.add_message(self.request, messages.INFO, u'Informations sauvegardées avec succès.')
        return HttpResponseRedirect(self.get_success_url())

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("agent:~agent_pro_card",)
