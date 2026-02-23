import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

BASE_URL = "http://localhost:3000"
DELAY_CURTO = 3.0
DELAY_MEDIO = 4.0
DELAY_LONGO = 5.0

random_id = int(time.time())
EMAIL_CLIENTE = f"cliente_{random_id}@teste.com"
CPF_CLIENTE = str(random_id)[:11].ljust(11, '0') 

PLACA_VEICULO = f"TES-{random_id}"[-8:]
CNH_VEICULO = str(random_id)[:11].ljust(11, '0')

EMAIL_EMPRESA = f"empresa_{random_id}@corp.com"
CNPJ_EMPRESA = str(random_id + 1)[:14].ljust(14, '0')

def iniciar_driver():
    print(" Iniciando Firefox...")
    options = webdriver.FirefoxOptions()
    service = Service()
    try:
        driver = webdriver.Firefox(service=service, options=options)
        driver.set_window_size(1366, 768)
        return driver
    except Exception as e:
        print(f"Erro ao iniciar Firefox: {e}")
        exit(1)

def esperar_e_clicar(driver, xpath):
    time.sleep(DELAY_CURTO)
    elemento = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", elemento)
    time.sleep(0.5)
    elemento.click()

def esperar_e_digitar(driver, xpath, texto):
    time.sleep(0.5)
    elemento = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )
    elemento.clear()
    elemento.send_keys(texto)

def passo(nome):
    print(f"\n🔹 {nome}...")
    time.sleep(DELAY_CURTO)

def fluxo_criar_reserva(driver, data_ini, data_fim):
    driver.get(f"{BASE_URL}/reservas/nova")
    time.sleep(DELAY_MEDIO)
    
    btns_escolher = driver.find_elements(By.XPATH, "//button[contains(text(), 'Escolher')]")
    if btns_escolher:
        btns_escolher[0].click()
    else:
        print(" Erro: Nenhum carro disponível!")
        exit()

    time.sleep(DELAY_CURTO)
    inputs_data = driver.find_elements(By.XPATH, "//input[@type='datetime-local']")
    inputs_data[0].send_keys(data_ini)
    inputs_data[1].send_keys(data_fim)
    
    esperar_e_clicar(driver, "//button[contains(., 'Simular e Continuar')]")
    time.sleep(DELAY_MEDIO)
    esperar_e_clicar(driver, "//button[contains(., 'CONFIRMAR RESERVA')]")
    time.sleep(DELAY_MEDIO)

driver = iniciar_driver()

try:
    # ==================================================================================
    # CENÁRIO 1: ADMIN PREPARA O VEÍCULO
    # ==================================================================================
    passo("1. [ADMIN] Acessando Login")
    driver.get(f"{BASE_URL}/admin/login")
    
    passo("2. [ADMIN] Fazendo Login")
    esperar_e_digitar(driver, "//input[@name='email']", "admin@frotanext.com")
    esperar_e_digitar(driver, "//input[@name='password']", "admin123")
    esperar_e_clicar(driver, "//button[contains(text(), 'ACESSAR SISTEMA')]")
    
    passo("3. [ADMIN] Cadastrando Veículo")
    time.sleep(DELAY_MEDIO)
    driver.get(f"{BASE_URL}/admin/veiculos")
    esperar_e_clicar(driver, "//button[contains(., 'Adicionar Novo Veículo')]")
    
    esperar_e_digitar(driver, "//input[@name='placa']", PLACA_VEICULO)
    esperar_e_digitar(driver, "//input[@name='chassi']", f"CHASSI{random_id}")
    esperar_e_digitar(driver, "//input[@name='marca']", "Tesla")
    esperar_e_digitar(driver, "//input[@name='modelo']", "Model S Plaid")
    esperar_e_digitar(driver, "//input[@name='valor_diaria']", "800")
    esperar_e_digitar(driver, "//input[@name='ano_fabricacao']", "2024")
    esperar_e_digitar(driver, "//input[@name='ano_modelo']", "2024")
    esperar_e_digitar(driver, "//input[@name='capacidade_tanque']", "100")
    
    select_cor = Select(driver.find_element(By.NAME, "cor"))
    select_cor.select_by_visible_text("Preto")
    
    esperar_e_clicar(driver, "//button[contains(., 'Cadastrar Veículo')]")
    time.sleep(DELAY_MEDIO)
    driver.refresh() 
    esperar_e_clicar(driver, "//button[contains(., 'Sair')]")

    # ==================================================================================
    # CENÁRIO 2: CLIENTE PF - CADASTRO, RESERVA, MODIFICAÇÃO E CANCELAMENTO
    # ==================================================================================
    passo("4. [PF] Cadastro de Cliente")
    driver.get(f"{BASE_URL}/cadastro")
    
    esperar_e_digitar(driver, "//input[@name='nome']", "Cliente Teste")
    esperar_e_digitar(driver, "//input[@name='documento']", CPF_CLIENTE)
    esperar_e_digitar(driver, "//input[@name='email']", EMAIL_CLIENTE)
    esperar_e_digitar(driver, "//input[@name='senha']", "senha123")
    esperar_e_digitar(driver, "//input[@name='telefone']", "11999999999")
    esperar_e_digitar(driver, "//input[@name='cnh']", CNH_VEICULO)

    esperar_e_digitar(driver, "//input[@name='cep']", "01001000")
    esperar_e_digitar(driver, "//input[@name='rua']", "Av Paulista")
    esperar_e_digitar(driver, "//input[@name='numero']", "1000")
    esperar_e_digitar(driver, "//input[@name='bairro']", "Bela Vista")
    esperar_e_digitar(driver, "//input[@name='cidade']", "São Paulo")
    esperar_e_digitar(driver, "//input[@name='estado']", "SP")
    
    esperar_e_clicar(driver, "//button[contains(text(), 'CADASTRAR')]")
    
    passo("5. [PF] Login")
    time.sleep(DELAY_MEDIO)
    esperar_e_digitar(driver, "//input[@name='email']", EMAIL_CLIENTE)
    esperar_e_digitar(driver, "//input[@name='password']", "senha123")
    esperar_e_clicar(driver, "//button[contains(text(), 'ENTRAR')]")
    time.sleep(DELAY_MEDIO)


    passo("6. [PF] Criando Reserva Inicial (Para Cancelar)")
    fluxo_criar_reserva(driver, "2025-12-20T09:00", "2025-12-25T18:00")
    
    passo("7. [PF] Modificando a Reserva")
    esperar_e_clicar(driver, "//button[contains(., 'Modificar Reserva')]")
    
    time.sleep(DELAY_CURTO)

    esperar_e_clicar(driver, "//input[@type='checkbox']")
    
    esperar_e_clicar(driver, "//button[contains(., 'Salvar Alterações')]")
    
    time.sleep(DELAY_MEDIO)
    try:
        driver.find_element(By.XPATH, "//button[contains(text(), 'OK, Entendi')]").click()
    except:
        pass 
    
    passo("8. [PF] Cancelando a Reserva Modificada")
    driver.refresh()
    time.sleep(DELAY_CURTO)
    esperar_e_clicar(driver, "//button[contains(., 'Cancelar')]")
    
    time.sleep(DELAY_CURTO)
    esperar_e_clicar(driver, "//button[contains(., 'Sim, Cancelar')]")
    time.sleep(DELAY_MEDIO)

    
    passo("9. [PF] Criando Reserva Definitiva (Para o Admin)")
    fluxo_criar_reserva(driver, "2025-12-20T09:00", "2025-12-25T18:00")
    
    passo("10. [PF] Logout")
    esperar_e_clicar(driver, "//button[contains(., 'Sair')]")

    # ==================================================================================
    # CENÁRIO 3: ADMIN APROVA E ENTREGA
    # ==================================================================================
    passo("11. [ADMIN] Login Admin")
    driver.get(f"{BASE_URL}/admin/login")
    esperar_e_digitar(driver, "//input[@name='email']", "admin@frotanext.com")
    esperar_e_digitar(driver, "//input[@name='password']", "admin123")
    esperar_e_clicar(driver, "//button[contains(text(), 'ACESSAR SISTEMA')]")

    passo("12. [ADMIN] Gestão de Reservas")
    driver.get(f"{BASE_URL}/admin/reservas")
    
    passo("13. [ADMIN] Aprovando Reserva")
    esperar_e_clicar(driver, "//button[@title='Aprovar Reserva']")
    time.sleep(DELAY_MEDIO)
    try: driver.find_element(By.XPATH, "//button[contains(text(), 'OK, Entendi')]").click()
    except: pass
    
    passo("14. [ADMIN] Entregando Veículo")
    driver.refresh()
    time.sleep(DELAY_CURTO)
    esperar_e_clicar(driver, "//button[@title='Registrar Retirada (Entregar Chaves)']")
    time.sleep(DELAY_MEDIO)
    try: driver.find_element(By.XPATH, "//button[contains(text(), 'OK, Entendi')]").click()
    except: pass

    passo("15. [ADMIN] Recebendo Veículo (Devolução)")
    driver.refresh()
    time.sleep(DELAY_CURTO)
    esperar_e_clicar(driver, "//button[@title='Registrar Devolução']")
    time.sleep(DELAY_CURTO)
    esperar_e_clicar(driver, "//button[contains(., 'Confirmar Devolução')]")
    time.sleep(DELAY_MEDIO)
    try: driver.find_element(By.XPATH, "//button[contains(text(), 'OK, Entendi')]").click()
    except: pass

    # ==================================================================================
    # CENÁRIO 4: ADMIN LIMPA (DELETE VEÍCULO)
    # ==================================================================================
    passo("16. [ADMIN] Excluindo Veículo")
    driver.get(f"{BASE_URL}/admin/veiculos")
    time.sleep(DELAY_MEDIO) # Espera a tabela carregar
    
    # 1. TENTA BUSCAR (Usa um seletor mais genérico para o input de busca)
    try:
        search_input = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Buscar')]")
        search_input.clear()
        search_input.send_keys(PLACA_VEICULO)
        time.sleep(2) # Espera filtrar
    except Exception as e:
        print(f"⚠️ Aviso: Não foi possível filtrar ({e}), tentando achar na lista visível...")

    # 2. TENTA CLICAR NA LIXEIRA (Busca por Title OU pelo ícone SVG de lixeira)
    btns_lixeira = driver.find_elements(By.XPATH, "//button[@title='Excluir'] | //button[descendant::*[local-name()='svg' and contains(@class, 'lucide-trash')]]")
    
    if btns_lixeira:
        print("   🗑️ Botão de excluir encontrado, clicando...")
        btns_lixeira[0].click()
        time.sleep(DELAY_CURTO)
        
        # 3. CONFIRMA NO MODAL (Procura qualquer botão vermelho de confirmação)
        try:
            # Tenta clicar no botão de "Sim/Confirmar" (geralmente é vermelho/bg-red)
            esperar_e_clicar(driver, "//button[contains(@class, 'bg-red') or contains(., 'Sim') or contains(., 'Excluir')]")
            time.sleep(DELAY_MEDIO)
            
            # Fecha modal de sucesso se aparecer
            try: driver.find_element(By.XPATH, "//button[contains(text(), 'OK') or contains(text(), 'Entendi')]").click()
            except: pass
            
        except Exception as e:
            print(f"   ❌ Erro ao confirmar exclusão: {e}")
            
    else:
        print("   ⚠️ Nenhum botão de excluir encontrado para este veículo.")
    
    # Logout final
    driver.refresh()
    time.sleep(DELAY_CURTO)
    esperar_e_clicar(driver, "//button[contains(., 'Sair')]")

    print("\n✅ TESTE DE JORNADA COMPLETA (INC. MODIFICAÇÃO) CONCLUÍDO!")

    # ==================================================================================
    # CENÁRIO 5: PJ E MOTORISTAS
    # ==================================================================================
    passo("17. [PJ] Cadastro de Empresa")
    driver.get(f"{BASE_URL}/cadastro")
    esperar_e_clicar(driver, "//button[contains(text(), 'Pessoa Jurídica')]")
    
    esperar_e_digitar(driver, "//input[@name='nome']", "Tech Solutions LTDA")
    esperar_e_digitar(driver, "//input[@name='documento']", CNPJ_EMPRESA)
    esperar_e_digitar(driver, "//input[@name='email']", EMAIL_EMPRESA)
    esperar_e_digitar(driver, "//input[@name='senha']", "senha123")
    esperar_e_digitar(driver, "//input[@name='telefone']", "1133334444")
    
    esperar_e_digitar(driver, "//input[@name='cep']", "04571000")
    esperar_e_digitar(driver, "//input[@name='rua']", "Av Berrini")
    esperar_e_digitar(driver, "//input[@name='numero']", "500")
    esperar_e_digitar(driver, "//input[@name='bairro']", "Brooklin")
    esperar_e_digitar(driver, "//input[@name='cidade']", "São Paulo")
    esperar_e_digitar(driver, "//input[@name='estado']", "SP")
    
    esperar_e_clicar(driver, "//button[contains(text(), 'CADASTRAR')]")

    passo("18. [PJ] Login da Empresa")
    time.sleep(DELAY_MEDIO)
    esperar_e_digitar(driver, "//input[@name='email']", EMAIL_EMPRESA)
    esperar_e_digitar(driver, "//input[@name='password']", "senha123")
    esperar_e_clicar(driver, "//button[contains(text(), 'ENTRAR')]")
    
    passo("19. [PJ] Vinculando Motorista (o Cliente PF)")
    time.sleep(DELAY_MEDIO)
    driver.get(f"{BASE_URL}/empresa/motoristas") 
    
    esperar_e_digitar(driver, "//input[@placeholder='Digite o CPF do motorista (apenas números)']", CPF_CLIENTE)
    esperar_e_clicar(driver, "//button[contains(text(), 'ADICIONAR')]")
    
    time.sleep(DELAY_MEDIO)
    try: driver.find_element(By.XPATH, "//button[contains(text(), 'OK, Entendi')]").click()
    except: pass

    print("\n TESTE DE JORNADA COMPLETA (INC. MODIFICAÇÃO) CONCLUÍDO!")

except Exception as e:
    print(f"\n Erro durante o teste: {e}")
    driver.save_screenshot("erro_jornada.png")
finally:
    time.sleep(5)
    if 'driver' in locals():
        driver.quit()
