from django.shortcuts import render, get_object_or_404
from .models import Constitution
from django.views import generic


def index(request):
    return render(request, 'conex/index.html')

def about(request):
    return render(request, 'conex/about.html')

def map(request):
    return render(request, 'conex/map.html')

class CountriesView(generic.ListView):
    model = Constitution
    template_name = 'conex/countries.html'

    def get_queryset(self):
        context = Constitution.objects.all()
        return context

class DetailView(generic.DetailView):
    model = Constitution
    template_name = 'conex/detail.html'


# def add(request):

#     # country_data_csv = open(os.path.join(settings.BASE_DIR, 'conex/static/conex/countr_ids.csv'))
#     # country_data = pd.read_csv(country_data_csv)
#     countries = Constitution.objects.all()

#     for i in range(len(countries)):
#         # country_id = country_data['country_id'][i]
#         # url = 'https://www.constituteproject.org/service/html?cons_id='+country_id+'&lang=en'
#         # response = requests.get(url)
#         # data = response.json()
#         # html = data['html']
#         country = Constitution.objects.get(pk=(i+1))
#         # country = Constitution()
#         # country.country=country_data['country'][i]
#         # country.constitution_text=html
#         if(country.write_date == 'n'):
#             country.write_date="Draft"
#         # country.write_date=country.write_date[:-2]
#         country.save()
    
#     return render(request, 'conex/add.html')