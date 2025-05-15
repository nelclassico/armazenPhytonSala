-- CRIAR TABELA PARA USUÁRIOS
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT UNIQUE NOT NULL, 
    password_hash TEXT NOT NULL, 
    funcao TEXT NOT NULL CHECK (funcao IN ('admin', 'gerente', 'estoquista', 'vendedor')), 
    nome TEXT NOT NULL
);

-- CRIAR TABELA PARA ÁREAS
CREATE TABLE IF NOT EXISTS areas_armazem (
    id_area TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    descricao TEXT NOT NULL
);

-- CRIAR TABELA PARA CATÁLOGO DE PRODUTOS
CREATE TABLE IF NOT EXISTS produtos_catalogo (
    id_produto TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    tipo_produto TEXT DEFAULT 'N/A',
    descricao TEXT DEFAULT ''
);

-- TABELA DE PRODUTOS NAS ÁREAS
CREATE TABLE IF NOT EXISTS produtos_areas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    area_id TEXT NOT NULL,
    id_catalogo_produto TEXT NOT NULL,
    nome_produto TEXT NOT NULL,
    quantidade INTEGER NOT NULL CHECK (quantidade >= 0),
    data_validade DATE NOT NULL,
    lote TEXT NOT NULL,
    FOREIGN KEY (area_id) REFERENCES areas_armazem(id_area),
    FOREIGN KEY (id_catalogo_produto) REFERENCES produtos_catalogo(id_produto),
    UNIQUE(area_id, id_catalogo_produto, lote, data_validade)
);

-- TABELA PARA VENDAS
CREATE TABLE IF NOT EXISTS vendas (
    id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
    id_catalogo_produto TEXT NOT NULL,
    nome_produto TEXT NOT NULL,
    lote_produto TEXT NOT NULL,
    data_validade_produto TEXT NOT NULL,
    quantidade_vendida INTEGER NOT NULL CHECK (quantidade_vendida > 0),
    data_venda DATE NOT NULL,
    destino TEXT NOT NULL,
    area_origem_id TEXT NOT NULL,
    usuario_responsavel TEXT NOT NULL,
    FOREIGN KEY (id_catalogo_produto) REFERENCES produtos_catalogo(id_produto),
    FOREIGN KEY (area_origem_id) REFERENCES areas_armazem(id_area),
    FOREIGN KEY (usuario_responsavel) REFERENCES usuarios(username)
);