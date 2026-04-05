import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

with open("../data/faq.json") as f:
    data=json.load(f)

questions=[item["question"] for item in data["faqs"]]
answers=[item["answer"] for item in data["faqs"]]

vectorizer=TfidfVectorizer()
X=vectorizer.fit_transform(questions)

def get_response(user_input):
    user_vec=vectorizer.transform([user_input])
    similarity = cosine_similarity(user_vec, X)
    idx = similarity.argmax()

    if similarity[0][idx] < 0.3:
        return "I don't understand. Please raise a ticket."

    return answers[idx]