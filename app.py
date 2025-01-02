from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, Client, ScheduledMessage
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
import pywhatkit
import time
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from services.message_service import send_message, send_bulk_messages
from pyvirtualdisplay import Display
import pyautogui

# Configuração do Flask
app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "instance", "whatsapp.db")}'
app.config['SECRET_KEY'] = 'your_secret_key'

# Inicializa o banco de dados e o agendador
db.init_app(app)
migrate = Migrate(app, db)  # Adiciona suporte ao Flask-Migrate
scheduler = BackgroundScheduler()
scheduler.start()

# Cria as tabelas ao iniciar o aplicativo
with app.app_context():
    db.create_all()

# Inicializa o display virtual
display = Display(visible=0, size=(1024, 768))
display.start()

# Rota principal
@app.route('/')
def dashboard():
    # Obter clientes em ordem alfabética
    clients = Client.query.order_by(Client.name.asc()).all()
    # Obter mensagens agendadas em ordem decrescente
    messages = ScheduledMessage.query.order_by(ScheduledMessage.schedule_time.desc()).all()
    return render_template('dashboard.html', clients=clients, messages=messages)


# Rota para adicionar cliente
@app.route('/add-client', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')

        if not name or not phone:
            flash("Todos os campos são obrigatórios!", "danger")
            return redirect(url_for('add_client'))

        # Verificar se o formato do telefone é válido
        if not phone.startswith('+55') or len(phone) != 14 or not phone[1:].isdigit():
            flash("O telefone deve estar no formato internacional brasileiro (+55 seguido de 11 dígitos).", "danger")
            return redirect(url_for('add_client'))

        client = Client(name=name, phone=phone)

        try:
            db.session.add(client)
            db.session.commit()
            flash("Cliente adicionado com sucesso!", "success")
        except IntegrityError:
            db.session.rollback()  # Reverte a transação em caso de erro
            flash(f"Erro: O telefone {phone} já está cadastrado!", "danger")
            return redirect(url_for('add_client'))

        return redirect(url_for('add_client'))

    # Recuperar todos os clientes cadastrados para exibição na tabela
    clients = Client.query.order_by(Client.name.asc()).all()
    return render_template('add_client.html', clients=clients)

@app.route('/edit-client/<int:client_id>', methods=['GET', 'POST'])
def edit_client(client_id):
    client = Client.query.get_or_404(client_id)

    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')

        if not name or not phone:
            flash("Todos os campos são obrigatórios!", "danger")
            return redirect(url_for('add_client'))
, methods=['GET', 'POST'])
def send_messages():
    if r
        # Validação do telefone
        if not phone.startswith('+55') or len(phone) != 14 or not phone[1:].isdigit():
            flash("O telefone deve estar no formato internacional brasileiro (+55 seguido de 11 dígitos).", "danger")
            return redirect(url_for('add_client'))

        client.name = name
        client.phone = phone

        try:
            db.session.commit()
            flash("Cliente atualizado com sucesso!", "success")
        except IntegrityError:
            db.session.rollback()
            flash(f"Erro: O telefone {phone} já está cadastrado!", "danger")

        return redirect(url_for('add_client'))

    return render_template('edit_client.html', client=client)



@app.route('/delete-client/<int:client_id>', methods=['POST'])
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)

    try:
        db.session.delete(client)
        db.session.commit()
        flash("Cliente excluído com sucesso!", "success")
    except Exception as e:
        flash(f"Erro ao excluir cliente: {str(e)}", "danger")

    return redirect(url_for('add_client'))




# Rota para enviar mensagem individual
@app.route('/send-messages', methods=['GET', 'POST'])
def send_messages():
    if request.method == 'POST':
        contact_id = request.form.get('contact')
        message = request.form.get('message')

        if not contact_id or not message:
            flash("Todos os campos são obrigatórios!", "danger")
            return redirect(url_for('send_messages'))

        client = Client.query.get(contact_id)
        if not client:
            flash("Cliente não encontrado!", "danger")
            return redirect(url_for('send_messages'))

        try:
            send_message(client.phone, message)
            flash(f"Mensagem enviada para {client.name} com sucesso!", "success")
        except Exception as e:
            flash(f"Erro ao enviar mensagem: {str(e)}", "danger")

        return redirect(url_for('dashboard'))

    clients = Client.query.order_by(Client.name.asc()).all()
    return render_template('send_message.html', clients=clients)


# Rota para agendar mensagens em lote
@app.route('/schedule-messages', methods=['GET', 'POST'])
def schedule_messages():
    if request.method == 'POST':
        contact_ids = request.form.getlist('contacts')
        message = request.form.get('message')
        schedule_time = request.form.get('schedule_time')

        if not contact_ids or not message or not schedule_time:
            flash("Todos os campos são obrigatórios!", "danger")
            return redirect(url_for('schedule_messages'))

        try:
            schedule_time = datetime.strptime(schedule_time, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash("Formato de data/hora inválido! Use o seletor de data/hora corretamente.", "danger")
            return redirect(url_for('schedule_messages'))

        contacts = [client.phone for client in Client.query.filter(Client.id.in_(contact_ids)).all()]

        for contact_id in contact_ids:
            scheduled_message = ScheduledMessage(
                client_id=contact_id,
                message=message,
                schedule_time=schedule_time
            )
            db.session.add(scheduled_message)

        db.session.commit()

        try:
            scheduler.add_job(
                func=send_bulk_messages,
                trigger='date',
                run_date=schedule_time,
                args=(contacts, message)
            )
            flash(f"Mensagens agendadas para {schedule_time}!", "success")
        except Exception as e:
            flash(f"Erro ao agendar mensagens: {str(e)}", "danger")

        return redirect(url_for('dashboard'))

    clients = Client.query.order_by(Client.name.asc()).all()
    return render_template('schedule_messages.html', clients=clients)


# Finaliza o display virtual ao sair da aplicação
import atexit
atexit.register(display.stop)


if __name__ == '__main__':
    app.run(debug=True)
