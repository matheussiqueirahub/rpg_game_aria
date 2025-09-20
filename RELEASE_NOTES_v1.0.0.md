# Aria v1.0.0

Principais mudanças
- Autenticação segura: cadastro, login e lockout após 5 tentativas (15 min).
- Senhas com PBKDF2 (SHA‑256, 200k iterações + salt por usuário).
- Personalização do personagem: nome, força, inteligência, agilidade (1–10), pele, cabelo (cor/estilo) e olhos.
- Preview em Canvas e nome exibido/atualizado em tempo real.
- Tema claro/escuro, tooltips, toasts e atalhos (Ctrl+S, Enter, Esc).
- Scripts de build e empacote (EXE + ZIP).

Como executar
- Via Python: `python -m Aria.main`
- Executável Windows: `dist/Aria.exe`

Notas
- Banco de dados local (SQLite) em `Aria/aria.db`.
- Consultas parametrizadas e migração leve automática.
- Requisitos de senha: mínimo 8 caracteres, com maiúscula, minúscula e número.

Agradecimentos
- Projeto desenvolvido com foco em simplicidade, segurança e UX.
