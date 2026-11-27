# Sistema de Memória

## Objetivo

Dar continuidade real à Lauda: ela deve lembrar de preferências, metas e momentos importantes das conversas, sem tratar *tudo* como memória permanente.

## Tipos de memória

| Tipo       | Uso                                      | Exemplo                                      |
|------------|------------------------------------------|----------------------------------------------|
| episodic   | Eventos e momentos vividos juntos        | "Wipeamos no trial de ontem"                 |
| semantic   | Fatos e preferências estáveis            | "Main é Dark Knight" / "Gosta de Island"     |
| goal       | Objetivos declarados                     | "Quero upar Culinarian até 90"               |

## Como funciona hoje

1. **Armazenamento:** SQLite local (`data/memories.db` por padrão).
2. **Extração automática:** heurísticas simples na mensagem do usuário (preferências, metas, eventos).
3. **Recuperação:** busca por palavras-chave + ranking por importância e uso.
4. **Injeção no contexto:** as memórias mais relevantes entram no system prompt da Lauda antes da geração da resposta.

## Endpoints

- `GET /api/v1/health` — inclui `memory_count`
- `POST /api/v1/chat` — recupera memórias, responde e grava novas quando fizer sentido
- `GET /api/v1/memories` — lista memórias recentes
- `POST /api/v1/memories` — cria memória manualmente

## Limitações atuais (e próximos passos)

- Busca ainda é lexical (sem embeddings / vetores).
- Extração é baseada em regras; depois pode usar o próprio LLM para decidir o que vale lembrar.
- Não há esquecimento ativo nem consolidação (sumarização de memórias antigas).

Próximas melhorias naturais:

1. Extração de memórias via LLM (mais precisa).
2. Embeddings + busca semântica.
3. Política de esquecimento / consolidação.
4. Separar memórias da Lauda vs memórias sobre o jogador de forma mais explícita.
