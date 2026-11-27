"""Verify public pages, the current video and the API without creating contacts."""
import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def verify(base):
    checks = {
        '/': ['apresentacoes.html', 'colheita.html', 'universo-kaggriculture', 'PROJETO CENTRAL', 'Bernardo de Paula Carvalho', 'Menos tarefas manuais.'],
        '/colheita.html': ['Gerar plano de colheita', 'farm-form', 'Fazenda Horizonte', 'Semana da Colheita', 'daily-cards'],
        '/equipe.html': ['Colheita no Prazo', 'crew-form', 'equipe.js'],
        '/api/kaggriculture/status': ['kaggriculture-harvest-0.2.0', '"connected":true'],
        '/colheita-modelo.js': ['function compare(s)', 'validate(s)'],
        '/kaggriculture.html': ['colheita.html', 'deliverables', 'PROJETO CENTRAL', 'equipe.html', 'Possibilidades de desenvolvimento'],
        '/portfolio.html': ['apresentacoes.html#chef'],
        '/apresentacoes.html': ['media/cheflu-operacao-narrada.mp4', 'PSgtg2YDMK0'],
        '/kaggriculture-360.html': ['pointermove', 'ArrowRight'],
        '/galeria-3d.html': ['kaggriculture-360.html'],
        '/api/health': ['ekonomatica-api'],
    }
    failures = []
    for path, markers in checks.items():
        try:
            with urlopen(base + path, timeout=15) as response:
                content = response.read().decode('utf-8')
                if response.status != 200 or any(m not in content for m in markers):
                    raise ValueError('conteúdo publicado diferente do esperado')
                if path == '/api/health' and json.loads(content).get('status') != 'ok':
                    raise ValueError('API indisponível')
            print('OK', path)
        except (HTTPError, URLError, ValueError, OSError) as error:
            failures.append(path)
            print('FALHOU', path, type(error).__name__)
    path = '/media/cheflu-operacao-narrada.mp4'
    try:
        request = Request(base + path, headers={'Range': 'bytes=0-63'})
        with urlopen(request, timeout=20) as response:
            prefix = response.read(64)
            if response.status not in (200, 206) or b'ftyp' not in prefix:
                raise ValueError('arquivo de vídeo inválido')
        print('OK vídeo MP4')
    except (HTTPError, URLError, ValueError, OSError) as error:
        failures.append(path)
        print('FALHOU vídeo MP4', type(error).__name__)
    print('Esta checagem não confirma áudio percebido, entrega de contatos ou resposta generativa.')
    return not failures


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', default='https://ekonomatica.com.br')
    args = parser.parse_args()
    sys.exit(0 if verify(args.base.rstrip('/')) else 1)
