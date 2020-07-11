from django.shortcuts import render, redirect
# from .models import Porto 
# from .forms import PortoForm


def register_tentor(request):
    # return render(request, 'loop.html', { 'Porto': Porto.objects.all() })
    return render(request,'tentor.html')

# def form(request):
#     if request.method == "POST":
#         form = PortoForm(request.POST, request.FILES)
#         print("REQUEST", request, "form", form, "POST", request.POST, "FILES",request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('base')  # call with name from url 'base'
#     else:
#         form = PortoForm()
#     return render(request, 'form_content.html',{'form': form })

# def porto_get(request, porto_id):
#     return render(request, 'stuff.html',{'Porto': Porto.objects.get(pk=porto_id) })
