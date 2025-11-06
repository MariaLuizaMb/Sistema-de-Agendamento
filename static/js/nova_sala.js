console.log('JS de Salas carregado');

document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('modalSala');
    const abrir = document.getElementById('abrirModalSala');
    const fechar = document.getElementById('fecharModalSala');
    const cancelar = document.getElementById('cancelarSalaBtn');
    const form = document.getElementById('formSala');
    const tbody = document.querySelector('tbody');
    const toastSucesso = document.getElementById('toast-sucesso');
    const toastErro = document.getElementById('toast-erro');
    const submitBtn = document.getElementById('submitSalaBtn');

    // ---- FUNÇÕES DE UI ----
    function show(el) {
        el.classList.remove('hidden', 'opacity-0');
        el.classList.add('flex', 'opacity-100');
        document.body.classList.add('overflow-hidden');
    }

    function hide(el) {
        el.classList.remove('opacity-100');
        el.classList.add('opacity-0');
        setTimeout(() => {
            el.classList.add('hidden');
            el.classList.remove('flex');
            document.body.classList.remove('overflow-hidden');
        }, 250);
    }

    function mostrarToast(el, msg) {
        el.textContent = msg;
        show(el);
        setTimeout(() => hide(el), 3000);
    }

    function mostrarSucesso(msg) { mostrarToast(toastSucesso, msg || 'Sala criada com sucesso! ✅'); }
    function mostrarErro(msg) { mostrarToast(toastErro, msg || 'Erro ao criar sala. ❌'); }

    // ---- ABRIR / FECHAR MODAL ----
    if (abrir && modal) {
        abrir.addEventListener('click', () => {
            form.reset();
            show(modal);
            const primeiroCampo = modal.querySelector('input, select');
            if (primeiroCampo) primeiroCampo.focus();
        });
    }

    if (fechar) fechar.addEventListener('click', () => hide(modal));
    if (cancelar) cancelar.addEventListener('click', () => hide(modal));
    window.addEventListener('click', e => { if (e.target === modal) hide(modal); });

    // ---- SUBMISSÃO VIA AJAX ----
    if (form) {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();

            if (submitBtn) submitBtn.disabled = true;
            const formData = new FormData(form);

            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value },
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    // --- Atualiza tabela dinamicamente OU recarrega ---
                    if (tbody && data.sala) {
                        const row = `
                            <tr class="border-b border-white hover:bg-blue-900 hover:text-white">
                                <td class="px-5 py-2">${data.sala.id}</td>
                                <td class="px-5 py-2">${data.sala.nome}</td>
                                <td class="px-5 py-2">${data.sala.tipo_sala}</td>
                                <td class="px-5 py-2">${data.sala.capacidade}</td>
                            </tr>`;
                        tbody.insertAdjacentHTML('beforeend', row);
                    }

                    hide(modal);
                    mostrarSucesso();

                    // --- Aguarda o toast aparecer e recarrega ---
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);

                } else {
                    console.error(data);
                    if (data.errors && data.errors.nome) {
                        mostrarErro(data.errors.nome[0]);
                    } else {
                        mostrarErro('Erro ao salvar. Verifique os campos.');
                    }
                }
            } catch (error) {
                console.error(error);
                mostrarErro('Erro inesperado. ❌');
            } finally {
                if (submitBtn) submitBtn.disabled = false;
            }
        });
    }
});
