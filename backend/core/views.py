from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.db import IntegrityError
from .serializers import BlogPostSerializer, UserSerializer
from .models import BlogPost
from django.http import JsonResponse

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'name': user.full_name
                    }
                }, status=201)
            except IntegrityError:
                return Response({'error': 'Email already exists'}, status=400)
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.full_name
                }
            }, status=200)
        return Response({'error': 'Invalid credentials'}, status=401)

class BlogPostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)  # ✅ Set author from logged-in user
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# for blog view
def blog_posts(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    data = [
        {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author_name': post.author.full_name,
            'created_at': post.created_at.strftime("%B %d, %Y")
        }
        for post in posts
    ]
    return JsonResponse(data, safe=False)
