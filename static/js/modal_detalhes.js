document.addEventListener("DOMContentLoaded", function () {
  const modalDetalhes = document.getElementById("modalDetalhes");
  const conteudoModal = document.getElementById("conteudoModalDetalhes");

  // Funções utilitárias visuais (se não estiverem globais ainda)
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

  // Torna global para ser chamado pelo onclick da tabela
  window.abrirDetalhesAgendamento = async function (id) {
    if (!modalDetalhes || !conteudoModal) return;

    // 1. Mostra o modal com estado de carregamento
    conteudoModal.innerHTML = `
            <div class="flex flex-col items-center justify-center py-12 text-gray-500">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-900 mb-4"></div>
                <p>Carregando detalhes...</p>
            </div>
        `;
    showModal(modalDetalhes);

    try {
      // Usa a variável global definida no template ou monta a URL aqui se preferir
      // Assumindo que você tem a const urlDetalhesAgendamentoBase no seu HTML
      const url =
        typeof urlDetalhesAgendamentoBase !== "undefined"
          ? urlDetalhesAgendamentoBase + id + "/"
          : `/agendamentos/detalhes/${id}/`; // Fallback se a variável não existir

      const response = await fetch(url);

      if (!response.ok) throw new Error("Erro ao carregar dados");

      const html = await response.text();
      conteudoModal.innerHTML = html;
    } catch (error) {
      console.error("Erro:", error);
      conteudoModal.innerHTML = `
                <div class="text-center py-8">
                    <p class="text-red-500 mb-4">Não foi possível carregar os detalhes.</p>
                    <button onclick="fecharModalDetalhes()" class="px-4 py-2 bg-gray-200 rounded-lg">Fechar</button>
                </div>
            `;
    }
  };

  window.fecharModalDetalhes = function () {
    if (modalDetalhes) hideModal(modalDetalhes);
  };

  // Fecha ao clicar fora
  if (modalDetalhes) {
    modalDetalhes.addEventListener("click", (e) => {
      if (e.target === modalDetalhes) window.fecharModalDetalhes();
    });
  }
});
