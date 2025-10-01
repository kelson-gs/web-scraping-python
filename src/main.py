import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def tentar_clicar(driver, xpath, tentativas_max=3, delay=2):
    tentativas = 0
    while tentativas < tentativas_max:
        try:
            elemento = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            elemento.click()
            return True
        except (StaleElementReferenceException, ElementClickInterceptedException) as e:
            print(f"Erro ao clicar no elemento {xpath}: {e}")
            tentativas += 1
            time.sleep(delay)
    print(f"Falha ao clicar no elemento {xpath} após {tentativas_max} tentativas.")
    return False

def get_element_text(driver, element_id):
    """Tenta pegar o texto de um elemento. Se não encontrar, retorna uma string vazia."""
    try:
        element = driver.find_element(By.ID, element_id)
        print(f"Texto encontrado para {element_id}: {element.text}")
        return element.text.strip()
    except Exception as e:
        print(f"Erro ao tentar pegar o texto do elemento {element_id}: {e}") 
        return ""
 
name_zona ="AEROPORTO" 

# Configuração do Selenium
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--start-maximized")  

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get('https://geoembraesp.com.br/login.aspx')

# Login
username_input = driver.find_element(By.ID, "LoginViewHeader_LoginHeader_UserName")
password_input = driver.find_element(By.ID, "LoginViewHeader_LoginHeader_Password")

username_input.clear()
password_input.clear()
time.sleep(1)

username_input.send_keys("email")
time.sleep(1)
password_input.send_keys("senha")
time.sleep(1)
password_input.send_keys(Keys.RETURN)

time.sleep(10)

# Clicar no link do modal de imóveis
open_modal_imovel = driver.find_element(By.ID, "lnkMenuImoveis")
open_modal_imovel.click()
print("Clicando para abrir modal")
time.sleep(10)

# Esperar até o modal ser carregado e garantir que o título está visível
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="Filtro de Imóveis"]')))
print("Modal 'Filtro de Imóveis' aberto!")

# Preencher zona
zona_input = driver.find_element(By.ID, "txtZonaValorFiltro")
zona_input.send_keys(name_zona)
print("Inserindo informação no input")

time.sleep(10)
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "afont10Black")))

# Capturar elementos atualizados
zona_items = driver.find_elements(By.CLASS_NAME, "afont10Black")

# Filtrar e clicar no item correto
for item in zona_items:
    if name_zona in item.text.strip().upper():
        item.click()
        print("Clicando no item certo")
        break

# Aguardar a lista lateral ser atualizada
try:
    time.sleep(10)
    print("Aguardando a lista lateral ser atualizada...")
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "itemGridMenu")))
except TimeoutException:
    print("A lista lateral não carregou completamente dentro do tempo esperado.")

# Capturar os imóveis carregados
time.sleep(10)
lista_imoveis = driver.find_elements(By.CLASS_NAME, "itemGridMenu")
print(f"Total de imóveis carregados: {len(lista_imoveis)}")

dados_imoveis = []
for index, imovel in enumerate(lista_imoveis):
    print(f"Tentando clicar no imóvel {index + 1}: {imovel.text}")
    driver.execute_script("arguments[0].click();", imovel)
    print("Clique no imóvel bem-sucedido!")

    mais_detalhes = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "font12Blue"))
    )
    driver.execute_script("arguments[0].click();", mais_detalhes)
    print("Clique no botão 'Mais Detalhes' bem-sucedido!")

    WebDriverWait(driver, 5).until(lambda d: len(d.window_handles) > 1)
    abas = driver.window_handles
    driver.switch_to.window(abas[1])

    # atribuir os dados da ficha ao array 
    dados_imovel = {
        "nome_empreendimento": get_element_text(driver, "ContentPlaceHolderRootPage_lblGUNome"),
        "bloco": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblBlocos"),
        "unidades_andar": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblUnidadesAndar"),
        "andares": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblAndaresTipo"),
        "total_unidades": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblTotalUnidades"),
        "elevadores": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblElevadores"),
        "cobertura": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblCoberturas"),
        "dormitorios": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblDormitorios"),
        "banheiros_sociais": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblBanheiros"),
        "vagas_garagem": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblVagasGaragem"),
        "area_util": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblAreaUtil"),
        "area_total": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblAreaTotal"),
        "area_terreno": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblTotalTerreno"),
        "area_util_cobertura": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblAreaUtilCobertura"),
        "area_total_cobertura": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblAreaTotalCobertura"),
        "preco_total": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblPrecoUnidadeReais"),
        "preco_total_us": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblPrecoUnidadeDolar"),
        "preco_pm2_area_util": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblPrecoAreaUtilReais"),
        "preco_pm2_area_util_us": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblPrecoAreaUtilDolar"),
        "preco_pm2_area_total": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblPrecoAreaTotalReais"),
        "preco_pm2_area_total_us": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblPrecoAreaTotalDolar"),
        "preco_total_cobertura": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblPrecoCoberturaReais"),
        "preco_total_cobertura_us": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblPrecoCoberturaDolar"),
        "preco_valor_us": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblValorDolar"),
        "financiamento": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblFinanciamento"),
        "agente": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblAgente"),
        "incorporacao": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_rptParceirosIncorporadora_lblParceiro_0"),
        "construtora": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_rptParceirosConstrutora_Label5_0"),
        "vendas": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_rptParceirosVendas_Label6_0"),
        "engenharia": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_rptParceirosEngenharia_Label7_0"),
        "arquitetura": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_rptParceirosArquitetura_Label8_0"),
        "endereco": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_wucLocalizacaoList_lblLogradouro"),
        "bairro": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_wucLocalizacaoList_lblBairro"),
        "cidade": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_wucLocalizacaoList_lblCidadeUF"),
        "cep": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_wucLocalizacaoList_lblCEP"),
        "zona_de_valor": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_wucLocalizacaoList_lblZonaValor"),
        "zoneamento": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_wucLocalizacaoList_lblZona"),
        "setor": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_wucLocalizacaoList_lblSetor"),
        "quadra": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_wucLocalizacaoList_lblQuadra"),
        "lote": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_wucLocalizacaoList_lblLote"),
        "latitude": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_wucLocalizacaoList_lblLatitude"),
        "longitude": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_wucLocalizacaoList_lblLongitude")
    }

    # Adicionando o imóvel na lista
    dados_imoveis.append(dados_imovel)

    # print(f"Dados da Ficha A coletados: {dados_imoveis}")

    fichas_coletadas = {"Ficha A"}
    fases_coletadas = {"1ª FASE"}
    max_tentativas = 3 

    while True:
        print("Entrando no loop para coletar fichas e fases.")
        
        # Primeiro, coleta as fichas da fase atual
        try:
            fichas = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="MenuGUFichas"]//ul//li//a'))
            )
        except:
            fichas = []
        
        fichas_disponiveis = [f.text.strip() for f in fichas if f.text.strip() not in fichas_coletadas]
        
        for ficha_texto in fichas_disponiveis:
            if tentar_clicar(driver, f'//div[@class="MenuGUFichas"]//ul//li//a[text()="{ficha_texto}"]'):
                fichas_coletadas.add(ficha_texto)
                # WebDriverWait(driver, 30).until(
                #     EC.presence_of_element_located((By.ID, "ContentPlaceHolderRootPage_lblGUNome"))
                # )
                time.sleep(1)
                
                dados_imovel = {
                    "nome_empreendimento": get_element_text(driver, "ContentPlaceHolderRootPage_lblGUNome"),
                    "area_util_cobertura": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblAreaUtilCobertura"),
                    "area_total_cobertura": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_lblAreaTotalCobertura"),
                    "endereco": get_element_text(driver, "ContentPlaceHolderRootPage_ContentPlaceHolderGUPage_wucLocalizacaoList_lblLogradouro"),
                }
                dados_imoveis.append(dados_imovel)
                print(f"Dados da {ficha_texto} coletados com sucesso.")
        
        # Obter a lista de fases
        try:
            fases = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="MenuGUFases"]//ul//li//a'))
            )
        except:
            print("Nenhuma fase encontrada.")
            fases = []
        
        fases_disponiveis = [f.text.strip() for f in fases if f.text.strip() not in fases_coletadas]
        
        if not fichas_disponiveis and not fases_disponiveis:
            print("Todas as fichas e fases já foram coletadas! Encerrando...")
            break
        
        try:
            fase_atual = driver.find_element(By.XPATH, '//div[@class="fase-atual"]').text.strip()
        except:
            fase_atual = None 
        
        for fase_texto in fases_disponiveis:
            try:
                if fase_texto == fase_atual:
                    print(f"Já estamos na {fase_texto}, pulando clique.")
                    continue
                
                print(f"Indo para {fase_texto}...")
                xpath_fase = f'//div[@class="MenuGUFases"]//ul//li//a[text()="{fase_texto}"]'
                if tentar_clicar(driver, xpath_fase):
                    fases_coletadas.add(fase_texto)
                    WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "MenuGUFichas")]'))
                    )
            except:
                print(f"Fase {fase_texto} não encontrada, pulando.")
                continue

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

# Salvar os dados no CSV
fieldnames = set()
for item in dados_imoveis:
    fieldnames.update(item.keys()) 

fieldnames = list(fieldnames)

print(f"Dados_imoveis: {len(dados_imoveis)}")
# Salva os dados no CSV
if dados_imoveis:
    with open(f"{name_zona}.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dados_imoveis)
    print("Dados salvos em imoveis.csv")

print("Processo finalizado!")
driver.quit()