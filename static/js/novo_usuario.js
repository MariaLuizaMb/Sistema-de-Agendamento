console.log('JS Usuários carregado');

document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('modalUsuario');
    const abrir = document.getElementById('abrirModal_usuario');
    const fechar = document.getElementById('fecharModalUsuario');
    const cancelar = document.getElementById('cancelarBtnUsuario');
    const form = document.getElementById('formUsuario');
    const tbody = document.querySelector('tbody');
    const toastSucesso = document.getElementById('toast-sucesso');
    const toastErro = document.getElementById('toast-erro');
    const submitBtn = document.getElementById('submitBtnUsuario');
    const pageContent = document.getElementById('pageContent');

    // --- UTILITÁRIOS DE UI ---
    function show(element) {
        element.classList.remove('hidden', 'opacity-0');
        element.classList.add('flex', 'opacity-100');
        document.body.classList.add('overflow-hidden');
        if (pageContent) pageContent.classList.add('modal-blurred-fallback');
    }
    function hide(element) {
        element.classList.remove('opacity-100');
        element.classList.add('opacity-0');
        setTimeout(() => {
            element.classList.add('hidden');
            element.classList.remove('flex');
            document.body.classList.remove('overflow-hidden');
        }, 250);
    }
    function mostrarToast(elemento, mensagem) {
        elemento.textContent = mensagem;
        show(elemento);
        setTimeout(() => hide(elemento), 3000);
    }
    function mostrarSucesso(msg) { mostrarToast(toastSucesso, msg || 'Usuário salvo com sucesso! ✅'); }
    function mostrarErro(msg) { mostrarToast(toastErro, msg || 'Erro ao salvar o usuário. ❌'); }

    // --- ABRIR / FECHAR MODAL ---
    if (abrir && modal) {
        abrir.addEventListener('click', () => {
            form.reset();
            form.action = form.dataset.createUrl; // URL padrão para criar
            submitBtn.textContent = 'Salvar';
            show(modal);
            const primeiroCampo = modal.querySelector('input, select, textarea');
            if (primeiroCampo) primeiroCampo.focus();
        });
    }
    if (fechar) fechar.addEventListener('click', () => hide(modal));
    if (cancelar) cancelar.addEventListener('click', () => hide(modal));
    window.addEventListener('click', (e) => { if (e.target === modal) hide(modal); });

    // --- SUBMISSÃO AJAX ---
    if (form) {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();

            if (!form.action) {
                mostrarErro("URL de submissão inválida.");
                return;
            }

            if (submitBtn) submitBtn.disabled = true;

            const formData = new FormData(form);
            modal.querySelectorAll('.field-error').forEach(el => el.textContent = '');
            const globalErr = document.getElementById('form-error-global');
            if (globalErr) globalErr.textContent = '';

            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
                    },
                    body: formData
                });

                let data;
                try {
                    data = await response.json();
                } catch {
                    throw new Error('Resposta inválida do servidor.');
                }

                if (data.success) {
                    // Atualiza tabela dinamicamente
                    if (tbody && data.usuario) {
                        const row = `
                            <tr class="hover:bg-blue-800 hover:text-white">
                                <td class="px-5 py-2">${data.usuario.id || ''}</td>
                                <td class="px-5 py-2 cursor-pointer hover:underline"
                                    onclick="abrirDetalhesUsuario('${data.usuario.username || ''}')"
                                    data-id="${data.usuario.id || ''}">
                                    ${data.usuario.username || ''}
                                </td>
                                <td class="px-5 py-2">${data.usuario.tipo_usuario || ''}</td>
                                <td class="px-5 py-2">${data.usuario.cargo || ''}</td>
                                <td class="px-5 py-2 flex rounded-r-xl gap-2">
                                    <button onclick="abrirModalEditar('${data.usuario.id || ''}')" 
                                            class="hover:underline duration-200">
                                        ✏️
                                    </button>
                                    <button onclick="abrirModalExcluir('${data.usuario.id || ''}')"
                                            class="hover:underline duration-200">
                                        🗑️
                                    </button>
                                </td>
                            </tr>
                        `;
                        // Se for edição, substitui linha existente
                        const existingRow = tbody.querySelector(`tr[data-id="${data.usuario.id}"]`);
                        if (existingRow) {
                            existingRow.outerHTML = row;
                        } else {
                            tbody.insertAdjacentHTML('beforeend', row);
                        }
                    }
                    form.reset();
                    hide(modal);
                    mostrarSucesso();
                } else {
                    // Tratamento de erros
                    if (data.errors && typeof data.errors === 'object') {
                        Object.keys(data.errors).forEach(field => {
                            const fieldEl = modal.querySelector(`.field-error[data-field="${field}"]`);
                            if (fieldEl) {
                                const msgs = Array.isArray(data.errors[field]) ? data.errors[field].join(' ') : String(data.errors[field]);
                                fieldEl.textContent = msgs;
                            }
                        });
                        if (data.error) {
                            if (globalErr) globalErr.textContent = data.error;
                            else mostrarErro(data.error);
                        } else {
                            mostrarErro('Verifique os campos do formulário.');
                        }
                    } else if (data.error) {
                        mostrarErro(data.error);
                    } else {
                        mostrarErro('Erro ao salvar o usuário. Verifique os campos.');
                    }
                }
            } catch (error) {
                console.error('Erro na requisição:', error);
                mostrarErro("Erro inesperado. Tente novamente.");
            } finally {
                if (submitBtn) submitBtn.disabled = false;
            }
        });
    }
});
