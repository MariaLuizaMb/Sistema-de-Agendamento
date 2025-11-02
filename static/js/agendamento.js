function abrirDetalhesAgendamento(id) {
    fetch(`{% url 'detalhes_agendamento' 0 %}`.replace('/0/', `/${id}/`), {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => {
        if (!response.ok) throw new Error("Erro ao carregar detalhes.");
        return response.text();
    })
    .then(html => {
        const modal = document.getElementById('modalDetalhes');
        modal.innerHTML = html; // substitui conteúdo
        modal.classList.remove('hidden');

        const conteudo = document.getElementById('conteudoModal');
        setTimeout(() => conteudo.classList.replace('scale-95', 'scale-100'), 10);

        const form = document.getElementById('formEditarAgendamento');
        if (form) form.addEventListener('submit', enviarFormularioAjax);
    })
    .catch(err => console.error(err));
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
        mensagemDiv.classList.remove('hidden');

        if (data.success) {
            mensagemDiv.textContent = data.message;

            const agCard = document.querySelector(`[data-id="${data.id}"]`);
            if (agCard) {
                agCard.querySelector("p.font-bold").textContent = data.titulo;
                agCard.querySelector("p:nth-child(2)").textContent = `${data.data} às ${data.horario}`;
            }
        } else {
            mensagemDiv.classList.add('text-red-600');
            mensagemDiv.textContent = "Erro ao salvar. Verifique os campos.";
        }
    })
    .catch(err => console.error(err));
}

function fecharModal() {
    const modal = document.getElementById('modalDetalhes');
    const conteudo = document.getElementById('conteudoModal');
    conteudo.classList.replace('scale-100', 'scale-95');
    setTimeout(() => modal.classList.add('hidden'), 150);
}

document.addEventListener('click', function(e) {
    const modal = document.getElementById('modalDetalhes');
    if (e.target === modal) fecharModal();
});
