"""
Loja Lumina - Doces e Salgados
Aplicação Flask para exibição de catálogo aos clientes.

Estrutura esperada (relativa a este arquivo, em src/):
    templates/  -> base.html, index.html, catalogo.html
    static/     -> css/style.css, js/main.js, img/

Executar:
    python src/app.py
"""

from dataclasses import dataclass, asdict
from decimal import Decimal
from pathlib import Path

from flask import Flask, abort, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent

CATEGORIAS = {
    "doces": "Doces",
    "salgados": "Salgados",
}


@dataclass(frozen=True)
class Produto:
    id: int
    nome: str
    categoria: str  # "doces" ou "salgados"
    descricao: str
    preco: Decimal
    imagem: str = "placeholder.png"  # arquivo dentro de static/img/
    disponivel: bool = True

    def to_dict(self) -> dict:
        dados = asdict(self)
        dados["preco"] = float(self.preco)
        return dados


# Catálogo em memória. Em produção, substituir por banco de dados.
PRODUTOS = [
    # Doces
    Produto(1, "Brigadeiro Gourmet", "doces",
            "Brigadeiro de chocolate belga com granulado crocante.", Decimal("4.50")),
    Produto(2, "Beijinho", "doces",
            "Clássico de coco cremoso coberto com açúcar cristal.", Decimal("4.00")),
    Produto(3, "Bolo de Cenoura com Chocolate", "doces",
            "Fatia generosa de bolo fofinho com cobertura de chocolate.", Decimal("9.90")),
    Produto(4, "Torta de Limão", "doces",
            "Massa amanteigada, creme de limão e merengue maçaricado.", Decimal("12.00")),
    Produto(5, "Pudim de Leite", "doces",
            "Pudim tradicional com calda de caramelo, fatia individual.", Decimal("8.50")),
    # Salgados
    Produto(6, "Coxinha de Frango", "salgados",
            "Massa macia recheada com frango desfiado e catupiry.", Decimal("7.00")),
    Produto(7, "Pastel de Carne", "salgados",
            "Pastel frito na hora com recheio de carne moída temperada.", Decimal("8.00")),
    Produto(8, "Empada de Palmito", "salgados",
            "Massa podre amanteigada com recheio cremoso de palmito.", Decimal("6.50")),
    Produto(9, "Esfiha de Queijo", "salgados",
            "Esfiha assada com mussarela derretida.", Decimal("6.00")),
    Produto(10, "Pão de Queijo", "salgados",
            "Porção com 5 unidades, quentinhos e crocantes por fora.", Decimal("9.00"),
            disponivel=False),
]


def filtrar_produtos(categoria: str | None = None, busca: str | None = None) -> list[Produto]:
    """Filtra os produtos por categoria e/ou termo de busca."""
    resultado = PRODUTOS

    if categoria:
        resultado = [p for p in resultado if p.categoria == categoria]

    if busca:
        termo = busca.strip().lower()
        resultado = [
            p for p in resultado
            if termo in p.nome.lower() or termo in p.descricao.lower()
        ]

    return resultado


def create_app(config: dict | None = None) -> Flask:
    """Application factory (facilita os testes em tests/test_app.py)."""
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )
    app.config.update(
        SECRET_KEY="troque-esta-chave-em-producao",
        NOME_LOJA="Loja Lumina",
        JSON_AS_ASCII=False,
    )
    if config:
        app.config.update(config)

    # ------------------------------------------------------------------
    # Filtros e contexto global dos templates
    # ------------------------------------------------------------------
    @app.template_filter("brl")
    def formatar_brl(valor) -> str:
        """Formata um valor numérico como moeda brasileira: R$ 1.234,50."""
        texto = f"{Decimal(valor):,.2f}"
        texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {texto}"

    @app.context_processor
    def injetar_globais():
        return {
            "nome_loja": app.config["NOME_LOJA"],
            "categorias": CATEGORIAS,
        }

    # ------------------------------------------------------------------
    # Rotas de páginas
    # ------------------------------------------------------------------
    @app.route("/")
    def index():
        destaques = [p for p in PRODUTOS if p.disponivel][:4]
        return render_template("index.html", destaques=destaques)

    @app.route("/catalogo")
    def catalogo():
        categoria = request.args.get("categoria", "").strip().lower()
        busca = request.args.get("q", "").strip()

        if categoria and categoria not in CATEGORIAS:
            abort(404)

        produtos = filtrar_produtos(categoria or None, busca or None)
        return render_template(
            "catalogo.html",
            produtos=produtos,
            categoria_ativa=categoria,
            busca=busca,
        )

    # ------------------------------------------------------------------
    # API JSON (útil para o main.js: busca dinâmica, carrinho, etc.)
    # ------------------------------------------------------------------
    @app.route("/api/produtos")
    def api_produtos():
        categoria = request.args.get("categoria", "").strip().lower()
        busca = request.args.get("q", "").strip()

        if categoria and categoria not in CATEGORIAS:
            return jsonify({"erro": "Categoria inválida."}), 400

        produtos = filtrar_produtos(categoria or None, busca or None)
        return jsonify([p.to_dict() for p in produtos])

    @app.route("/api/produtos/<int:produto_id>")
    def api_produto(produto_id: int):
        produto = next((p for p in PRODUTOS if p.id == produto_id), None)
        if produto is None:
            return jsonify({"erro": "Produto não encontrado."}), 404
        return jsonify(produto.to_dict())

    # ------------------------------------------------------------------
    # Tratamento de erros
    # ------------------------------------------------------------------
    @app.errorhandler(404)
    def pagina_nao_encontrada(_erro):
        if request.path.startswith("/api/"):
            return jsonify({"erro": "Recurso não encontrado."}), 404
        return render_template("index.html", destaques=[], erro_404=True), 404

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
