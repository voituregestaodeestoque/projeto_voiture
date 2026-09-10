const ICONES = { estoque: '⚠️', entrada: '📥', saida: '📤' };

async function carregarNotificacoes() {
    try {
        const resposta = await fetch('/api/notificacoes');
        const dados = await resposta.json();

        const contador = document.getElementById('contador');
        const lista = document.getElementById('listaNotificacoes');

        if (dados.total > 0) {
            contador.textContent = dados.total;
            contador.style.display = 'inline-block';
        } else {
            contador.style.display = 'none';
        }

        lista.innerHTML = '';
        if (dados.total === 0) {
            lista.innerHTML = '<li class="notif-vazio">Nenhuma notificação</li>';
        } else {
            dados.notificacoes.forEach(n => {
                const item = document.createElement('li');
                item.textContent = `${ICONES[n.tipo] || '🔔'} ${n.mensagem}`;
                lista.appendChild(item);
            });
        }
    } catch (erro) {
        console.error('Erro ao carregar notificações:', erro);
    }
}

document.getElementById('btnNotificacoes').addEventListener('click', (e) => {
    e.stopPropagation();
    document.getElementById('painelNotificacoes').classList.toggle('aberto');
});

document.addEventListener('click', (e) => {
    const painel = document.getElementById('painelNotificacoes');
    const botao = document.getElementById('btnNotificacoes');
    if (!painel.contains(e.target) && !botao.contains(e.target)) {
        painel.classList.remove('aberto');
    }
});

document.getElementById('btnLimpar').addEventListener('click', async () => {
    await fetch('/api/notificacoes', { method: 'DELETE' });
    carregarNotificacoes();
});

carregarNotificacoes();
setInterval(carregarNotificacoes, 30000);