from django.shortcuts import render, redirect
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from app.models import Post
import time


def home(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        start = time.time()

        # Define categories to fetch and create a mapping for broader labels
        categories = [
            'alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc',
            'comp.sys.ibm.pc.hardware', 'comp.sys.mac.hardware', 'comp.windows.x',
            'misc.forsale', 'rec.autos', 'rec.motorcycles', 'rec.sport.baseball',
            'rec.sport.hockey', 'sci.crypt', 'sci.electronics', 'sci.med',
            'sci.space', 'soc.religion.christian', 'talk.politics.guns',
            'talk.politics.mideast', 'talk.politics.misc', 'talk.religion.misc'
        ]

        # Mapping to group similar categories under broader labels
        category_mapping = {
            'alt.atheism': 'Atheism',
            'soc.religion.christian': 'Christianity',
            'comp.graphics': 'Graphics',
            'comp.os.ms-windows.misc': 'Windows OS',
            'comp.sys.ibm.pc.hardware': 'IBM Hardware',
            'comp.sys.mac.hardware': 'Mac Hardware',
            'comp.windows.x': 'Windows X',
            'misc.forsale': 'For Sale',
            'rec.autos': 'Sports',
            'rec.motorcycles': 'Sports',
            'rec.sport.baseball': 'Sports',
            'rec.sport.hockey': 'Sports',
            'sci.crypt': 'Cryptography',
            'sci.electronics': 'Electronics',
            'sci.med': 'Medicine',
            'sci.space': 'Space',
            'talk.politics.guns': 'Politics',
            'talk.politics.mideast': 'Politics',
            'talk.politics.misc': 'Politics',
            'talk.religion.misc': 'Religion'
        }

        # Fetch training data
        train = fetch_20newsgroups(subset='train', categories=categories)

        # Build and train the model
        model = make_pipeline(TfidfVectorizer(), MultinomialNB())
        model.fit(train.data, train.target)
        
        # Prediction function for a given text
        def predict_category(text):
            pred = model.predict([text])[0]
            raw_category = train.target_names[pred]
            # Map raw category to broader label
            return category_mapping.get(raw_category, raw_category)

        # Predict the category of the input text
        predicted_category = predict_category(text)

        # Save to Post model with the mapped category
        create_post = Post.objects.create(title=text, category=predicted_category)

        return redirect(news)

    return render(request, 'app/input.html')

def news(request):
    categories = {post.category for post in Post.objects.all()}
    

    context = {
        'categories': categories
    }
    return render(request, 'app/news.html', context)

def category(request, i):
    posts = Post.objects.filter(category = i)

    context = {
        'posts': posts,
        'category': i
    }
    return render(request, 'app/category.html', context)


def setup(request):
    return render(request, 'app/setup.html')