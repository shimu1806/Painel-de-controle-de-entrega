from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager): 
    def create_superuser(self, email, username, password=None):

        return self.create_user(username, email, password)
      

    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Please provide an email address")
   

        email = self.normalize_email(email)
        user  = self.model(
            email=email,
            username=username,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    objects = create_user, create_superuser

class User(AbstractBaseUser):
    
    email           = models.EmailField(('email address'), unique = True)
    username        = models.CharField(max_length=50, unique=True)
    is_active       = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email']

"""
|*****************************************************************|
|                                                                 |
|   CLASSE DE TESTE - https://jsonplaceholder.typicode.com/todos  |
|                                                                 |
|*****************************************************************|
"""

class Todo(models.Model):  

    userId      = models.IntegerField()
    id          = models.AutoField(primary_key=True)
    title       = models.CharField(max_length=100)
    completed   = models.BooleanField(default=False)

class Produto(models.Model):

    CB7_STATUS  = models.IntegerField()                              # Campo status                                  -> Deve ser colorido
    CB7_FILIAL  = models.CharField(max_length=50)                    # Campo código da filial '01 / 02 / 03'                 * primarykey
    CB7_ORDSEP  = models.CharField(max_length=50, unique=True)       # Campo código ordem de separação 6 digitos
    CB7_PEDIDO  = models.CharField(max_length=50)                    # Campo código Pedido 6 digitos
    CB7_CLIENT  = models.CharField(max_length=6)                     # Campo código cliente C###### 
    CB7_LOJA    = models.CharField(max_length=50)                    # Campo código loja '01 / 02 / etc...'
    A1_NOME     = models.CharField(max_length=50)                    # Campo Nome representante
    CB7_DTEMIS  = models.CharField(max_length=50)                    # Campo data emissão
    CB7_HREMIS  = models.CharField(max_length=5)                     # Campo hora emissão
    CB7_DTINIS  = models.CharField(max_length=50)                    # Campo data inicio
    CB7_HRINIS  = models.CharField(max_length=5)                     # Campo hora inicio
    CB7_DTFIMS  = models.CharField(max_length=50)                    # Campo data fim 
    CB7_HRFIMS  = models.CharField(max_length=5)                     # Campo hora fim
    CB7_NOTA    = models.CharField(max_length=50)                    # Campo código da nota                                  * primarykey
    CB7_SERIE   = models.CharField(max_length=50)                    # Campo serie ' 1 '                                     * primarykey
    CB8_PROD    = models.CharField(max_length=50)                    # Campo codigo de produção
    B1_DESC     = models.CharField(max_length=50)                    # Campo descrição produto
    LINE        = models.IntegerField(default=0)    