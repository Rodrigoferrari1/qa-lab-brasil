# QA Games 3.4.0 - Etapa 2 (candidata de teste)

Base: 3.4.0 Etapa 1 com correção de navegação validada visualmente pelo usuário.

Escopo: apenas assets/js/qa-games.js e query de cache no index.html.

- Navegação entre jogos reinicia a questão no primeiro desafio.
- Resposta correta registra XP apenas uma vez por desafio.
- Resposta incorreta apresenta explicação e permite nova tentativa.
- A última questão apresenta tela de conclusão, sem reiniciar automaticamente.
- Botões para jogar novamente e consultar progresso.
- Progresso armazenado localmente; falha de armazenamento não impede jogar.

Validação técnica: node --check; inspeção dos fluxos de pontuação, respostas e navegação.
Pendente: homologação funcional web/mobile em navegador real.
Não é uma release aprovada para produção.
