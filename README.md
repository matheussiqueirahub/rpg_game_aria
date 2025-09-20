Aria — Crie e personalize seu personagem no desktop

O Aria é um app de desktop simples e focado que permite criar uma conta, fazer login e personalizar o seu personagem com atributos (1–10) e aparência (pele, cabelo, olhos). Tudo fica salvo no seu perfil, localmente, de forma segura. É leve, roda offline e está pronto para ser enviado como executável.

Por dentro do Aria em 12 segundos
- ![Demo](docs/demo.gif)

Principais telas
- Login: ![Login](docs/preview-login.png)
- Cadastro: ![Cadastro](docs/preview-register.png)
- Personalização: ![Personalização](docs/preview-customize.png)

Destaques
- Login e cadastro com validações claras e mensagens objetivas.
- Senhas com hash PBKDF2 + salt (nunca armazenadas em texto).
- Lockout automático após 5 falhas (desbloqueio em 15 min).
- Customização completa: nome, força, inteligência, agilidade, pele, cabelo (cor/estilo) e olhos.
- Preview em Canvas, com nome atualizado em tempo real.
- Tema claro/escuro, tooltips, toasts e atalhos (Ctrl+S, Enter, Esc).

Baixar o executável (Windows)
- Release v1.0.0: https://github.com/matheussiqueirahub/rpg_game_aria/releases/tag/v1.0.0
- ZIP leve (< 10 MB): link direto para download
  - https://github.com/matheussiqueirahub/rpg_game_aria/releases/download/v1.0.0/Aria_Package_Lite.zip

Rodar pelo código (desenvolvimento)
- Requisitos: Python 3.9+
- Passos:
  - (Opcional) criar venv: `python -m venv .venv && ./.venv/Scripts/Activate.ps1`
  - Executar: `python -m Aria.main`

Como funciona (por cima)
- `Aria/main.py`:1 controla janelas (login/cadastro/personalização), tema e sessão.
- `Aria/database.py`:1 cria e acessa o SQLite local (`Aria/aria.db`) e aplica a migração leve.
- `Aria/security.py`:1 faz hash/verificação de senhas com PBKDF2 (200k iterações + salt).
- `Aria/ui/*`:1 telas e utilitários (tema, toast, tooltip).

Segurança em foco
- Hash PBKDF2 (SHA‑256, 200.000 iterações) com salt aleatório por senha.
- Consultas parametrizadas (evita injeção SQL).
- Lockout: 5 tentativas erradas → bloqueio por 15 minutos.
- Política de senha: mínimo 8 caracteres, com maiúscula, minúscula e número.

Banco de dados
- SQLite local (`Aria/aria.db`), fácil de backup (copie o arquivo).
- Tabelas:
  - `users`: usuário único, hash de senha, tentativas e bloqueio.
  - `characters`: ficha 1–1 por usuário.

Atalhos úteis
- Ctrl+S: salvar personagem
- Enter: submeter (login/cadastro)
- Esc: sair (personalização) / limpar (login) / voltar (cadastro)

Empacotamento
- Build do executável: `pwsh Aria/build.ps1 -NoConsole`
- ZIP completo (código + exe + docs): `pwsh Aria/package.ps1`
- ZIP leve (<10 MB, só exe + README + LICENSE): `pwsh Aria/package-lite.ps1`

Licença
- MIT — veja `LICENSE`:1

Links úteis (Release)
- ZIP completo: https://github.com/matheussiqueirahub/rpg_game_aria/releases/download/v1.0.0/Aria_Package.zip
- ZIP leve (<10 MB): https://github.com/matheussiqueirahub/rpg_game_aria/releases/download/v1.0.0/Aria_Package_Lite.zip
