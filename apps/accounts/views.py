from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import UserProfileSerializer, DepositSerializer
class LogoutView(APIView):
    """Logout by blacklisting refresh token. Send: {"refresh": "token"}"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Refresh token required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            RefreshToken(refresh_token).blacklist()
            return Response({'message': 'Logged out successfully.'})
        except TokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
class ProfileView(APIView):
    """Get or update the logged-in user's profile."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DepositView(APIView):
    """Add money to user balance for bookings."""
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            amount= serializer.validated_data['amount']
            request.user.balance += amount
            request.user.save(update_fields=['balance'])
            return Response({
                'message':     f'Successfully deposited ${amount}.',
                'new_balance': float(request.user.balance),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
