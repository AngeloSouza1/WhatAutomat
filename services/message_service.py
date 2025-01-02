import pywhatkit
import time
import pyautogui

def send_message(phone, message):
    """
    Envia uma mensagem individual via WhatsApp com automação para envio direto.
    Lida com erros de número inválido e foca no campo de entrada antes de enviar.
    """
    try:
        if not phone or not message:
            raise ValueError("Número de telefone e mensagem são obrigatórios!")

        print(f"Preparando envio de mensagem para {phone}:\n{message}")
        
        # Abre o WhatsApp Web com a mensagem
        pywhatkit.sendwhatmsg_instantly(
            phone_no=phone,
            message=message,
            wait_time=15  # Tempo para carregar o WhatsApp e preencher a mensagem
        )
        
        time.sleep(5)  # Aguarda para garantir que a página está pronta

        # Verifica se aparece a mensagem de número inválido
        print("Verificando se há mensagem de número inválido...")
        for _ in range(1):  # Tentativas para detectar o alerta
            try:
                invalid_popup_position = pyautogui.locateOnScreen('numero_invalido.png', confidence=0.8)
                if invalid_popup_position:
                    print(f"Número {phone} é inválido no WhatsApp. Fechando o alerta.")
                    pyautogui.click(invalid_popup_position)  # Clica no botão "OK"
                    return f"Número inválido: {phone}"
            except Exception as e:
                print(f"Erro ao verificar número inválido: {e}")
            time.sleep(2)  # Pausa entre tentativas

        # Foca no campo de entrada da mensagem
        print("Focando no campo de entrada...")
        pyautogui.click(x=1714, y=987)  # Ajuste as coordenadas conforme necessário
        time.sleep(1)  # Pequena pausa para garantir que o clique seja processado

        # Simula o envio pressionando "Enter"
        pyautogui.press("enter")
        print(f"Mensagem enviada com sucesso para {phone}")

        # Fecha a aba ativa do navegador
        close_active_tab()
        return f"Mensagem enviada com sucesso para {phone}"

    except Exception as e:
        print(f"Erro ao enviar mensagem para {phone}: {e}")
        return f"Erro ao enviar para {phone}: {e}"


def close_active_tab():
    """
    Fecha a aba ativa do navegador sem fechar o navegador inteiro.
    """
    try:
        time.sleep(2)  # Pausa para garantir o foco na aba do navegador
        pyautogui.hotkey("ctrl", "w")  # Fecha a aba ativa
        print("Aba ativa fechada com sucesso.")
    except Exception as e:
        print(f"Erro ao fechar a aba ativa: {e}")


def send_bulk_messages(contacts, message, delay=5):
    """
    Envia mensagens em lote para múltiplos contatos.

    Args:
        contacts (list): Lista de números de telefone no formato internacional.
        message (str): Mensagem a ser enviada.
        delay (int): Intervalo em segundos entre os envios para evitar bloqueios.
    """
    if not contacts or not message:
        raise ValueError("Contatos e mensagem são obrigatórios para envio em lote!")

    print("Iniciando envio em lote...")
    total_contacts = len(contacts)
    invalid_numbers = []

    for index, phone in enumerate(contacts, start=1):
        try:
            print(f"[{index}/{total_contacts}] Enviando mensagem para {phone}...")
            result = send_message(phone, message)
            print(result)
            
            # Verifica se o número foi considerado inválido
            if "inválido" in result:
                invalid_numbers.append(phone)

            # Aguarda antes de enviar a próxima mensagem
            if index < total_contacts:
                print(f"Aguardando {delay} segundos antes do próximo envio...")
                time.sleep(delay)
        
        except Exception as e:
            print(f"Erro ao enviar mensagem para {phone}: {e}")
            continue  # Continua para o próximo contato

    print("Envio em lote concluído.")
    if invalid_numbers:
        print("Os seguintes números foram considerados inválidos:")
        for number in invalid_numbers:
            print(f" - {number}")
