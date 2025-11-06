console.log("JS carregado");

document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("modalAgendamento");
  const abrir = document.getElementById("abrirModal");
  const fechar = document.getElementById("fecharModal");
  const cancelar = document.getElementById("cancelarBtn");
  const form = document.getElementById("formAgendamento");
  const tbody = document.querySelector("tbody");
  const toastSucesso = document.getElementById("toast-sucesso");
  const toastErro = document.getElementById("toast-erro");
  const submitBtn = document.getElementById("submitBtn");
  const pageContent = document.getElementById("pageContent");

  // Utilitários de UI
  function show(element) {
    element.classList.remove("hidden", "opacity-0");
    element.classList.add("flex", "opacity-100");
    document.body.classList.add("overflow-hidden");
    if (pageContent) pageContent.classList.add("modal-blurred-fallback");
    document.body.classList.add("overflow-hidden");
  }
  function hide(element) {
    element.classList.remove("opacity-100");
    element.classList.add("opacity-0");
    setTimeout(() => {
      element.classList.add("hidden");
      element.classList.remove("flex");
      document.body.classList.remove("overflow-hidden");
    }, 250);
  }
  function mostrarToast(elemento, mensagem) {
    elemento.textContent = mensagem;
    show(elemento);
    setTimeout(() => hide(elemento), 3000);
  }
  function mostrarSucesso(msg) {
    mostrarToast(toastSucesso, msg || "Agendamento criado com sucesso! ✅");
  }
  function mostrarErro(msg) {
    mostrarToast(toastErro, msg || "Erro ao salvar o agendamento. ❌");
  }

  // Abre/fecha modal (checagens para evitar erros se elementos não existem)
  if (abrir && modal) {
    abrir.addEventListener("click", () => {
      // limpar erros antigos...
      show(modal);
      const primeiroCampo = modal.querySelector(
        "input, select, textarea, button"
      );
      if (primeiroCampo) primeiroCampo.focus();
    });
  }
  if (fechar) fechar.addEventListener("click", () => hide(modal));
  if (cancelar) cancelar.addEventListener("click", () => hide(modal));
  window.addEventListener("click", (e) => {
    if (e.target === modal) hide(modal);
  });

  // Submissão AJAX segura
  if (form) {
    form.addEventListener("submit", async function (e) {
      e.preventDefault();
      if (!form.action) {
        mostrarErro("URL de submissão inválida.");
        return;
      }

      // desativa botão para evitar múltiplos envios
      if (submitBtn) submitBtn.disabled = true;

      const formData = new FormData(form);

      // ----- ADICIONE ESTAS LINHAS PARA DEPURAR -----
      console.log("--- Depurando FormData ---");
      console.log("Dados do formulário prestes a enviar:");
      for (let [key, value] of formData.entries()) {
        console.log(key, ":", value);
      }
      console.log("----------------------------");
      // limpa mensagens anteriores
      modal
        .querySelectorAll(".field-error")
        .forEach((el) => (el.textContent = ""));
      const globalErr = document.getElementById("form-error-global");
      if (globalErr) globalErr.textContent = "";

      try {
        const response = await fetch(form.action, {
          method: "POST",
          headers: {
            "X-CSRFToken":
              document.querySelector("[name=csrfmiddlewaretoken]")?.value || "",
          },
          body: formData,
        });

        // tenta parsear JSON, se falhar mostra erro genérico
        let data;
        try {
          data = await response.json();
        } catch (err) {
          throw new Error("Resposta inválida do servidor.");
        }

        if (data.success) {
          // adiciona linha se tbody existir
          if (tbody && data.agendamento) {
            const row = `
                            <tr class="border-b border-white hover:bg-blue-900 hover:text-white">
                                <td class="px-5 py-2">${
                                  data.agendamento.codigo_agendamento || ""
                                }</td>
                                <td class="px-5 py-2 cursor-pointer hover:underline"
                                    onclick="abrirDetalhesAgendamento('${
                                      data.agendamento.id || ""
                                    }')"
                                    data-id="${data.agendamento.id || ""}">
                                    ${data.agendamento.nome || ""}
                                </td>
                                <td class="px-5 py-2">${
                                  data.agendamento.sala || ""
                                }</td>
                                <td class="px-5 py-2">${
                                  data.agendamento.criador || ""
                                }</td>
                                <td class="px-5 py-2">${
                                  data.agendamento.hora_inicio || ""
                                }</td>
                                <td class="pl-5 py-2">${
                                  data.agendamento.data || ""
                                }</td>
                                <td class="px-5 py-2 flex gap-3 justify-center">
                                <button onclick="abrirModalEditar('${
                                  data.agendamento.id || ""
                                }')"
                                        class="hover:underline duration-200">
                                    ✏️
                                </button>
                                <button onclick="abrirModalExcluir('${
                                  data.agendamento.id || ""
                                }')"
                                        class="hover:underline duration-200">
                                    🗑️
                                </button>
                            </td>
                            </tr>
                        `;
            tbody.insertAdjacentHTML("beforeend", row);
          }
          form.reset();
          hide(modal);
          mostrarSucesso();
        } else {
          // suporta três formatos de erro esperados:
          // 1) data.error (string), 2) data.errors (dict de campo -> lista), 3) mensagens de validação genéricas
          if (data.errors && typeof data.errors === "object") {
            // mostra por campo se possível
            Object.keys(data.errors).forEach((field) => {
              const fieldEl = modal.querySelector(
                `.field-error[data-field="${field}"]`
              );
              if (fieldEl) {
                const msgs = Array.isArray(data.errors[field])
                  ? data.errors[field].join(" ")
                  : String(data.errors[field]);
                fieldEl.textContent = msgs;
              }
            });
            // se houver um não-campo, mostra no global
            if (data.error) {
              if (globalErr) globalErr.textContent = data.error;
              else mostrarErro(data.error);
            } else {
              if (globalErr)
                globalErr.textContent = "Verifique os campos do formulário.";
              else mostrarErro("Verifique os campos do formulário.");
            }
          } else if (data.error) {
            if (globalErr) globalErr.textContent = data.error;
            else mostrarErro(data.error);
          } else {
            mostrarErro("Erro ao salvar o agendamento. Verifique os campos.");
          }
        }
      } catch (error) {
        console.error("Erro na requisição:", error);
        mostrarErro("Erro inesperado. Tente novamente.");
      } finally {
        if (submitBtn) submitBtn.disabled = false;
      }
    });
  }
});

let agendamentoIdParaExcluir = null;

function abrirModalExcluir(id) {
  agendamentoIdParaExcluir = id;
  const modal = document.getElementById("modalExcluir");
  if (modal) {
    modal.classList.remove("hidden");
    modal.classList.add("flex");
  }
}

function fecharModalExcluir() {
  agendamentoIdParaExcluir = null;
  const modal = document.getElementById("modalExcluir");
  if (modal) {
    modal.classList.add("hidden");
    modal.classList.remove("flex");
  }
}

async function confirmarExclusao() {
  if (!agendamentoIdParaExcluir) return;

  try {
    const response = await fetch(
      `/agendamentos/excluir/${agendamentoIdParaExcluir}/`,
      {
        method: "DELETE",
        headers: {
          "X-CSRFToken":
            document.querySelector("[name=csrfmiddlewaretoken]")?.value ||
            getCookie("csrftoken"),
          "Content-Type": "application/json",
          "X-Requested-With": "XMLHttpRequest",
        },
      }
    );

    const data = await response.json();

    if (response.ok && data.success) {
      window.location.reload();
    } else {
      alert(data.error || "Erro ao excluir o agendamento.");
    }
  } catch (error) {
    console.error("Erro na exclusão:", error);
    alert("Erro de conexão com o servidor.");
  } finally {
    fecharModalExcluir();
  }
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
