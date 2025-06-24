from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import pandas as pd
from datetime import datetime
import os
from scraper import Scraper
from url_collector import URLCollector
from scraping_log import logger
import socketio
import uvicorn
from dotenv import load_dotenv
import io
import asyncio
from threading import Thread

# Carrega variáveis de ambiente
load_dotenv()

# Criando instância do Socket.IO
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

# Criando instância do FastAPI
app = FastAPI(
    title="API de Scraping de Dados Nutricionais",
    description="API para coletar e consultar dados nutricionais de produtos do Pão de Açúcar",
    version="1.0.0"
)

# Montando o Socket.IO com o FastAPI
socket_app = socketio.ASGIApp(sio, app)

# Configuração dos templates e arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class ProdutoBase(BaseModel):
    url: str
    nome: str
    categoria: Optional[str] = None

class DadoNutricional(ProdutoBase):
    porcao: float
    calorias: float
    carboidratos: float
    proteinas: float
    gorduras: float
    gorduras_saturadas: float
    fibras: float
    acucares: float
    sodio: float
    data_coleta: Optional[str] = None

class URLCategoria(BaseModel):
    url: str
    nome: Optional[str] = None
    modo_teste: Optional[bool] = False

class ColetaRequest(BaseModel):
    modo: str
    categorias: List[str]

# Variável global para controlar o estado da coleta
coleta_ativa = False
scraper_instance = None

def get_system_metrics():
    """Obtém as métricas do sistema"""
    # TODO: Implementar lógica real de métricas
    return {
        "total_produtos": 0,  # Será atualizado com dados reais
        "total_categorias": 0,  # Será atualizado com dados reais
        "ultima_atualizacao": "Nenhuma coleta realizada"
    }

def get_system_status():
    """Obtém o status atual do sistema"""
    # TODO: Implementar lógica real de status
    return {
        "ultima_execucao": "Nenhuma execução",
        "status": "Aguardando",
        "status_class": "waiting",
        "mensagem": "Sistema pronto para iniciar coleta"
    }

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página inicial da aplicação"""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "metricas": get_system_metrics(),
            "status": get_system_status()
        }
    )

@app.get("/coletar", response_class=HTMLResponse)
async def pagina_coletar(request: Request):
    """Página de coleta de dados"""
    return templates.TemplateResponse(
        "coletar.html",
        {"request": request}
    )

@app.get("/consultar", response_class=HTMLResponse)
async def pagina_consultar(request: Request):
    """Página de consulta de dados"""
    return templates.TemplateResponse(
        "consultar.html",
        {"request": request}
    )

@app.get("/categorias")
async def listar_categorias():
    """Lista as categorias disponíveis para scraping"""
    return {
        "categorias": [
            {
                "id": "1",
                "nome": "Açougue",
                "url": "https://www.paodeacucar.com/categoria/alimentos/acougue"
            },
            {
                "id": "2",
                "nome": "Alimentos Congelados",
                "url": "https://www.paodeacucar.com/categoria/alimentos/alimentos-congelados"
            },
            {
                "id": "3",
                "nome": "Alimentos Refrigerados",
                "url": "https://www.paodeacucar.com/categoria/alimentos/alimentos-refrigerados"
            },
            {
                "id": "4",
                "nome": "Básicos da Despensa",
                "url": "https://www.paodeacucar.com/categoria/alimentos/basico-da-despensa"
            },
            {
                "id": "5",
                "nome": "Cereais",
                "url": "https://www.paodeacucar.com/categoria/alimentos/cereais"
            },
            {
                "id": "6",
                "nome": "Complemento da Despensa",
                "url": "https://www.paodeacucar.com/categoria/alimentos/complemento-da-despensa"
            },
            {
                "id": "7",
                "nome": "Doces e Sobremesas",
                "url": "https://www.paodeacucar.com/categoria/alimentos/doces-e-sobremesas"
            },
            {
                "id": "8",
                "nome": "Hortifruti",
                "url": "https://www.paodeacucar.com/categoria/alimentos/hortifruti"
            },
            {
                "id": "9",
                "nome": "Mercearia Salgada",
                "url": "https://www.paodeacucar.com/categoria/alimentos/mercearia-salgada"
            },
            {
                "id": "10",
                "nome": "Padaria",
                "url": "https://www.paodeacucar.com/categoria/alimentos/padaria"
            },
            {
                "id": "11",
                "nome": "Peixaria",
                "url": "https://www.paodeacucar.com/categoria/alimentos/peixaria"
            },
            {
                "id": "12",
                "nome": "Rotisserie",
                "url": "https://www.paodeacucar.com/categoria/alimentos/rotisserie"
            },
            {
                "id": "13",
                "nome": "Salgadinhos e Aperitivos",
                "url": "https://www.paodeacucar.com/categoria/alimentos/salgadinhos-e-aperitivos"
            }
        ]
    }

@app.post("/coletar/urls", response_model=List[ProdutoBase])
async def coletar_urls(categoria: URLCategoria):
    """
    Coleta URLs dos produtos de uma categoria específica
    
    - **url**: URL da categoria para coletar
    - **nome**: Nome da categoria (opcional)
    - **modo_teste**: Se True, limita a quantidade de URLs coletadas
    """
    try:
        collector = URLCollector(modo_teste=bool(categoria.modo_teste))
        urls = collector.coletar_urls(categoria.url)
        
        # Converte para o formato da API
        produtos = []
        for url_info in urls:
            produto = ProdutoBase(
                url=str(url_info['url']),
                nome=str(url_info['nome']),
                categoria=str(url_info.get('categoria', categoria.nome))
            )
            produtos.append(produto)
        
        return produtos
    
    except Exception as e:
        logger.error(f"Erro ao coletar URLs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/coletar/dados", response_model=List[DadoNutricional])
async def coletar_dados(urls: List[ProdutoBase]):
    """
    Faz scraping dos dados nutricionais de uma lista de URLs
    
    - **urls**: Lista de objetos contendo URL, nome e categoria dos produtos
    """
    try:
        # Salva URLs em CSV temporário
        df_urls = pd.DataFrame([url.dict() for url in urls])
        temp_urls_file = f"urls_temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df_urls.to_csv(temp_urls_file, index=False)
        
        # Faz o scraping
        scraper = Scraper()
        scraper.processar_arquivo_urls(temp_urls_file)
        
        # Lê os resultados
        if os.path.exists("dados_nutricionais.csv"):
            df_dados = pd.read_csv("dados_nutricionais.csv")
            
            # Converte para o formato da API
            produtos = []
            for _, row in df_dados.iterrows():
                produto = DadoNutricional(
                    nome=str(row['NOME_PRODUTO']),
                    url=str(row['URL']),
                    porcao=float(row['PORCAO (g)']),
                    calorias=float(row['CALORIAS (kcal)']),
                    carboidratos=float(row['CARBOIDRATOS (g)']),
                    proteinas=float(row['PROTEINAS (g)']),
                    gorduras=float(row['GORDURAS_TOTAIS (g)']),
                    gorduras_saturadas=float(row['GORDURAS_SATURADAS (g)']),
                    fibras=float(row['FIBRAS (g)']),
                    acucares=float(row['ACUCARES (g)']),
                    sodio=float(row['SODIO (mg)']),
                    categoria=str(row.get('categoria', '')),
                    data_coleta=datetime.now().isoformat()
                )
                produtos.append(produto)
            
            # Remove arquivo temporário
            if os.path.exists(temp_urls_file):
                os.remove(temp_urls_file)
            
            return produtos
        else:
            raise HTTPException(status_code=404, detail="Nenhum dado foi coletado")
    
    except Exception as e:
        logger.error(f"Erro ao coletar dados: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/coletar/categoria", response_model=List[DadoNutricional])
async def coletar_categoria_completa(categoria: URLCategoria):
    """
    Faz o processo completo de coleta para uma categoria:
    1. Coleta URLs dos produtos
    2. Faz scraping dos dados nutricionais
    
    - **url**: URL da categoria para coletar
    - **nome**: Nome da categoria (opcional)
    - **modo_teste**: Se True, limita a quantidade de URLs coletadas
    """
    try:
        logger.info(f"🔍 Iniciando coleta para categoria: {categoria.nome}")
        logger.info(f"📊 Modo de coleta: {'Teste' if categoria.modo_teste else 'Completo'}")
        
        # Primeiro coleta as URLs
        logger.info("🌐 Inicializando coletor de URLs...")
        collector = URLCollector(modo_teste=bool(categoria.modo_teste))
        
        logger.info(f"📑 Coletando URLs da categoria {categoria.nome}...")
        urls = collector.coletar_urls(categoria.url)
        logger.info(f"✅ URLs coletadas com sucesso! Total: {len(urls)} produtos encontrados")
        
        # Converte para o formato da API
        produtos = []
        logger.info("🔄 Processando informações coletadas...")
        for url_info in urls:
            produto = ProdutoBase(
                url=str(url_info['url']),
                nome=str(url_info['nome']),
                categoria=str(url_info.get('categoria', categoria.nome))
            )
            produtos.append(produto)
        
        # Depois faz o scraping dos dados
        logger.info("🤖 Iniciando coleta de dados nutricionais...")
        logger.info("⚙️ Configurando scraper...")
        
        # Salva URLs em CSV temporário
        df_urls = pd.DataFrame([url.dict() for url in produtos])
        temp_urls_file = f"urls_temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df_urls.to_csv(temp_urls_file, index=False)
        
        # Faz o scraping
        scraper = Scraper()
        logger.info("🔄 Processando arquivo de URLs...")
        scraper.processar_arquivo_urls(temp_urls_file)
        
        # Lê os resultados
        if os.path.exists("dados_nutricionais.csv"):
            logger.info("📊 Lendo dados coletados...")
            df_dados = pd.read_csv("dados_nutricionais.csv")
            
            # Converte para o formato da API
            produtos_coletados = []
            for _, row in df_dados.iterrows():
                produto = DadoNutricional(
                    nome=str(row['NOME_PRODUTO']),
                    url=str(row['URL']),
                    porcao=float(row['PORCAO (g)']),
                    calorias=float(row['CALORIAS (kcal)']),
                    carboidratos=float(row['CARBOIDRATOS (g)']),
                    proteinas=float(row['PROTEINAS (g)']),
                    gorduras=float(row['GORDURAS_TOTAIS (g)']),
                    gorduras_saturadas=float(row['GORDURAS_SATURADAS (g)']),
                    fibras=float(row['FIBRAS (g)']),
                    acucares=float(row['ACUCARES (g)']),
                    sodio=float(row['SODIO (mg)']),
                    categoria=str(row.get('categoria', '')),
                    data_coleta=datetime.now().isoformat()
                )
                produtos_coletados.append(produto)
            
            # Remove arquivo temporário
            if os.path.exists(temp_urls_file):
                os.remove(temp_urls_file)
                logger.info("🧹 Arquivos temporários removidos")
            
            logger.info(f"✨ Coleta finalizada com sucesso! {len(produtos_coletados)} produtos processados")
            return produtos_coletados
        else:
            raise HTTPException(status_code=404, detail="Nenhum dado foi coletado")
    
    except Exception as e:
        logger.error(f"❌ Erro ao processar categoria: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/produtos", response_model=List[DadoNutricional])
async def listar_produtos(
    skip: int = Query(0, description="Número de registros para pular (para paginação)"),
    limit: int = Query(10, description="Número máximo de registros para retornar"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoria de produto"),
    nome: Optional[str] = Query(None, description="Filtrar por nome do produto (busca parcial)")
):
    """
    Lista os produtos e seus dados nutricionais com opções de paginação e filtros
    """
    try:
        # Verifica se o arquivo de dados existe
        if not os.path.exists("dados_nutricionais.csv"):
            raise HTTPException(status_code=404, detail="Nenhum dado nutricional disponível")
        
        # Lê o arquivo CSV
        df = pd.read_csv("dados_nutricionais.csv")
        
        # Verifica se as colunas necessárias existem
        colunas_esperadas = [
            'NOME_PRODUTO', 'URL', 'PORCAO (g)', 'CALORIAS (kcal)', 
            'CARBOIDRATOS (g)', 'PROTEINAS (g)', 'GORDURAS_TOTAIS (g)',
            'GORDURAS_SATURADAS (g)', 'FIBRAS (g)', 'ACUCARES (g)', 'SODIO (mg)',
            'data_coleta'
        ]
        colunas_faltantes = [col for col in colunas_esperadas if col not in df.columns]
        if colunas_faltantes:
            raise HTTPException(
                status_code=500, 
                detail=f"Colunas faltantes no CSV: {', '.join(colunas_faltantes)}"
            )
        
        # Aplica filtros se fornecidos
        if categoria:
            df = df[df['categoria'].str.contains(categoria, case=False, na=False)]
        if nome:
            df = df[df['NOME_PRODUTO'].str.contains(nome, case=False, na=False)]
        
        # Aplica paginação
        total = len(df)
        df = df.iloc[skip:skip + limit]
        
        # Converte para o formato da API
        produtos = []
        for _, row in df.iterrows():
            try:
                # Garante que os valores numéricos sejam float
                valores_numericos = {
                    'PORCAO (g)': float(row['PORCAO (g)']),
                    'CALORIAS (kcal)': float(row['CALORIAS (kcal)']),
                    'CARBOIDRATOS (g)': float(row['CARBOIDRATOS (g)']),
                    'PROTEINAS (g)': float(row['PROTEINAS (g)']),
                    'GORDURAS_TOTAIS (g)': float(row['GORDURAS_TOTAIS (g)']),
                    'GORDURAS_SATURADAS (g)': float(row['GORDURAS_SATURADAS (g)']),
                    'FIBRAS (g)': float(row['FIBRAS (g)']),
                    'ACUCARES (g)': float(row['ACUCARES (g)']),
                    'SODIO (mg)': float(row['SODIO (mg)'])
                }
                
                # Garante que a data seja string
                data_coleta = str(row['data_coleta']) if pd.notna(row['data_coleta']) else None
                
                produto = DadoNutricional(
                    nome=str(row['NOME_PRODUTO']),
                    url=str(row['URL']),
                    porcao=valores_numericos['PORCAO (g)'],
                    calorias=valores_numericos['CALORIAS (kcal)'],
                    carboidratos=valores_numericos['CARBOIDRATOS (g)'],
                    proteinas=valores_numericos['PROTEINAS (g)'],
                    gorduras=valores_numericos['GORDURAS_TOTAIS (g)'],
                    gorduras_saturadas=valores_numericos['GORDURAS_SATURADAS (g)'],
                    fibras=valores_numericos['FIBRAS (g)'],
                    acucares=valores_numericos['ACUCARES (g)'],
                    sodio=valores_numericos['SODIO (mg)'],
                    categoria=str(row.get('categoria', '')),
                    data_coleta=data_coleta
                )
                produtos.append(produto)
            except Exception as e:
                logger.error(f"Erro ao converter linha do CSV: {str(e)}")
                logger.error(f"Dados da linha: {row.to_dict()}")
                continue
        
        return produtos
    
    except Exception as e:
        logger.error(f"Erro ao listar produtos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/coletar")
async def iniciar_coleta(request: Request):
    """Inicia o processo de coleta de dados"""
    global coleta_ativa, scraper_instance
    
    if coleta_ativa:
        raise HTTPException(status_code=400, detail="Já existe uma coleta em andamento")
    
    try:
        form = await request.form()
        modo = form.get("modo", "teste")
        categorias = form.getlist("categorias[]") if "categorias[]" in form else form.getlist("categorias")
        
        if not categorias:
            raise HTTPException(status_code=400, detail="Nenhuma categoria selecionada")
        
        # Marca a coleta como ativa
        coleta_ativa = True
        
        # Inicializa o scraper
        scraper_instance = Scraper()
        
        # Inicia a coleta em background
        import asyncio
        asyncio.create_task(realizar_coleta(modo, categorias))
        
        return {"status": "Coleta iniciada com sucesso"}
        
    except Exception as e:
        coleta_ativa = False
        scraper_instance = None
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cancelar-coleta")
async def cancelar_coleta():
    """Cancela o processo de coleta em andamento"""
    global coleta_ativa, scraper_instance
    
    if not coleta_ativa:
        raise HTTPException(status_code=400, detail="Não há coleta em andamento")
    
    try:
        # Primeiro marca como inativa para interromper o loop de coleta
        coleta_ativa = False
        
        # Aguarda um momento para garantir que o loop de coleta foi interrompido
        await asyncio.sleep(1)
        
        # Cancela o scraper se existir
        if scraper_instance:
            try:
                scraper_instance.cancelar()  # Usa o novo método de cancelamento
            except Exception as e:
                logger.error(f"Erro ao cancelar scraper: {str(e)}")
            finally:
                scraper_instance = None
        
        await emit_log_update("Coleta cancelada pelo usuário", "warning")
        return {"status": "Coleta cancelada com sucesso"}
        
    except Exception as e:
        logger.error(f"Erro ao cancelar coleta: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def realizar_coleta(modo: str, categorias: List[str]):
    """Realiza a coleta de dados em background"""
    global coleta_ativa, scraper_instance
    
    try:
        # Carrega URLs já coletadas do CSV existente
        urls_ja_coletadas = set()
        if os.path.exists('dados_nutricionais.csv'):
            df_existente = pd.read_csv('dados_nutricionais.csv')
            urls_ja_coletadas = set(df_existente['URL'])
            await emit_log_update(f"Encontrados {len(urls_ja_coletadas)} produtos já coletados anteriormente")
        
        # Obtém as URLs das categorias
        todas_categorias = (await listar_categorias())["categorias"]
        # Converte os IDs para string para garantir a comparação correta
        categorias = [str(cat) for cat in categorias]
        categorias_selecionadas = [cat for cat in todas_categorias if str(cat["id"]) in categorias]
        
        await emit_log_update(f"Iniciando coleta para {len(categorias_selecionadas)} categorias")
        
        # Lista para armazenar todas as URLs coletadas
        todas_urls = []
        
        # Primeiro coleta todas as URLs de todas as categorias
        for categoria in categorias_selecionadas:
            if not coleta_ativa:
                await emit_log_update("Coleta interrompida", "warning")
                if scraper_instance:
                    scraper_instance.cancelar()
                break
                
            try:
                await emit_log_update(f"Coletando URLs da categoria: {categoria['nome']}")
                
                # Coleta URLs da categoria
                collector = URLCollector()
                urls = collector.coletar_urls(url_categoria=categoria["url"], modo_teste=(modo == "teste"))
                
                if not coleta_ativa:
                    if scraper_instance:
                        scraper_instance.cancelar()
                    break
                
                # Filtra apenas URLs que ainda não foram coletadas
                urls_novas = [url for url in urls if url['url'] not in urls_ja_coletadas]
                await emit_log_update(f"Encontrados {len(urls)} produtos em {categoria['nome']}, sendo {len(urls_novas)} novos")
                todas_urls.extend(urls_novas)
                
            except Exception as e:
                await emit_log_update(f"Erro ao coletar URLs da categoria {categoria['nome']}: {str(e)}", "error")
                continue
        
        # Depois coleta os dados nutricionais apenas das URLs novas
        total_urls = len(todas_urls)
        await emit_log_update(f"Total de URLs novas para coletar: {total_urls}")
        
        if total_urls == 0:
            await emit_log_update("✅ Não há novos produtos para coletar!", "success")
            return
        
        # Processa cada URL nova
        for i, url_info in enumerate(todas_urls, 1):
            if not coleta_ativa:
                if scraper_instance:
                    scraper_instance.cancelar()
                break
                
            try:
                await emit_log_update(f"Processando novo produto {i}/{total_urls}")
                # Extrai a URL do dicionário
                url = url_info['url']
                
                # Verifica novamente se a URL já não foi coletada (dupla verificação)
                if url in urls_ja_coletadas:
                    await emit_log_update(f"Produto {i}/{total_urls} já foi coletado anteriormente, pulando...", "info")
                    continue
                
                resultado = scraper_instance.extrair_dados_nutricionais(url)
                
                if resultado:
                    # Adiciona a URL ao conjunto de URLs já coletadas
                    urls_ja_coletadas.add(url)
                    await emit_log_update(f"✅ Novo produto {i}/{total_urls} coletado com sucesso", "success")
                else:
                    await emit_log_update(f"❌ Falha ao coletar novo produto {i}/{total_urls}", "error")
                
            except Exception as e:
                await emit_log_update(f"Erro ao processar produto: {str(e)}", "error")
                continue
        
        if coleta_ativa:
            await emit_log_update("✅ Coleta finalizada com sucesso", "success")
        
    except Exception as e:
        await emit_log_update(f"❌ Erro durante a coleta: {str(e)}", "error")
    
    finally:
        coleta_ativa = False
        if scraper_instance:
            scraper_instance.cancelar()
            scraper_instance = None
        await emit_log_update("Sistema pronto para nova coleta", "info")

@app.get("/download-excel")
async def download_excel():
    """Endpoint para download dos dados em formato Excel"""
    try:
        # Lê o arquivo CSV
        df = pd.read_csv("dados_nutricionais.csv")
        
        # Cria um buffer em memória para o Excel
        output = io.BytesIO()
        
        # Salva o DataFrame como Excel no buffer
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Dados Nutricionais', index=False)
            
            # Ajusta largura das colunas
            worksheet = writer.sheets['Dados Nutricionais']
            for i, col in enumerate(df.columns):
                max_length = max(df[col].astype(str).apply(len).max(), len(col)) + 2
                worksheet.set_column(i, i, max_length)
        
        # Prepara o buffer para leitura
        output.seek(0)
        
        # Retorna o arquivo Excel como resposta
        headers = {
            'Content-Disposition': 'attachment; filename=dados_nutricionais.xlsx'
        }
        return StreamingResponse(
            output,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers=headers
        )
    
    except Exception as e:
        logger.error(f"Erro ao gerar arquivo Excel: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Eventos do Socket.IO
@sio.event
async def connect(sid, environ):
    print(f"Cliente conectado: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Cliente desconectado: {sid}")

# Função para emitir atualizações do log
async def emit_log_update(message: str, type: str = "info"):
    await sio.emit('log_update', {'message': message, 'type': type})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("api:socket_app", host="0.0.0.0", port=port, reload=True) 