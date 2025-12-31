# 🔐 Password Generator Pro

![Python](https://img.shields.io/badge/Python-3.14-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Gerador profissional de senhas com interface gráfica moderna, armazenamento criptografado e análise de força.

## ✨ Características

- 🎲 **Geração de senhas personalizadas** - Controle comprimento, tipos de caracteres e exclusão de ambíguos
- 💾 **Armazenamento seguro** - Senhas salvas com criptografia Fernet
- 📊 **Análise de força** - Verificação detalhada com estimativa de tempo para quebrar
- 📋 **Copiar com um clique** - Integração com clipboard
- 📜 **Histórico completo** - Organize e categorize suas senhas
- 🎨 **Interface moderna** - Dark theme profissional

## 📸 Screenshots

### Gerador de Senhas
- Configuração flexível de comprimento (8-64 caracteres)
- Opções para maiúsculas, minúsculas, números e símbolos
- Visualização de força em tempo real

### Histórico
- Lista de todas as senhas salvas
- Detalhes completos (data de criação, categoria, força)
- Operações: visualizar, copiar, deletar

### Análise de Força
- Análise detalhada de composição
- Cálculo de combinações possíveis
- Estimativa de tempo para quebrar (força bruta)
- Recomendações personalizadas

## 🚀 Instalação

### Pré-requisitos
- Python 3.14

### Passos

1. Clone o repositório:
```bash
git clone https://github.com/garotinha666/password-generator-pro.git
cd password-generator-pro
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o aplicativo:
```bash
python main.py
```

## 📦 Dependências

- **cryptography** - Criptografia das senhas salvas
- **pyperclip** - Copiar para área de transferência

## 🎯 Como Usar

### Gerando uma Senha

1. Na aba **"⚡ Gerar Senha"**, ajuste o comprimento desejado (8-64 caracteres)
2. Selecione os tipos de caracteres:
   - ✅ Maiúsculas (A-Z)
   - ✅ Minúsculas (a-z)
   - ✅ Números (0-9)
   - ✅ Símbolos (!@#$%)
3. Opcionalmente, exclua caracteres ambíguos (0, O, l, 1)
4. Clique em **"🎲 Gerar Senha"**
5. Use **"📋 Copiar"** para copiar ou **"💾 Salvar"** para armazenar

### Salvando Senhas

1. Após gerar uma senha, clique em **"💾 Salvar"**
2. Digite um nome/descrição (ex: "Gmail", "Banco XYZ")
3. Opcionalmente, adicione uma categoria (ex: "Emails", "Bancos")
4. As senhas são criptografadas automaticamente

### Visualizando Histórico

1. Vá para a aba **"📜 Histórico"**
2. Selecione uma senha da lista
3. Veja os detalhes no painel inferior
4. Use **"👁️ Ver Senha"** para revelar
5. Use **"📋 Copiar Senha"** para copiar
6. Use **"🗑️ Deletar"** para remover

### Analisando Força

1. Vá para a aba **"💪 Analisar Força"**
2. Digite ou cole uma senha
3. Clique em **"🔍 Analisar"**
4. Veja análise detalhada:
   - Comprimento e composição
   - Força geral
   - Combinações possíveis
   - Tempo estimado para quebrar
   - Recomendações de melhoria

## 🔒 Segurança

- **Criptografia Fernet** (AES-128) para todas as senhas salvas
- Chave de criptografia armazenada localmente em `.key`
- Senhas nunca são enviadas pela internet
- Dados armazenados em `passwords.enc`

**⚠️ IMPORTANTE**: 
- Faça backup dos arquivos `.key` e `passwords.enc`
- Perder a chave significa perder acesso às senhas salvas
- Não compartilhe o arquivo `.key`

## 🎨 Personalização

O código é modular e fácil de personalizar:

```python
# Alterar cores (em setup_styles())
bg_dark = "#0f0f1e"
accent = "#0f4c75"

# Alterar comprimento padrão
self.length_var = tk.IntVar(value=16)

# Adicionar novos símbolos
chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abrir um Pull Request

## 📝 Ideias para Melhorias

- [ ] Importar/exportar senhas
- [ ] Geração de passphrases
- [ ] Integração com gerenciadores de senhas
- [ ] Verificação de senhas vazadas (Have I Been Pwned API)
- [ ] Senha mestra para proteger o aplicativo
- [ ] Modo portátil (sem instalação)
- [ ] Tema claro/escuro

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👤 Autor

Desenvolvido com ❤️ para ajudar você a manter suas contas seguras!

## ⚠️ Aviso

Este é um projeto educacional. Para uso profissional, considere gerenciadores de senha estabelecidos como Bitwarden, 1Password ou KeePass.

---

**Dica**: Para máxima segurança, use senhas de 16+ caracteres com todos os tipos de caracteres! 🔒