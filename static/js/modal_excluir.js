document.addEventListener("DOMContentLoaded", function () {
  const modalExcluir = document.getElementById("modalExcluir");
  const inputIdExcluir = document.getElementById("idExcluir");
  const btnConfirmar = modalExcluir
    ? modalExcluir.querySelector("button.bg-red-600")
    : null;

  // --- Funções Visuais (Reutilizando o padrão) ---
  function showModal(modal) {
    modal.classList.remove("hidden", "opacity-0");
    modal.classList.add("flex", "opacity-100");
  }

  function hideModal(modal) {
    modal.classList.remove("opacity-100");
    modal.classList.add("opacity-0");
    setTimeout(() => {
      modal.classList.add("hidden");
      modal.classList.remove("flex");
    }, 300);
  }

  // --- Funções Globais (chamadas pelo onclick no HTML) ---
  window.abrirModalExcluir = function (id) {
    if (modalExcluir && inputIdExcluir) {
      inputIdExcluir.value = id;
      showModal(modalExcluir);
    }
  };

  window.fecharModalExcluir = function () {
    if (modalExcluir) {
      hideModal(modalExcluir);
      if (inputIdExcluir) inputIdExcluir.value = ""; // Limpa o ID ao fechar
    }
  };

  window.confirmarExclusao = async function () {
    const id = inputIdExcluir.value;
    if (!id) return;

    // Feedback visual no botão
    const textoOriginal = btnConfirmar ? btnConfirmar.innerText : "Excluir";
    if (btnConfirmar) {
      btnConfirmar.disabled = true;
      btnConfirmar.innerText = "Excluindo...";
    }

    try {
      const response = await fetch(`/agendamentos/excluir/${id}/`, {
        method: "DELETE",
        headers: {
          "X-CSRFToken":
            document.querySelector("[name=csrfmiddlewaretoken]")?.value ||
            getCookie("csrftoken"),
          "Content-Type": "application/json",
          "X-Requested-With": "XMLHttpRequest",
        },
      });

      const data = await response.json();

      if (response.ok && data.success) {
        // Sucesso: recarrega a página
        window.location.reload();
      } else {
        alert(data.error || "Erro ao excluir o agendamento.");
      }
    } catch (error) {
      console.error("Erro na exclusão:", error);
      alert("Erro de conexão com o servidor.");
    } finally {
      // Restaura o botão se deu erro e o modal continuou aberto (raro, pois recarregamos no sucesso)
      if (btnConfirmar) {
        btnConfirmar.disabled = false;
        btnConfirmar.innerText = textoOriginal;
      }
      fecharModalExcluir();
    }
  };

  // Fecha ao clicar fora
  if (modalExcluir) {
    modalExcluir.addEventListener("click", (e) => {
      if (e.target === modalExcluir) window.fecharModalExcluir();
    });
  }

  // Função auxiliar para pegar o CSRF token de cookies se não houver form na página
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
});
