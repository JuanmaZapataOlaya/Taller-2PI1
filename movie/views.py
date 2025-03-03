from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt 
import matplotlib 
import io 
import urllib, base64 

from .models import Movie

# create your views here

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name':'Paola Vallejo'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies':movies})


def about(request):
    #return HttpResponse('<h1>Welcome to About Page</h1>')
    return render(request, 'about.html')

def statistics_view(request):
    matplotlib.use('Agg')  # Usar backend no interactivo
    
    # Obtener todas las películas
    all_movies = Movie.objects.all()
    
    # Diccionarios para almacenar conteos
    movie_counts_by_year = {}
    movie_counts_by_genre = {}
    
    # Contar películas por año y por género
    for movie in all_movies:
        year = movie.year if movie.year else "Unknown"
        genre = movie.genre.split(",")[0] if movie.genre else "Unknown"
        
        movie_counts_by_year[year] = movie_counts_by_year.get(year, 0) + 1
        movie_counts_by_genre[genre] = movie_counts_by_genre.get(genre, 0) + 1
    
    # Crear y guardar la primera gráfica (Movies per Year)
    buffer1 = io.BytesIO()
    plt.figure(figsize=(10, 5))
    plt.bar([str(year) for year in movie_counts_by_year.keys()], movie_counts_by_year.values(), width=0.5, align='center')
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(buffer1, format='png')
    buffer1.seek(0)
    plt.close()
    
    # Convertir la primera gráfica a base64
    image_png1 = buffer1.getvalue()
    buffer1.close()
    graphic1 = base64.b64encode(image_png1).decode('utf-8')

    # Crear y guardar la segunda gráfica (Movies per Genre)
    buffer2 = io.BytesIO()
    plt.figure(figsize=(10, 5))
    plt.bar(movie_counts_by_genre.keys(), movie_counts_by_genre.values(), width=0.5, align='center', color='orange')
    plt.title('Movies per Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(buffer2, format='png')
    buffer2.seek(0)
    plt.close()

    # Convertir la segunda gráfica a base64
    image_png2 = buffer2.getvalue()
    buffer2.close()
    graphic2 = base64.b64encode(image_png2).decode('utf-8')

    return render(request, 'statistics.html', {'graphic1': graphic1, 'graphic2': graphic2})


def signup(request):
    email= request.GET.get('email')
    return render(request, 'signup.html',{'email':email})