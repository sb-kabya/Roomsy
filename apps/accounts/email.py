from djoser.email import (
    ActivationEmail as BaseActivationEmail,
    ConfirmationEmail as BaseConfirmationEmail,
    PasswordResetEmail as BasePasswordResetEmail,
    PasswordChangedConfirmationEmail as BasePasswordChangedConfirmationEmail,
)
class ActivationEmail(BaseActivationEmail):
    template_name = 'email/activation.html'

class ConfirmationEmail(BaseConfirmationEmail):
    template_name = 'email/confirmation.html'
class PasswordResetEmail(BasePasswordResetEmail):
    template_name = 'email/password_reset.html'
class PasswordChangedConfirmationEmail(BasePasswordChangedConfirmationEmail):
    template_name = 'email/password_changed.html'
