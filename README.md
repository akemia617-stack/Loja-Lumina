# 🍰 Loja Lumina

Aplicação web em Flask para uma loja de **doces e salgados**. Os clientes podem navegar pelo catálogo, filtrar por categoria e buscar produtos pelo nome ou descrição.

## Funcionalidades

- Página inicial com produtos em destaque
- Catálogo completo com filtro por categoria (doces ou salgados)
- Busca por termo
- Indicação de produtos indisponíveis
- Preços formatados em reais (R$)
- API JSON para consulta de produtos

## Tecnologias

- Python 3.10+
- Flask 3
- HTML, CSS e JavaScript
- pytest (testes)

## Estrutura do projeto

```
loja-lumina/
├── README.md
├── requirements.txt
├── .gitignore
├── docs/
│   └── requisitos.md
├── src/
│   ├── app.py
│   ├── routes/
│   │   └── __init__.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   └── catalogo.html
│   └── static/
│       ├── css/style.css
│       ├── js/main.js
│       └── img/
├── tests/
│   └── test_app.py
└── notebooks/
    └── README.md
```

## Como executar

1. Clone o repositório e entre na pasta:

   ```bash
   cd loja-lumina
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv

   # Linux / macOS
   source .venv/bin/activate

   # Windows
   .venv\Scripts\activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Inicie a aplicação:

   ```bash
   python src/app.py
   ```

5. Acesse no navegador: <http://127.0.0.1:5000>

## Rotas

### Páginas

| Rota | Descrição |
|------|-----------|
| `/` | Página inicial com destaques |
| `/catalogo` | Catálogo completo |
| `/catalogo?categoria=doces` | Filtra por categoria (`doces` ou `salgados`) |
| `/catalogo?q=coxinha` | Busca por termo |

### API

| Rota | Descrição |
|------|-----------|
| `GET /api/produtos` | Lista produtos (aceita `categoria` e `q`) |
| `GET /api/produtos/<id>` | Retorna um produto pelo ID |

Exemplo de resposta de `/api/produtos/1`:

```json
{
  "id": 1,
  "nome": "Brigadeiro Gourmet",
  "categoria": "doces",
  "descricao": "Brigadeiro de chocolate belga com granulado crocante.",
  "preco": 4.5,
  "imagem": "placeholder.png",
  "disponivel": true
}
```

## Testes

```bash
pytest
```

## Configuração

- Troque a `SECRET_KEY` em `src/app.py` antes de colocar a aplicação em produção.
- Coloque as imagens dos produtos em `src/static/img/` e ajuste o campo `imagem` de cada produto.
- O catálogo está em memória. Para uso real, substitua por um banco de dados (por exemplo, SQLite com SQLAlchemy).

## Próximos passos

- Carrinho de compras
- Pedidos e pagamento
- Painel administrativo para cadastrar produtos
- Migração do catálogo para banco de dados
- Organização das rotas em Blueprints (`src/routes/`)

## Licença

Defina a licença do projeto (por exemplo, MIT).
