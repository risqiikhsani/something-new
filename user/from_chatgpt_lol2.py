from .serializers_auth import ForgotPassword_Serializer
from random import randint

class ForgotPassword(generics.GenericAPIView):
    serializer_class = ForgotPassword_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            user = get_object_or_404(User, email=email)

            # Generate a 4-digit verification code
            verification_code = str(randint(1000, 9999))

            # Save the verification code in the user's profile or any other suitable place
            user.profile.verification_code = verification_code
            user.profile.save()

            # Send email with the verification code
            app_name = "Testing"
            name = user.profile.name
            subject = f'Verification from {app_name} App'
            message = f'Hi {name}, your verification code is: {verification_code}. Enter this code to reset your password.'
            email_from = settings.EMAIL_HOST_USER
            recepient_list = [user.email,]
            send_mail(subject, message, email_from, recepient_list, fail_silently=False)

            return Response({"message": "Reset Password Guide has been sent to email"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from .serializers_auth import ForgotPasswordConfirm_Serializer

class ForgotPasswordConfirm(generics.GenericAPIView):
    serializer_class = ForgotPasswordConfirm_Serializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            verification_code = serializer.validated_data['verification_code']
            new_password = serializer.validated_data['password']

            try:
                user = User.objects.get(profile__verification_code=verification_code)
                # Reset the user's password
                user.set_password(new_password)
                user.save()
                # Clear the verification code after successful password reset
                user.profile.verification_code = ''
                user.profile.save()
            except User.DoesNotExist:
                return Response({'detail': 'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Password updated successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
