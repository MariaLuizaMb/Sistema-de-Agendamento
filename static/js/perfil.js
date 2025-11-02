document.addEventListener("DOMContentLoaded", () => {
    const formDados = document.getElementById("form-dados");
    const btnSalvar = document.getElementById("btn-salvar-dados");
    const formSenha = document.getElementById("form-senha");
    const btnSenha = document.getElementById("btn-alterar-senha");

    console.log("formDados, btnSalvar, formSenha, btnSenha =>", formDados, btnSalvar, formSenha, btnSenha);

    const mensagensDiv = document.getElementById("mensagens");

    function exibirMensagem(texto, tipo="success") {
        mensagensDiv.innerHTML = `<div class="p-3 mb-2 rounded ${tipo === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">${texto}</div>`;
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function enviarFormulario(form, nomeBotao, callback) {
        if (!form) {
            exibirMensagem("Formulário não encontrado.", "error");
            return;
        }

        const formData = new FormData(form);
        formData.append(nomeBotao, "true"); // identifica qual ação

        const csrf = formData.get('csrfmiddlewaretoken');
        if (!csrf) {
            exibirMensagem("Token CSRF não encontrado. Atualize a página.", "error");
            return;
        }

        fetch(window.location.href, {
            method: "POST",
            credentials: 'same-origin',
            headers: {
                'X-CSRFToken': csrf,
                // 'Accept': 'application/json' // opcional
            },
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Servidor retornou ${response.status}`);
            }
            return response.json().catch(() => { throw new Error("Resposta não é JSON"); });
        })
        .then(data => callback(data))
        .catch(error => {
            console.error("Erro fetch:", error);
            exibirMensagem("Erro ao enviar o formulário.", "error");
        });
    }

    if (btnSalvar) {
        btnSalvar.addEventListener("click", () => {
            enviarFormulario(formDados, "salvar_dados", (data) => {
                if (data.success) {
                    exibirMensagem("Dados salvos com sucesso!");
                } else {
                    const erros = data.errors ? Object.values(data.errors).flat().join("<br>") : "Erro desconhecido";
                    exibirMensagem(erros, "error");
                }
            });
        });
    }

    if (btnSenha) {
        btnSenha.addEventListener("click", () => {
            enviarFormulario(formSenha, "alterar_senha", (data) => {
                if (data.success) {
                    exibirMensagem("Senha alterada com sucesso!");
                    formSenha.reset();
                } else {
                    const erros = data.errors ? Object.values(data.errors).flat().join("<br>") : "Erro desconhecido";
                    exibirMensagem(erros, "error");
                }
            });
        });
    }
});
