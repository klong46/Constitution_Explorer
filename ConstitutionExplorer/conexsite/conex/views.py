from django.shortcuts import render, get_object_or_404
from .models import Constitution
from django.views import generic
from html.parser import HTMLParser
import nltk
import plotly.express as px



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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        freq_dist = get_common_words(super().get_object().constitution_text)
        most_common = freq_dist.most_common(20)
        x_data = [word[0] for word in most_common]
        y_data = [word[1] for word in most_common]
        y_data.reverse(), x_data.reverse()
        fig = px.histogram(x=y_data,y=x_data, width=1300, height=700)
        fig.update_layout(xaxis_title="Count", yaxis_title="Most Common Words")
        fig.update_traces(
            hovertemplate="<br>".join([
            "Word: %{y}",
            "Count: %{x}",
        ])
)
        fig.write_html("conex/templates/conex/word_histogram.html")

        context['plain_text'] = most_common
        return context

class HTMLFilter(HTMLParser):
    text = ""
    def handle_data(self, data):
        self.text += data

def parse_html(html_text):
    f = HTMLFilter()
    f.feed(html_text)
    return f.text

#returns most common nouns and verbs
def get_common_words(html_text):
    plain_text = parse_html(html_text)
    token_list = nltk.word_tokenize(plain_text)
    tagged_tokens = nltk.pos_tag(token_list)
    nouns_and_verbs = [token[0] for token in tagged_tokens if token[1] in ['VBD','VB', 'VBP', 'NN', 'NNS','NNP', 'NNPS']]
    freq_dist = nltk.FreqDist(nouns_and_verbs)
    return freq_dist


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