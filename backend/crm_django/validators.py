from django.contrib.auth.password_validation import UserAttributeSimilarityValidator, MinimumLengthValidator, CommonPasswordValidator, NumericPasswordValidator
from django.utils.translation import ngettext

class CustomAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    def get_help_text(self):
        return (
            "Tu contraseña no puede ser muy similar a tu informacion personal.")

class CustomMinimumLengthValidator(MinimumLengthValidator):
    def get_help_text(self):
        return ngettext(
            "Tu contraseña debe de conteer por lo menos %(min_length)d caracter.",
            "Tu contraseña debe de contener por lo menos %(min_length)d caracteres.",
            self.min_length,
        ) % {"min_length": self.min_length}

class CustomCommonPasswordValidator(CommonPasswordValidator):
    def get_help_text(self):
        return ("Tu contraseña no puede ser una contraseña comun.")

class CustomNumericPasswordValidator(NumericPasswordValidator):
    def get_help_text(self):
        return ("Tu contraseña no puede ser enteramente numerica.")


