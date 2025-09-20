RPG Game Aria (Desktop)

Resumo
- Plataforma: Desktop (Python 3 + Tkinter)
- Armazenamento: SQLite local (arquivo `Aria/aria.db`)
- Segurança: PBKDF2 (SHA‑256 + salt + 200k iterações), bloqueio por tentativas
- UI: Telas de Login, Cadastro e Personalização com tema claro/escuro

Objetivo
O Aria permite que cada usuário crie uma conta, faça login e personalize seu personagem (atributos 1–10 e aparência), salvando tudo no perfil. O app é leve, 100% offline e pronto para empacotamento em executável.

Funcionalidades
- Contas de usuário com login e senha (cadastro, autenticação e bloqueio após tentativas).
- Senhas armazenadas com hash PBKDF2 + salt (sem plaintext).
- Personalização do personagem: nome, força, inteligência, agilidade, pele, cabelo (cor/estilo) e olhos.
- Preview no Canvas com nome, cabelo/olhos/pele.
- Botões de ação: Salvar, Resetar e Aleatorizar.
- Tema claro/escuro com toggle na barra superior.
- Atalhos: Ctrl+S (salvar), Esc (sair/voltar/limpar), Enter (submeter).

Arquitetura
- `Aria/main.py`: ponto de entrada, controle de janelas e tema.
- `Aria/database.py`: criação/migração leve do SQLite e operações de dados seguras.
- `Aria/security.py`: hashing/verificação de senhas (PBKDF2 + salt).
- `Aria/ui/*`: telas de login, cadastro e personalização, além de tema, toast e tooltip.
- `Aria/assets/`: ícone opcional `aria.ico` para o executável.

Instalação
1) Requisitos: Python 3.9+.
2) (Opcional) Ambiente virtual:
   - Windows PowerShell
     - `python -m venv .venv`
     - `./.venv/Scripts/Activate.ps1`
3) Dependências: não há dependências de runtime. Para empacotar, instale `pyinstaller` (dev).

Execução
- `python -m Aria.main`

Empacotamento (Windows)
- Instale: `pip install -r requirements-dev.txt` (ou `pip install pyinstaller`)
- Build: `pwsh Aria/build.ps1 -NoConsole` → gera `dist/Aria.exe`
- Zip final: `pwsh Aria/package.ps1` → gera `Aria_Package.zip` com TODO o projeto (código + executável + docs).

Banco de Dados
- SQLite local em `Aria/aria.db`.
- Tabelas: `users` (unique username, hash, tentativas/bloqueio) e `characters` (1–1 com usuário).
- Migração leve automática: adiciona colunas de segurança se necessário.

Segurança
- Hash PBKDF2 (SHA‑256, 200.000 iterações) com salt aleatório por senha.
- Consultas parametrizadas para evitar injeção.
- Bloqueio temporário após N tentativas (padrão: 5 falhas → 15 min).
- Política de senha: mínimo 8 caracteres, exige maiúscula, minúscula e número.

Qualidade e Organização
- Código modular e padronizado (nomes claros, separação por camadas).
- UI com foco em clareza, mensagens diretas e feedback sutis (toasts).
- Scripts de build/empacote incluídos.

Licença
- MIT (ver arquivo `LICENSE`).

Publicação no GitHub (sugestão)
1. Garanta que apenas os diretórios/arquivos do projeto Aria estejam versionados.
2. Adicione `.gitignore` (Python + PyInstaller) para evitar `dist/`, `build/`, `__pycache__/`, etc.
3. Commits curtos e objetivos (ex.: "feat(ui): tema claro/escuro", "feat(auth): lockout por tentativas").
4. Crie uma Release com o `Aria_Package.zip` anexado.
5. Descreva a release com highlights, requisitos e instruções de execução.

Nota de transparência
- Este repositório contém apenas a implementação e documentação técnica do aplicativo. Evite incluir declarações enganosas sobre o processo de desenvolvimento.
