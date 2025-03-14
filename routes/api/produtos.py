from flask import Blueprint, jsonify, request
from services.produtomanager import ProdutoManager
from data.json_manager import carregar_lista
from util.logger_util import get_logger

produto_bp=Blueprint("produto", __name__)

manager =ProdutoManager()

routelog = get_logger("produto_routes")

"""
    ROTAS PRODUTOS:
    - /produto/ (GET)       - Listar os Clientes
    - /produto/ (POST)      - Adicionar novo produto
    - /produto/<id>/remover - Remover produto
    - /produto/<id>/editar  - Editar produto


"""

@produto_bp.route("/produtos", methods=["GET"])
def lista_produtos():
    try:
        routelog.info("Requisição GET para listar produtos.")
        produtos = carregar_lista()  # Agora sempre busca a versão mais recente
        return jsonify(produtos), 200
    except Exception as e:
        routelog.error(f"Erro ao listar produtos: {str(e)}")
        return jsonify({"erro": "Erro ao carregar produtos."}), 500


@produto_bp.route("/novo", methods=["POST"])
def adicionar_produto():
    try:
        data = request.get_json()
        routelog.debug(f"Recebendo dados para novo produto: {data}")

        nome_produto = data.get("nome")
        preco = data.get("preco")

        if not nome_produto or preco is None:
            routelog.warning("Tentativa de adicionar produto com dados inválidos.")
            return jsonify({"erro": "Nome e preço são obrigatórios."}), 400

        preco = float(preco)

        manager.adicionar_produto(nome_produto, preco)
        routelog.info(f"Produto adicionado com sucesso: {nome_produto}")

        return jsonify({"mensagem": "Produto adicionado com sucesso!"}), 201

    except ValueError:
        routelog.warning("Erro ao converter preço para número.")
        return jsonify({"erro": "O preço deve ser um número válido."}), 400

    except Exception as e:
        routelog.error(f"Erro ao adicionar produto: {str(e)}")
        return jsonify({"erro": "Erro ao adicionar produto."}), 500

@produto_bp.route("/<int:id>/remover", methods=["DELETE"])
def remover_produto(id):
    try:
        produtos_antes = len(manager.listaprodutos)
        manager.remover_produto_id(id)

        if len(manager.listaprodutos) < produtos_antes:
            routelog.info(f"Produto removido com sucesso: ID {id}")
            return jsonify({"mensagem": "Produto removido com sucesso!"}), 200
        else:
            routelog.warning(f"Tentativa de remover produto inexistente: ID {id}")
            return jsonify({"erro": "Produto não encontrado."}), 404

    except Exception as e:
        routelog.error(f"Erro ao remover produto: {str(e)}")
        return jsonify({"erro": "Erro ao remover produto."}), 500

@produto_bp.route("/<int:id>/editar", methods=["PUT"])
def atualizar_produto(id):
    try:
        data = request.get_json()
        novo_nome = data.get("nome")
        novo_preco = data.get("preco")

        if not novo_nome and novo_preco is None:
            routelog.warning(f"Tentativa de atualização sem dados válidos: ID {id}")
            return jsonify({"erro": "Nome ou preço devem ser informados."}), 400

        atualizado = manager.atualizar_produto(id, novo_nome, novo_preco)

        if not atualizado:
            routelog.warning(f"Tentativa de atualizar produto inexistente: ID {id}")
            return jsonify({"erro": "Produto não encontrado."}), 404

        routelog.info(f"Produto atualizado: ID {id}, Nome: {novo_nome}, Preço: {novo_preco}")
        return jsonify({"mensagem": "Produto atualizado com sucesso!"}), 200

    except ValueError:
        routelog.warning("Erro ao converter preço para número.")
        return jsonify({"erro": "O preço deve ser um número válido."}), 400

    except Exception as e:
        routelog.error(f"Erro ao atualizar produto: {str(e)}")
        return jsonify({"erro": "Erro ao atualizar produto."}), 500



