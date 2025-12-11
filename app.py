from flask import Flask, render_template, request, url_for, redirect
from parser import convert_expression_in_PA

app = Flask(__name__)

automato_global = None
expressao_global = None
response_global = None

@app.route("/", methods=["GET", "POST"])
def home():
    global automato_global
    global expressao_global
    
    valor = None
    response = None
    
    if request.method == "POST":
        valor = request.form.get("expression")

        response, automato = convert_expression_in_PA(valor, "expression.jflap")

        if not response:
            return render_template("index.html", erro=True)

        automato_global = automato
        expressao_global = valor
        response_global = response

    return render_template(
        "index.html",
        valor_usuario=(valor is not None),
        valor_infixo=valor,
        valor_postfixo=response,
        automata_output=url_for("static", filename="automata_output.png"),
        arquivo_jflap=url_for("static", filename="expression.jflap"),
    )



@app.route("/testar", methods=["GET", "POST"])
def testar():
    global automato_global
    global expressao_global
    global response_global
    if response_global == False:
        return render_template(
            "index.html",
            erro_autômato=True,
            valor_usuario=False,
            response=response_global,
            expressao_infixa = expressao_global
        )

    if automato_global is None:
        return redirect(url_for("home"))
    
    resultados = []
    palavra_unica = ""
    palavras_multiplas = ""
    if request.method == "POST":

        palavra_unica = request.form.get("palavra_unica", "").strip()
        palavras_multiplas = request.form.get("palavras_multiplas", "").strip()

        lista = []

        if palavra_unica:
            lista.append(palavra_unica)

        if palavras_multiplas:
            for linha in palavras_multiplas.split("\n"):
                linha = linha.strip()
                if linha:
                    lista.append(linha)

        for palavra in lista:
            aceita = automato_global.execute(palavra)
            resultados.append({
                "palavra": palavra,
                "aceita": aceita,
            })

    return render_template(
        "testar.html",
        resultados=resultados,
        expressao_infixa=expressao_global,
        palavra_unica=palavra_unica,
        palavras_multiplas=palavras_multiplas
    )


@app.route("/documentacao")
def documentacao():
    return render_template("documentacao.html")

@app.route("/api/testar_vazio")
def api_testar_vazio():
    global automato_global

    if not automato_global:
        return {"erro": True, "mensagem": "Nenhum autômato carregado."}

    aceita = automato_global.execute("")

    return {"erro": False, "aceita": aceita}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

