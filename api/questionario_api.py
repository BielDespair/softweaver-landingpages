#!/usr/bin/env python3
"""API do questionário: recebe o POST e grava uma linha por resposta em /data/respostas.jsonl."""

import json
import os
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ARQUIVO = "/data/respostas.jsonl"
MAX_BYTES = 64 * 1024

COLUNAS = [
    "auto_cuidado", "cor_favorita", "cronograma_capilar", "produtos_mais_usados", "skin_care",
    "depilacao_laser", "tatuagem", "cor_do_cabelo", "usa_volume_russo", "tamanho_unha_postiça",
    "bronze", "hobbies_favoritos", "estilo_musical_favorito", "cantora_favorita", "youtuber_favorito",
    "bebe", "fuma", "usa_drogas", "decote", "roupa_apertada", "perfume_favorito", "livro_favorito",
    "atividade_fisica", "frequenta_igreja",
    # Estética
    "estilo_de_roupa", "tipo_de_maquiagem", "usa_delineador", "usa_batom", "usa_acessorios",
    "acessorio_favorito", "tipo_de_sapato", "usa_salto", "usa_bota",
    # Música / entretenimento
    "filme_favorito", "serie_favorita", "jogo_favorito", "artista_favorito",
    "frequenta_shows", "frequenta_festivais", "frequenta_baladas",
    # Hobbies
    "atividade_de_fim_de_semana", "tipo_de_viagem", "gosta_de_fotografia", "gosta_de_dancar",
    "gosta_de_cozinhar", "gosta_de_ler",
    # Estilo de vida
    "tipo_de_restaurante_favorito", "bebida_favorita", "cafe_ou_cha", "animal_favorito", "pet",
]

trava = threading.Lock()


class Handler(BaseHTTPRequestHandler):
    def _json(self, status, obj):
        corpo = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_POST(self):
        if self.path != "/api/questionario/respostas":
            return self._json(404, {"erro": "não encontrado"})

        try:
            tamanho = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            tamanho = 0
        if not 0 < tamanho <= MAX_BYTES:
            return self._json(413, {"erro": "tamanho inválido"})

        try:
            dados = json.loads(self.rfile.read(tamanho))
        except ValueError:
            return self._json(400, {"erro": "JSON inválido"})
        if not isinstance(dados, dict) or set(dados) != set(COLUNAS):
            return self._json(422, {"erro": "colunas não batem com o questionário"})

        registro = {"recebido_em": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        registro.update((c, dados[c]) for c in COLUNAS)

        with trava, open(ARQUIVO, "a", encoding="utf-8") as f:
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")

        self._json(201, {"ok": True})


if __name__ == "__main__":
    os.makedirs(os.path.dirname(ARQUIVO), exist_ok=True)
    print("questionario-api ouvindo em 127.0.0.1:8000", flush=True)
    ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()