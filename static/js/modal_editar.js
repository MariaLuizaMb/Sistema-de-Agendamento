document.addEventListener("DOMContentLoaded", function () {
  const modalEditar = document.getElementById("modalEditar");
  const formEditar = document.getElementById("formEditar");

  // --- Funções Utilitárias de Visualização (Reutilize se já tiver em outro lugar comum) ---
  function showModal(modal) {
    modal.classList.remove("hidden", "opacity-0");
    modal.classList.add("flex", "opacity-100");
  }

  function hideModal(modal) {
    modal.classList.remove("opacity-100", "opacity-100"); // Garante que remove a opacidade total
    modal.classList.add("opacity-0");
    setTimeout(() => {
      modal.classList.add("hidden");
      modal.classList.remove("flex");
    }, 300); // Tempo deve bater com a classe duration-300 do Tailwind
  }

  // Torna as funções globais para serem chamadas pelos botões onclick no HTML
  window.abrirModalEditar = async function (id) {
    if (!modalEditar) return;

    try {
      // Mostra um loading ou desabilita enquanto carrega (opcional)
      // modalEditar.querySelector('.modal-content').classList.add('opacity-50');

      const response = await fetch(`/agendamentos/editar-modal/${id}/`);
      if (!response.ok) throw new Error("Falha na requisição");

      const data = await response.json();

      if (data.success) {
        document.getElementById("editId").value = data.id;
        document.getElementById("editNome").value = data.nome;
        document.getElementById("editData").value = data.data;
        document.getElementById("editHora").value = data.hora_inicio;

        showModal(modalEditar);
      } else {
        alert(data.error || "Erro ao carregar dados do agendamento.");
      }
    } catch (error) {
      console.error("Erro ao buscar dados para edição:", error);
      alert("Erro de conexão. Não foi possível abrir a edição.");
    }
  };

  window.fecharModalEditar = function () {
    if (modalEditar) hideModal(modalEditar);
  };

  // Fecha ao clicar fora do conteúdo do modal
  if (modalEditar) {
    modalEditar.addEventListener("click", (e) => {
      if (e.target === modalEditar) window.fecharModalEditar();
    });
  }

  // --- Submissão do Formulário de Edição ---
  if (formEditar) {
    formEditar.addEventListener("submit", async function (e) {
      e.preventDefault();

      const id = document.getElementById("editId").value;
      const submitBtn = formEditar.querySelector('button[type="submit"]');
      const originalBtnText = submitBtn.innerText;

      // Feedback visual de carregamento
      submitBtn.disabled = true;
      submitBtn.innerText = "Salvando...";

      const formData = {
        nome: document.getElementById("editNome").value,
        data: document.getElementById("editData").value,
        hora_inicio: document.getElementById("editHora").value,
      };

      try {
        const response = await fetch(`/agendamentos/editar-modal/${id}/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
              .value,
          },
          body: JSON.stringify(formData),
        });

        const result = await response.json();

        if (result.success) {
          // Opcional: mostrar um toast de sucesso antes de recarregar
          window.location.reload();
        } else {
          alert("Erro ao salvar: " + (result.error || "Verifique os dados."));
        }
      } catch (error) {
        console.error("Erro ao salvar edição:", error);
        alert("Erro de conexão ao tentar salvar.");
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerText = originalBtnText;
      }
    });
  }
});
