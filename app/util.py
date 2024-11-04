# app/util.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from app.models import Post

def all_categories():
    # Define categories and names as a dictionary (you may adjust categories as needed)
    category_names = {
        'alt.atheism': 'Atheism',
        'soc.religion.christian': 'Christianity',
        'comp.graphics': 'Graphics',
        'sci.med': 'Medicine'
    }
    return list(category_names.values())

def get_post_predictions():
    # Retrieve posts from the Post model
    posts = Post.objects.all()
    
    # Assuming each Post instance has a `title` field to use for content
    post_texts = [post.title for post in posts]
    
    # Manually label some of the posts for training (this would be your "ground truth" data)
    # For demonstration, I'm assuming labels based on content (adjust this part as needed)
    post_labels = []
    for text in post_texts:
        if "god" in text.lower():
            post_labels.append('Christianity')
        elif "graphics" in text.lower():
            post_labels.append('Graphics')
        elif "medicine" in text.lower():
            post_labels.append('Medicine')
        else:
            post_labels.append('Atheism')
    
    # Train the model
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(post_texts, post_labels)

    # Predict categories for each post
    predictions = [
        {
            'post': post,
            'predicted_category': model.predict([post.title])[0]
        }
        for post in posts
    ]

    return predictions


"""

# app/views.py
from django.shortcuts import render
from app.util import all_categories, get_post_predictions

def home(request):
    # Get categories and predictions
    categories = all_categories()
    predictions = get_post_predictions()

    context = {
        'categories': categories,
        'predictions': predictions
    }
    return render(request, 'app/home.html', context)


"""