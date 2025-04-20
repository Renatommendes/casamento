from django.db import models

class Upload(models.Model):
    nome = models.CharField(max_length=255)
    arquivo = models.FileField(upload_to='temp_uploads/')  # só temporário
    link_drive = models.URLField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome