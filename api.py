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
import webbrowser
import time

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
            'nome', 'url', 'porcao', 'calorias', 
            'carboidratos', 'proteinas', 'gorduras',
            'gorduras_saturadas', 'fibras', 'acucares', 'sodio',
            'data_coleta', 'categoria'
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
            df = df[df['nome'].str.contains(nome, case=False, na=False)]
        
        # Ordena por data de coleta decrescente (mais recente primeiro)
        try:
            # Converte datas para datetime, lidando com formatos mistos
            df['data_coleta_dt'] = pd.to_datetime(df['data_coleta'], format='mixed', errors='coerce')
            # Se falhar, tenta formatos específicos
            mask_na = df['data_coleta_dt'].isna()
            if mask_na.any():
                # Tenta formato apenas data
                df.loc[mask_na, 'data_coleta_dt'] = pd.to_datetime(
                    df.loc[mask_na, 'data_coleta'], 
                    format='%Y-%m-%d', 
                    errors='coerce'
                )
            
            # Ordena por data decrescente
            df = df.sort_values('data_coleta_dt', ascending=False, na_position='last')
            df = df.drop('data_coleta_dt', axis=1)  # Remove coluna auxiliar
        except Exception as e:
            logger.warning(f"Erro ao ordenar por data: {e}. Mantendo ordem original.")
        
        # Aplica paginação
        total = len(df)
        df = df.iloc[skip:skip + limit]
        
        # Converte para o formato da API
        produtos = []
        for _, row in df.iterrows():
            try:
                # Garante que os valores numéricos sejam float
                valores_numericos = {
                    'porcao': float(row['porcao']),
                    'calorias': float(row['calorias']),
                    'carboidratos': float(row['carboidratos']),
                    'proteinas': float(row['proteinas']),
                    'gorduras': float(row['gorduras']),
                    'gorduras_saturadas': float(row['gorduras_saturadas']),
                    'fibras': float(row['fibras']),
                    'acucares': float(row['acucares']),
                    'sodio': float(row['sodio'])
                }
                
                # Garante que a data seja string
                data_coleta = str(row['data_coleta']) if pd.notna(row['data_coleta']) else None
                
                produto = DadoNutricional(
                    nome=str(row['nome']),
                    url=str(row['url']),
                    porcao=valores_numericos['porcao'],
                    calorias=valores_numericos['calorias'],
                    carboidratos=valores_numericos['carboidratos'],
                    proteinas=valores_numericos['proteinas'],
                    gorduras=valores_numericos['gorduras'],
                    gorduras_saturadas=valores_numericos['gorduras_saturadas'],
                    fibras=valores_numericos['fibras'],
                    acucares=valores_numericos['acucares'],
                    sodio=valores_numericos['sodio'],
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
    """Realiza a coleta de dados em background com logging detalhado"""
    global coleta_ativa, scraper_instance
    
    inicio_coleta = datetime.now()
    estatisticas = {
        'sucessos': 0,
        'falhas': 0,
        'produtos_ja_existentes': 0,
        'categorias_processadas': 0,
        'tempo_medio_por_produto': 0
    }
    
    try:
        await emit_log_update("🚀 Iniciando sistema de coleta...", "system")
        
        # Carrega URLs já coletadas do CSV existente
        urls_ja_coletadas = set()
        if os.path.exists('dados_nutricionais.csv'):
            df_existente = pd.read_csv('dados_nutricionais.csv')
            urls_ja_coletadas = set(df_existente['url'])
            await emit_log_update(
                f"📊 Base de dados carregada: {len(urls_ja_coletadas)} produtos já coletados",
                "info",
                estatisticas={"produtos_existentes": len(urls_ja_coletadas)}
            )
        else:
            await emit_log_update("📊 Criando nova base de dados (primeira coleta)", "info")
        
        # Obtém as URLs das categorias
        todas_categorias = (await listar_categorias())["categorias"]
        categorias = [str(cat) for cat in categorias]
        categorias_selecionadas = [cat for cat in todas_categorias if str(cat["id"]) in categorias]
        
        await emit_log_update(
            f"🎯 Configuração de coleta: {len(categorias_selecionadas)} categorias selecionadas",
            "system",
            total=len(categorias_selecionadas)
        )
        
        for i, cat in enumerate(categorias_selecionadas, 1):
            await emit_log_update(f"  📂 {i}. {cat['nome']}", "info")
        
        await emit_log_update(f"⚙️ Modo de coleta: {'🧪 Teste (limitado)' if modo == 'teste' else '🔥 Completo (ilimitado)'}", "system")
        
        # Lista para armazenar todas as URLs coletadas
        todas_urls = []
        
        # FASE 1: Coleta de URLs
        await emit_log_update("📋 FASE 1: Coletando URLs dos produtos...", "system")
        
        for idx_cat, categoria in enumerate(categorias_selecionadas, 1):
            if not coleta_ativa:
                await emit_log_update("⏹️ Coleta interrompida pelo usuário", "warning")
                if scraper_instance:
                    scraper_instance.cancelar()
                break
                
            try:
                progresso_categoria = int((idx_cat - 1) / len(categorias_selecionadas) * 50)  # 50% para coleta URLs
                
                await emit_log_update(
                    f"🔍 Processando categoria: {categoria['nome']}",
                    "info",
                    progress=progresso_categoria,
                    categoria=categoria['nome'],
                    estatisticas={"fase": "Coleta de URLs", "categoria_atual": f"{idx_cat}/{len(categorias_selecionadas)}"}
                )
                
                # Coleta URLs da categoria
                collector = URLCollector()
                
                # Log inicio da coleta de URLs
                await emit_log_update(f"  🌐 Abrindo navegador para categoria {categoria['nome']}...", "info")
                
                urls = collector.coletar_urls(
                    url_categoria=categoria["url"], 
                    modo_teste=(modo == "teste"),
                    categoria_nome=categoria["nome"]
                )
                
                if not coleta_ativa:
                    if scraper_instance:
                        scraper_instance.cancelar()
                    break
                
                # Filtra apenas URLs que ainda não foram coletadas
                urls_novas = [url for url in urls if url['url'] not in urls_ja_coletadas]
                urls_existentes = len(urls) - len(urls_novas)
                
                estatisticas['produtos_ja_existentes'] += urls_existentes
                estatisticas['categorias_processadas'] += 1
                
                await emit_log_update(
                    f"  ✅ {categoria['nome']}: {len(urls)} produtos encontrados ({len(urls_novas)} novos, {urls_existentes} já coletados)",
                    "success",
                    categoria=categoria['nome'],
                    collected=len(urls_novas),
                    total=len(urls)
                )
                
                todas_urls.extend(urls_novas)
                
                # Log detalhado dos primeiros produtos encontrados
                if urls_novas:
                    await emit_log_update(f"  📝 Exemplos encontrados:", "info")
                    for i, url_info in enumerate(urls_novas[:3], 1):
                        await emit_log_update(f"    {i}. {url_info['nome'][:50]}{'...' if len(url_info['nome']) > 50 else ''}", "info")
                    if len(urls_novas) > 3:
                        await emit_log_update(f"    ... e mais {len(urls_novas) - 3} produtos", "info")
                
            except Exception as e:
                await emit_log_update(f"❌ Erro ao coletar URLs da categoria {categoria['nome']}: {str(e)}", "error")
                estatisticas['falhas'] += 1
                continue
        
        # FASE 2: Coleta de dados nutricionais
        total_urls = len(todas_urls)
        
        if total_urls == 0:
            await emit_log_update("ℹ️ Não há novos produtos para coletar. Base de dados já está atualizada!", "success", progress=100)
            return
        
        await emit_log_update(
            f"🍽️ FASE 2: Coletando dados nutricionais de {total_urls} produtos...",
            "system",
            progress=50,
            total=total_urls
        )
        
        tempo_estimado_por_produto = 8  # segundos por produto estimado
        tempo_total_estimado = total_urls * tempo_estimado_por_produto
        
        await emit_log_update(
            f"⏱️ Tempo estimado: {tempo_total_estimado // 60}min {tempo_total_estimado % 60}s ({tempo_estimado_por_produto}s por produto)",
            "info",
            tempo_estimado=f"{tempo_total_estimado // 60}min {tempo_total_estimado % 60}s"
        )
        
        # Processa cada URL nova
        for i, url_info in enumerate(todas_urls, 1):
            if not coleta_ativa:
                if scraper_instance:
                    scraper_instance.cancelar()
                break
                
            try:
                inicio_produto = datetime.now()
                progresso = int(50 + (i / total_urls) * 50)  # 50-100% para coleta de dados
                
                nome_produto = url_info.get('nome', 'Produto sem nome')[:40]
                categoria_produto = url_info.get('categoria', 'Categoria não informada')
                
                await emit_log_update(
                    f"🔄 Produto {i}/{total_urls}: {nome_produto}{'...' if len(url_info.get('nome', '')) > 40 else ''}",
                    "info",
                    progress=progresso,
                    collected=estatisticas['sucessos'],
                    total=total_urls,
                    categoria=categoria_produto,
                    produto_nome=nome_produto
                )
                
                # Extrai a URL do dicionário
                url = url_info['url']
                
                # Verifica novamente se a URL já não foi coletada (dupla verificação)
                if url in urls_ja_coletadas:
                    await emit_log_update(f"  ⏭️ Produto já coletado anteriormente, pulando...", "info")
                    estatisticas['produtos_ja_existentes'] += 1
                    continue
                
                await emit_log_update(f"  🌐 Acessando página do produto...", "info")
                resultado = scraper_instance.extrair_dados_nutricionais(url, categoria_produto)
                
                fim_produto = datetime.now()
                tempo_produto = (fim_produto - inicio_produto).total_seconds()
                
                if resultado:
                    # Adiciona a URL ao conjunto de URLs já coletadas
                    urls_ja_coletadas.add(url)
                    estatisticas['sucessos'] += 1
                    
                    # Atualiza tempo médio
                    estatisticas['tempo_medio_por_produto'] = (
                        (estatisticas['tempo_medio_por_produto'] * (estatisticas['sucessos'] - 1) + tempo_produto) / 
                        estatisticas['sucessos']
                    )
                    
                    # Calcula novo tempo estimado
                    produtos_restantes = total_urls - i
                    tempo_restante = int(produtos_restantes * estatisticas['tempo_medio_por_produto'])
                    
                    await emit_log_update(
                        f"  ✅ Dados coletados com sucesso! ({tempo_produto:.1f}s)",
                        "success",
                        progress=progresso,
                        collected=estatisticas['sucessos'],
                        tempo_estimado=f"{tempo_restante // 60}min {tempo_restante % 60}s restantes",
                        estatisticas=estatisticas
                    )
                    
                    # Log dos dados nutricionais coletados
                    if resultado.get('calorias', 0) > 0:
                        await emit_log_update(
                            f"    📊 {resultado.get('calorias', 0)}kcal | Prot: {resultado.get('proteinas', 0)}g | Carb: {resultado.get('carboidratos', 0)}g | Gord: {resultado.get('gorduras', 0)}g",
                            "info"
                        )
                    
                else:
                    estatisticas['falhas'] += 1
                    await emit_log_update(
                        f"  ❌ Falha ao extrair dados nutricionais ({tempo_produto:.1f}s)",
                        "error",
                        progress=progresso,
                        estatisticas=estatisticas
                    )
                
            except Exception as e:
                estatisticas['falhas'] += 1
                await emit_log_update(f"  💥 Erro ao processar produto: {str(e)}", "error")
                continue
        
        # Finalização
        if coleta_ativa:
            tempo_total = (datetime.now() - inicio_coleta).total_seconds()
            
            await emit_log_update(
                "🎉 Coleta finalizada com sucesso!",
                "success",
                progress=100,
                collected=estatisticas['sucessos'],
                total=total_urls,
                estatisticas=estatisticas
            )
            
            await emit_log_update(
                f"📈 Resumo da coleta:",
                "system",
                estatisticas=estatisticas
            )
            await emit_log_update(f"  ✅ Sucessos: {estatisticas['sucessos']}", "success")
            await emit_log_update(f"  ❌ Falhas: {estatisticas['falhas']}", "error")
            await emit_log_update(f"  📂 Categorias processadas: {estatisticas['categorias_processadas']}", "info")
            await emit_log_update(f"  ⏱️ Tempo total: {int(tempo_total // 60)}min {int(tempo_total % 60)}s", "info")
            await emit_log_update(f"  📊 Taxa de sucesso: {(estatisticas['sucessos'] / (estatisticas['sucessos'] + estatisticas['falhas']) * 100):.1f}%" if (estatisticas['sucessos'] + estatisticas['falhas']) > 0 else "0%", "info")
        
    except Exception as e:
        await emit_log_update(f"💥 Erro crítico durante a coleta: {str(e)}", "error", estatisticas=estatisticas)
    
    finally:
        coleta_ativa = False
        if scraper_instance:
            scraper_instance.cancelar()
            scraper_instance = None
        await emit_log_update("🏁 Sistema pronto para nova coleta", "system")

@app.get("/download-excel")
async def download_excel():
    """
    Baixa os dados nutricionais em formato Excel
    """
    # TODO: Implementar lógica para ler os dados do arquivo/banco
    # Por enquanto, vamos criar um DataFrame de exemplo
    dados = []
    
    # Verificar se existe arquivo de dados
    if os.path.exists("dados_nutricionais.csv"):
        try:
            df = pd.read_csv("dados_nutricionais.csv")
            dados = df.to_dict('records')
        except Exception as e:
            logger.error(f"Erro ao ler dados do arquivo CSV: {e}")
    
    if not dados:
        dados = [{
            "nome": "Exemplo - Produto não encontrado",
            "categoria": "Nenhuma",
            "porcao": 100,
            "calorias": 0,
            "carboidratos": 0,
            "proteinas": 0,
            "gorduras": 0,
            "gorduras_saturadas": 0,
            "fibras": 0,
            "acucares": 0,
            "sodio": 0,
            "data_coleta": datetime.now().strftime("%Y-%m-%d")
        }]
    
    df = pd.DataFrame(dados)
    
    # Criar arquivo Excel em memória
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Dados Nutricionais', index=False)
    
    output.seek(0)
    
    # Retornar o arquivo como resposta de streaming
    return StreamingResponse(
        io.BytesIO(output.read()),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=dados_nutricionais.xlsx"}
    )

# Endpoints com prefixo /api/ para compatibilidade com o frontend
@app.get("/api/categorias")
async def api_listar_categorias():
    """Lista as categorias disponíveis para scraping (API endpoint)"""
    return await listar_categorias()

@app.get("/api/produtos")
async def api_listar_produtos(
    page: int = Query(1, description="Número da página (começa em 1)"),
    limit: int = Query(10, description="Número máximo de registros por página"),
    search: Optional[str] = Query(None, description="Filtrar por nome do produto (busca parcial)"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoria de produto")
):
    """
    Lista os produtos coletados com paginação e filtros (API endpoint)
    
    - **page**: Número da página (começa em 1)
    - **limit**: Número máximo de registros por página
    - **search**: Filtrar por nome do produto (busca parcial)
    - **categoria**: Filtrar por categoria de produto
    """
    try:
        # Verifica se o arquivo de dados existe
        if not os.path.exists("dados_nutricionais.csv"):
            return {"produtos": [], "total": 0}
        
        # Lê o arquivo CSV
        df = pd.read_csv("dados_nutricionais.csv")
        
        # Aplica filtros se fornecidos
        if categoria:
            df = df[df['categoria'].str.contains(categoria, case=False, na=False)]
        if search:
            df = df[df['nome'].str.contains(search, case=False, na=False)]
        
        # Total de produtos após filtros
        total_produtos = len(df)
        
        # Ordena por data de coleta decrescente (mais recente primeiro)
        try:
            df['data_coleta_dt'] = pd.to_datetime(df['data_coleta'], format='mixed', errors='coerce')
            mask_na = df['data_coleta_dt'].isna()
            if mask_na.any():
                df.loc[mask_na, 'data_coleta_dt'] = pd.to_datetime(
                    df.loc[mask_na, 'data_coleta'], 
                    format='%Y-%m-%d', 
                    errors='coerce'
                )
            df = df.sort_values('data_coleta_dt', ascending=False, na_position='last')
            df = df.drop('data_coleta_dt', axis=1)
        except Exception as e:
            logger.warning(f"Erro ao ordenar por data: {e}. Mantendo ordem original.")
        
        # Aplica paginação
        skip = (page - 1) * limit
        df_paginado = df.iloc[skip:skip + limit]
        
        # Converte para o formato da API
        produtos = []
        for idx, row in df_paginado.iterrows():
            try:
                produto = {
                    "id": int(idx),  # Usa o índice como ID
                    "nome": str(row['nome']),
                    "categoria": str(row.get('categoria', '')),
                    "url": str(row['url']),
                    "porcao": float(row['porcao']),
                    "calorias": float(row['calorias']),
                    "energia": float(row['calorias']),  # Alias para calorias
                    "carboidratos": float(row['carboidratos']),
                    "proteinas": float(row['proteinas']),
                    "gorduras": float(row['gorduras']),
                    "gorduras_saturadas": float(row['gorduras_saturadas']),
                    "fibras": float(row['fibras']),
                    "acucares": float(row['acucares']),
                    "sodio": float(row['sodio']),
                    "data_coleta": str(row['data_coleta']) if pd.notna(row['data_coleta']) else None
                }
                produtos.append(produto)
            except Exception as e:
                logger.error(f"Erro ao converter linha do CSV: {str(e)}")
                continue
        
        return {
            "produtos": produtos,
            "total": total_produtos
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar produtos: {str(e)}")
        return {"produtos": [], "total": 0}

@app.get("/api/produtos/{produto_id}")
async def api_obter_produto(produto_id: int):
    """Obtém detalhes de um produto específico (API endpoint)"""
    try:
        # Verifica se o arquivo de dados existe
        if not os.path.exists("dados_nutricionais.csv"):
            raise HTTPException(status_code=404, detail="Nenhum dado nutricional disponível")
        
        # Lê o arquivo CSV
        df = pd.read_csv("dados_nutricionais.csv")
        
        # Verifica se o produto existe
        if produto_id >= len(df):
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        # Obtém o produto pelo índice
        row = df.iloc[produto_id]
        
        produto = {
            "id": produto_id,
            "nome": str(row['nome']),
            "categoria": str(row.get('categoria', '')),
            "url": str(row['url']),
            "porcao": float(row['porcao']),
            "calorias": float(row['calorias']),
            "energia": float(row['calorias']),  # Alias para calorias
            "carboidratos": float(row['carboidratos']),
            "proteinas": float(row['proteinas']),
            "gorduras": float(row['gorduras']),
            "gorduras_saturadas": float(row['gorduras_saturadas']),
            "fibras": float(row['fibras']),
            "acucares": float(row['acucares']),
            "sodio": float(row['sodio']),
            "data_coleta": str(row['data_coleta']) if pd.notna(row['data_coleta']) else None
        }
        
        return produto
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter produto: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@app.get("/api/download-excel")
async def api_download_excel(
    search: Optional[str] = Query(None, description="Filtrar por nome do produto"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoria")
):
    """
    Baixa os dados nutricionais em formato Excel (API endpoint)
    """
    return await download_excel()

# Eventos do Socket.IO
@sio.event
async def connect(sid, environ):
    print(f"Cliente conectado: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Cliente desconectado: {sid}")

# Função para emitir atualizações do log
async def emit_log_update(message: str, type: str = "info", progress: int = None, 
                         collected: int = None, total: int = None, categoria: str = None,
                         produto_nome: str = None, tempo_estimado: str = None,
                         estatisticas: dict = None):
    """
    Emite atualizações do log com informações detalhadas
    
    Args:
        message: Mensagem principal do log
        type: Tipo do log (info, success, error, warning, system)
        progress: Progresso em porcentagem (0-100)
        collected: Número de produtos coletados
        total: Total de produtos a coletar
        categoria: Categoria atual sendo processada
        produto_nome: Nome do produto atual
        tempo_estimado: Tempo estimado para conclusão
        estatisticas: Dicionário com estatísticas detalhadas
    """
    log_data = {
        'message': message, 
        'type': type,
        'timestamp': datetime.now().isoformat()
    }
    
    # Adiciona informações opcionais se fornecidas
    if progress is not None:
        log_data['progress'] = progress
    if collected is not None:
        log_data['collected'] = collected
    if total is not None:
        log_data['total'] = total
    if categoria:
        log_data['categoria'] = categoria
    if produto_nome:
        log_data['produto_nome'] = produto_nome
    if tempo_estimado:
        log_data['tempo_estimado'] = tempo_estimado
    if estatisticas:
        log_data['estatisticas'] = estatisticas
    
    await sio.emit('log_update', log_data)

# Função para abrir o navegador
def abrir_navegador(host: str, port: int):
    """Abre o navegador após aguardar o servidor iniciar"""
    time.sleep(1.5)  # Aguarda 1.5 segundos para o servidor iniciar completamente
    url = f"http://{host}:{port}"
    print(f"\n🚀 Abrindo navegador automaticamente: {url}")
    webbrowser.open(url)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = "localhost"  # Usando localhost para abrir no navegador local
    
    # Inicia thread para abrir o navegador
    browser_thread = Thread(target=abrir_navegador, args=(host, port))
    browser_thread.daemon = True
    browser_thread.start()
    
    print(f"🌟 Iniciando API de Dados Nutricionais...")
    print(f"📍 Servidor será executado em: http://{host}:{port}")
    print(f"🌐 O navegador abrirá automaticamente!")
    
    # Executa o servidor (usando localhost para consistência)
    uvicorn.run("api:socket_app", host="0.0.0.0", port=port, reload=True)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   