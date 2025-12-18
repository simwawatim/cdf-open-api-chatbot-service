from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

from chat.serializers import ChatEntrySerializer
from .models import ChatEntry

# ---------------- Load Chat Entries ----------------
def load_chat_entries():
    entries = ChatEntry.objects.all()
    questions = [entry.question.lower().strip() for entry in entries]
    answers = [entry.answer.strip() for entry in entries]
    # Full-question mapping for exact matches
    question_map = {entry.question.lower().strip(): entry.answer.strip() for entry in entries}
    return questions, answers, question_map

# ---------------- Precompute TF-IDF ----------------
questions, answers, question_map = load_chat_entries()
vectorizer = TfidfVectorizer(ngram_range=(1,2), stop_words='english')
X = vectorizer.fit_transform(questions) if questions else None

# ---------------- Chat Logic ----------------
def get_chat_response(user_input: str) -> str:
    user_input_lower = user_input.lower().strip()

    # Exact full-question match
    if user_input_lower in question_map:
        return question_map[user_input_lower]

    # Special command for word probabilities
    if user_input_lower == "__word_probs__":
        all_text = " ".join(questions)
        words = all_text.split()
        total_words = len(words)
        if total_words == 0:
            return {}
        word_counts = Counter(words)
        word_probabilities = {word: count / total_words for word, count in word_counts.items()}
        # Top 20 words
        return dict(sorted(word_probabilities.items(), key=lambda x: x[1], reverse=True)[:20])

    # TF-IDF similarity fallback
    if not questions or X is None:
        return "Sorry, I don't have any data to answer that."

    user_vec = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_vec, X)
    best_match_idx = similarities.argmax()

    if similarities[0][best_match_idx] < 0.4:  # adjust threshold if needed
        return "Sorry, I didn't understand that. Could you rephrase it?"

    return answers[best_match_idx]

# ---------------- Chat API ----------------
class ChatAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user_message = request.data.get("message", "").strip()
        if not user_message:
            return Response({
                "status": "fail",
                "message": "Message is required",
                "data": None,
                "status_code": 400
            }, status=status.HTTP_400_BAD_REQUEST)

        reply = get_chat_response(user_message)

        if isinstance(reply, dict):
            return Response({
                "status": "success",
                "message": "Word probabilities computed successfully",
                "data": reply,
                "status_code": 200
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "success",
            "message": "Response generated successfully",
            "data": {"reply": reply},
            "status_code": 200
        }, status=status.HTTP_200_OK)

# ---------------- Chat Entry CRUD API ----------------
class ChatEntryListCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        entries = ChatEntry.objects.all()
        serializer = ChatEntrySerializer(entries, many=True)
        return Response({
            "status": "success",
            "data": serializer.data,
            "status_code": 200
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ChatEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Update global cache for TF-IDF and question map
            global questions, answers, question_map, X
            questions, answers, question_map = load_chat_entries()
            X = vectorizer.fit_transform(questions) if questions else None

            return Response({
                "status": "success",
                "message": "Question-answer added successfully",
                "data": serializer.data,
                "status_code": 201
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "fail",
            "message": "Invalid data",
            "errors": serializer.errors,
            "status_code": 400
        }, status=status.HTTP_400_BAD_REQUEST)
