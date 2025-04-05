from django.shortcuts import render, redirect
from django.http import HttpResponse,Http404
from .models import Mentorados, Navigators, DisponibilidadeHorarios
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime, timedelta
# Create your views here.
def mentorados(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method== 'GET':
        navigators = Navigators.objects.filter(user=request.user)
        mentorados = Mentorados.objects.filter(user=request.user)

        estagios_flat = [i[1] for i in Mentorados.estagio_choices]
        qtd_estagios = []
        for i, j in Mentorados.estagio_choices:
            qtd_estagios.append(Mentorados.objects.filter(estagio=i).count())

        return render(request, 'mentorados.html', {'estagios': Mentorados.estagio_choices, 'navigators': navigators, 'mentorados': mentorados, 'estagios_flat': estagios_flat, 'qtd_estagios': qtd_estagios})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        foto = request.FILES.get('foto')
        estagio = request.POST.get("estagio")
        navigator = request.POST.get('navigator')

        mentorado = Mentorados(
            nome = nome,
            foto = foto,
            estagio = estagio,
            navigator_id=navigator,
            user=request.user
        )

        mentorado.save()

        messages.add_message(request, constants.SUCCESS, 'Mentorado cadastrado com sucesso!')
        return redirect('mentorados')

def reunioes(request):
    if request.method == 'GET':
        return render(request, 'reunioes.html')
    elif request.method == 'POST':
        data = request.POST.get('data')
        data = datetime.strptime(data, '%Y-%m-%dT%H:%M')

        disponibilidades = DisponibilidadeHorarios.objects.filter(mentor=request.user).filter(
            data_INICIAL__gte=(data - timedelta(minutes=50)),
            data_INICIAL__lte=(data + timedelta(minutes=50))
        )

        if disponibilidades.exists():
            messages.add_message(request, constants.ERROR, 'Você ja possui uma reunião em aberto!')
            return redirect('reunioes')

        disponibilidades = DisponibilidadeHorarios(
            data_INICIAL=data,
            mentor=request.user,
        )
        disponibilidades.save()
        
        messages.add_message(request, constants.SUCCESS, 'Horario disponibilizado com sucesso!')
        return redirect('reunioes')