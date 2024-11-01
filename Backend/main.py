from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import time
import asyncpg
import os

# Função para obter a conexão com o banco de dados PostgreSQL
async def get_database():
    DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/Placas_de_video") 
    return await asyncpg.connect(DATABASE_URL)

# Inicializar a aplicação FastAPI
app = FastAPI()

# Modelo para adicionar novas placas de vídeo
class Placa(BaseModel):
    id: Optional[int] = None
    Modelo: str
    Marca: str
    quantidade: int
    preco: float

class PlacaBase(BaseModel):
    Modelo: str
    Marca: str
    quantidade: int
    preco: float

# Modelo para venda de Placas de vídeo
class VendaPlaca(BaseModel):
    quantidade: int

# Modelo para atualizar atributos de uma placa (exceto o ID)
class AtualizarPlaca(BaseModel):
    Modelo: Optional[str] = None
    Marca: Optional[str] = None
    quantidade: Optional[int] = None
    preco: Optional[float] = None

# Middleware para logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Path: {request.url.path}, Method: {request.method}, Process Time: {process_time:.4f}s")
    return response

# Função para verificar se a placa existe usando marca e modelo
async def placa_existe(Modelo: str, Marca: str, conn: asyncpg.Connection):
    try:
        query = "SELECT * FROM Placas_de_video WHERE LOWER(Modelo) = LOWER($1) AND LOWER(Marca) = LOWER($2)"
        result = await conn.fetchval(query, Modelo, Marca)
        return result is not None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao verificar se a placa existe: {str(e)}")

# 1. Adicionar uma nova placa
@app.post("/api/v1/Placas_de_video/", status_code=201)
async def adicionar_placa(placa: PlacaBase):
    conn = await get_database()
    if await placa_existe(placa.Modelo, placa.Marca, conn):
        raise HTTPException(status_code=400, detail="Placa já existe.")
    try:
        query = "INSERT INTO Placas_de_video (Modelo, Marca, quantidade, preco) VALUES ($1, $2, $3, $4)"
        async with conn.transaction():
            await conn.execute(query, placa.Modelo, placa.Marca, placa.quantidade, placa.preco)
            return {"message": "Placa adicionada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao adicionar a placa: {str(e)}")
    finally:
        await conn.close()

# 2. Listar todas as placas de vídeo
@app.get("/api/v1/Placas_de_video/", response_model=List[Placa])
async def listar_placas():
    conn = await get_database()
    try:
        query = "SELECT * FROM Placas_de_video"
        rows = await conn.fetch(query)
        placas_de_video = [dict(row) for row in rows]
        return placas_de_video
    finally:
        await conn.close()

# 3. Buscar placa por ID
@app.get("/api/v1/Placas_de_video/{placa_id}")
async def listar_placa_por_id(placa_id: int):
    conn = await get_database()
    try:
        query = "SELECT * FROM Placas_de_video WHERE id = $1"
        placa = await conn.fetchrow(query, placa_id)
        if placa is None:
            raise HTTPException(status_code=404, detail="Placa de vídeo não encontrada.")
        return dict(placa)
    finally:
        await conn.close()

# 4. Vender uma placa de vídeo (reduzir quantidade no estoque)
@app.put("/api/v1/Placas_de_video/{placa_id}/vender/")
async def vender_placa(placa_id: int, venda: VendaPlaca):
    conn = await get_database()
    try:
        query = "SELECT * FROM Placas_de_video WHERE id = $1"
        placa = await conn.fetchrow(query, placa_id)
        if placa is None:
            raise HTTPException(status_code=404, detail="Placa de vídeo não encontrada.")

        if placa['quantidade'] < venda.quantidade:
            raise HTTPException(status_code=400, detail="Quantidade insuficiente no estoque.")

        nova_quantidade = placa['quantidade'] - venda.quantidade
        update_query = "UPDATE Placas_de_video SET quantidade = $1 WHERE id = $2"
        await conn.execute(update_query, nova_quantidade, placa_id)

        valor_venda = placa['preco'] * venda.quantidade
        insert_venda_query = """
            INSERT INTO vendas (placa_id, quantidade_vendida, valor_venda) 
            VALUES ($1, $2, $3)
        """
        await conn.execute(insert_venda_query, placa_id, venda.quantidade, valor_venda)

        placa_atualizada = dict(placa)
        placa_atualizada['quantidade'] = nova_quantidade

        return {"message": "Venda realizada com sucesso!", "placa": placa_atualizada}
    finally:
        await conn.close()

# 5. Atualizar atributos de uma placa pelo ID (exceto o ID)
@app.patch("/api/v1/Placas_de_video/{placa_id}")
async def atualizar_placa(placa_id: int, placa_atualizacao: AtualizarPlaca):
    conn = await get_database()
    try:
        query = "SELECT * FROM Placas_de_video WHERE id = $1"
        placa = await conn.fetchrow(query, placa_id)
        if placa is None:
            raise HTTPException(status_code=404, detail="Placa de vídeo não encontrada.")

        update_query = """
            UPDATE Placas_de_video
            SET Modelo = COALESCE($1, Modelo),
                Marca = COALESCE($2, Marca),
                quantidade = COALESCE($3, quantidade),
                preco = COALESCE($4, preco)
            WHERE id = $5
        """
        await conn.execute(
            update_query,
            placa_atualizacao.Modelo,
            placa_atualizacao.Marca,
            placa_atualizacao.quantidade,
            placa_atualizacao.preco,
            placa_id
        )
        return {"message": "Placa de vídeo atualizada com sucesso!"}
    finally:
        await conn.close()

# 6. Remover uma placa pelo ID
@app.delete("/api/v1/Placas_de_video/{placa_id}")
async def remover_placa(placa_id: int):
    conn = await get_database()
    try:
        query = "SELECT * FROM Placas_de_video WHERE id = $1"
        placa = await conn.fetchrow(query, placa_id)
        if placa is None:
            raise HTTPException(status_code=404, detail="Placa de vídeo não encontrada.")

        delete_query = "DELETE FROM Placas_de_video WHERE id = $1"
        await conn.execute(delete_query, placa_id)
        return {"message": "Placa removida com sucesso!"}
    finally:
        await conn.close()

# 7. Resetar banco de dados de Placas de vídeo
@app.delete("/api/v1/Placas_de_video/")
async def resetar_Placas_de_video():
    init_sql = os.getenv("INIT_SQL", "db/init.sql")
    conn = await get_database()
    try:
        with open(init_sql, 'r') as file:
            sql_commands = file.read()
        await conn.execute(sql_commands)
        return {"message": "Banco de dados limpo com sucesso!"}
    finally:
        await conn.close()

# 8. Listar vendas
@app.get("/api/v1/vendas/")
async def listar_vendas():
    conn = await get_database()
    try:
        query = "SELECT * FROM vendas"
        rows = await conn.fetch(query)
        vendas = [dict(row) for row in rows]
        return vendas
    finally:
        await conn.close()
