from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Tabella squadre: nome
class Squadra(models.Model):
  nome = models.CharField('nome squadra', max_length=30)
  class Meta:
    verbose_name_plural = "squadre"
  
  def __str__(self):
    return self.nome

# Tabella calendario
class Calendario(models.Model):
  nomeCampionato = models.CharField('nome campionato', max_length=60, default="Serie A 2015/16")
  giornata = models.IntegerField('numero giornata')
  data = models.DateTimeField('data partita')
  squadraLocale = models.ForeignKey(Squadra, on_delete=models.CASCADE, related_name='locale', verbose_name='Squadra di casa (locale)')
  squadraOspite = models.ForeignKey(Squadra, on_delete=models.CASCADE, related_name='ospite', verbose_name='Squadra ospite')
  retiLocali = models.IntegerField('goal locali', validators=[MaxValueValidator(50), MinValueValidator(0)])
  retiOspiti = models.IntegerField('goal ospite', validators=[MaxValueValidator(50), MinValueValidator(0)])
  class Meta:
      verbose_name_plural = "Calendari"
  
  def __str__(self):
    return '[{}] {} - {}'.format(self.data.strftime("%d/%m/%Y"), self.squadraLocale, self.squadraOspite)

  def schedina(self):
      if self.retiLocali > self.retiOspiti:
        return "1"
      elif self.retiOspiti > self.retiLocali:
        return "2"
      else:
        return "X"
