function abrirDetalhesAgendamento(id) {
    const modal = document.getElementById('modalDetalhes');
    const loading = document.getElementById('modalLoading');
    const conteudoFinal = document.getElementById('modalConteudoFinal');

    // Abrir modal imediatamente
    modal.classList.remove('hidden');
    loading.classList.remove('hidden');
    conteudoFinal.classList.add('hidden');

    fetch(`${urlDetalhesAgendamentoBase}${id}/`, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => {
        if (!response.ok) throw new Error("Erro ao carregar detalhes.");
        return response.text();
    })
    .then(html => {
        loading.classList.add('hidden');
        conteudoFinal.innerHTML = html;
        conteudoFinal.classList.remove('hidden');

        // Adiciona evento de envio AJAX se houver formulário
        const form = document.getElementById('formEditarAgendamento');
        if (form && !form.hasAttribute('data-listener')) {
            form.addEventListener('submit', enviarFormularioAjax);
            form.setAttribute('data-listener', 'true'); // evita múltiplos listeners
        }
    })
    .catch(err => {
        loading.innerHTML = `<p class="text-red-600">Erro ao carregar os detalhes.</p>`;
        console.error(err);
    });
}

function enviarFormularioAjax(event) {
    event.preventDefault();
    const form = event.target;
    const url = form.getAttribute('action') || window.location.href;
    const formData = new FormData(form);

    fetch(url, {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const mensagemDiv = document.getElementById('mensagemModal');
        if (mensagemDiv) mensagemDiv.classList.remove('hidden');

        if (data.success) {
            mensagemDiv.textContent = data.message;

            // Atualiza título na tabela
            const agCard = document.querySelector(`[data-id="${data.id}"]`);
            if (agCard) agCard.textContent = data.titulo;
        } else {
            if (mensagemDiv) {
                mensagemDiv.classList.remove('text-green-600');
                mensagemDiv.classList.add('text-red-600');
                mensagemDiv.textContent = "Erro ao salvar. Verifique os campos.";
            }
        }
    })
    .catch(err => console.error(err));
}

function fecharModalDetalhes() {
    const modal = document.getElementById('modalDetalhes');
    modal.classList.add('hidden');
}

// Fechar modal ao clicar no X ou fora do conteúdo
document.getElementById('fecharDetalhes').addEventListener('click', fecharModalDetalhes);
window.addEventListener('click', (e) => {
    const modal = document.getElementById('modalDetalhes');
    const conteudo = document.getElementById('conteudoModal');
    if (e.target === modal) fecharModalDetalhes();
});