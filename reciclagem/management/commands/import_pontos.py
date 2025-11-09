from django.core.management.base import BaseCommand
from reciclagem.models import PontoColeta
import os

class Command(BaseCommand):
    help = 'Importa pontos de coleta a partir de data/pontos_coleta.txt'

    def handle(self, *args, **opts):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(file)))
        path = os.path.join(base_dir, 'data', 'pontos_coleta.txt')
        with open(path, encoding='utf-8') as f:
            for line in f:
                # supondo formato: Nome do Ponto – Endereço – Telefone
                parts = [p.strip() for p in line.split('–')]
                if len(parts) >= 2:
                    nome = parts[0]
                    endereco = parts[1]
                    telefone = parts[2] if len(parts) > 2 else ''
                    PontoColeta.objects.get_or_create(
                        nome=nome,
                        defaults={'endereco': endereco, 'telefone': telefone}
                    )
        self.stdout.write(self.style.SUCCESS('Importação concluída.'))