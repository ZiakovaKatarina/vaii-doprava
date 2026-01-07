from django.db import models
from django.conf import settings

class FavouriteRoute(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Použite toto namiesto priamej referencie
        on_delete=models.CASCADE,
        verbose_name='Používateľ'
    )
    startLocation = models.CharField(max_length=100, verbose_name='Počiatočný bod')
    endLocation = models.CharField(max_length=20, verbose_name='Koncový bod')

    class Meta:
        verbose_name = 'Obľúbená trasa'
        verbose_name_plural = 'Obľúbené trasy'
        unique_together = ('user', 'startLocation', 'endLocation')
    
    def __str__(self):
        return f"{self.user.username}: from {self.startLocation} to {self.endLocation}"