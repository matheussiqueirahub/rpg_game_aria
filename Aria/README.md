Aria — Programa de Personalização de Personagens (Desktop)

Resumo
- Nome do jogo: Aria
- Plataforma: Desktop (Windows/macOS/Linux via Python + Tkinter)
- Armazenamento: SQLite local (arquivo `aria.db`)
- Segurança: Hash de senha com PBKDF2 (SHA-256 + salt + iterações)
- UI: Tkinter (login, registro e personalização de personagem)

Funcionalidades
- Registro e login com validações e mensagens de erro claras.
- Senhas armazenadas de forma segura (PBKDF2; sem armazenar senhas em texto).
- Personalização do personagem: nome, força, inteligência, agilidade, cor da pele, cabelo (cor e estilo) e olhos.
- Escalas 1–10 para atributos numéricos.
- Salvamento/edição persistente por usuário.
- Pré-visualização do personagem via Canvas (face/cabelo/olhos/pele) com nome exibido.
- Ações rápidas: Resetar e Aleatorizar.
- Tema claro/escuro com toggle no topo.

Requisitos
- Python 3.9+ (Tkinter incluído por padrão)
- Windows: recomendado executar em venv

Instalação e Execução
1) (Opcional) Criar e ativar venv
   - Windows PowerShell:
     - `python -m venv .venv`
     - `./.venv/Scripts/Activate.ps1`
2) Instalar dependências (não há dependências externas obrigatórias)
3) Rodar o app
   - `python -m Aria.main`

Geração de Executável (Windows)
- Requer: `pip install pyinstaller`
- Comando:
  - `pyinstaller --onefile --noconsole --name Aria --icon Aria/assets/aria.ico Aria/main.py`
- O executável será gerado em `dist/Aria.exe`.

Estrutura
- `Aria/main.py` — ponto de entrada da aplicação (janela Tk e navegação entre telas)
- `Aria/database.py` — criação e acesso ao banco SQLite
- `Aria/security.py` — hash/validação de senhas (PBKDF2)
- `Aria/ui/login_frame.py` — tela de login
- `Aria/ui/register_frame.py` — tela de registro
- `Aria/ui/character_frame.py` — tela de personalização do personagem
- `Aria/assets/` — ícone e futuros assets

Notas de Segurança
- PBKDF2 com 200.000 iterações e salt aleatório de 16 bytes.
- Uso de consultas parametrizadas no SQLite para evitar injeção.
- Lockout: após 5 tentativas falhas, bloqueio de 15 min.
- Política de senha: mínimo de 8 caracteres, com maiúscula, minúscula e número.

Tema e Paleta
- Paleta inspirada no projeto `paleta_de_cores_aria` (primária, secundária e acento).
- Toggle “Modo Escuro/Modo Claro” disponível na barra superior.

Backup e Migração
- O banco está em `Aria/aria.db`. Faça backup desse arquivo para salvar usuários e personagens.

Licença
- Uso privado do cliente CB Games.
