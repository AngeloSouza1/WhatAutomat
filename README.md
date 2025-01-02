# WhatsApp Automation Application

Este projeto foi criado para explorar o agendamento e envio automatizado de mensagens via WhatsApp. Ele combina várias tecnologias para oferecer uma experiência funcional, prática e com foco no aprendizado.

---

## 🚀 **Funcionalidades**
- **Cadastro de Clientes**: Adicione clientes com nome e número de telefone no formato internacional.
- **Envio de Mensagens Individuais**: Envie mensagens personalizadas para contatos cadastrados.
- **Agendamento de Mensagens**: Programe envios para uma data e horário específicos.
- **Envio em Lote**: Automatize o envio de mensagens para múltiplos contatos.
- **Interface Simples**: Interface web intuitiva para gerenciar clientes e agendamentos.

---

## 🛠️ **Tecnologias Utilizadas**
- **Back-end**: Flask (Python)
- **Banco de Dados**: SQLite com SQLAlchemy para gerenciamento de dados.
- **Mensageria**: PyWhatKit para integração com o WhatsApp.
- **Automação de Interface**: PyAutoGUI para interações simuladas.
- **Agendamento**: APScheduler para gerenciar tarefas agendadas.
- **Virtualização de Tela**: PyVirtualDisplay para compatibilidade em ambientes de deploy.

---

## 💻 **Instalação e Execução**

### **Pré-requisitos**
- Python 3.11+
- Git
- Ambiente virtual configurado (opcional)

### **Clone o Repositório**
```bash
git clone https://github.com/seu-usuario/whatsapp-automation.git
cd whatsapp-automation
```

### **Instale as Dependências**
Crie e ative o ambiente virtual (opcional):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

Instale as Dependências

```bash
pip install -r requirements.txt
```

### **Configure o Banco de Dados**

```bash
flask db init
flask db migrate -m "Inicializando banco"
flask db upgrade
```
### **Configure o Banco de Dados**

```bash
python app.py
```
Acesse a aplicação no navegador:

```bash
http://127.0.0.1:5000/
```

---

## 📷 **Preview**

### Dashboard

Uma visão geral dos clientes cadastrados e mensagens agendadas.

### Cadastro de Clientes

Interface para adicionar, editar e excluir clientes.

### Agendamento de Mensagens

Programe mensagens para envio futuro com horário definido.



https://github.com/user-attachments/assets/23c6e70f-d396-4999-92fa-4014609a4526



---

## 🧪 Testes e Melhorias

Este é um projeto de estudo, mas funcional. Estou aberto a feedbacks, ideias ou melhorias. 



## 📞 Contato

Se quiser trocar uma ideia ou colaborar, me encontre em:

    E-mail: angeloafdesouza@gmail.com
  















