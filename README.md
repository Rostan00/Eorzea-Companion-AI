# Eorzea Companion AI

Companheiro de IA autônomo inspirado no mundo e na atmosfera de Eorzea.

O projeto busca construir um personagem persistente, com personalidade coerente, memória de longo prazo, interação por voz, objetivos pessoais e capacidade de agir de forma autônoma dentro de uma **simulação controlada e separada**.

## Princípios do projeto

- **Personagem em primeiro lugar:** identidade, personalidade, relacionamentos e continuidade importam tanto quanto o modelo por baixo.
- **Memória persistente:** preservar experiências significativas sem tratar toda conversa como memória permanente.
- **Autonomia limitada:** o agente pode planejar e agir apenas dentro de ambientes e ferramentas explicitamente permitidos.
- **Amigável à nuvem:** manter o serviço principal implantável remotamente para não consumir recursos do PC do usuário o tempo todo.
- **Integração segura:** este projeto **não** automatiza, lê estado interno, injeta código ou controla o cliente oficial do Final Fantasy XIV. Qualquer integração futura com o cliente oficial exigiria autorização explícita da Square Enix.

## Arquitetura inicial

- Backend em Python + FastAPI
- Núcleo do agente para percepção, decisões e planejamento
- Configuração de personalidade e personagem
- Memória persistente (SQLite agora; PostgreSQL/vetores depois)
- Provedor de LLM plugável
- Interface de voz (speech-to-text e text-to-speech)
- Simulação independente para testar autonomia

Veja [docs/architecture.md](docs/architecture.md), [docs/personality.md](docs/personality.md) e [docs/memory.md](docs/memory.md).

## Roadmap de desenvolvimento

1. Estabelecer backend e configuração.
2. Implementar chat e a primeira versão da persona do personagem.
3. Adicionar memória episódica persistente.
4. Adicionar objetivos, planejamento e comportamento autônomo limitado.
5. Adicionar interação por voz.
6. Construir uma pequena simulação independente e avaliar o comportamento.
7. Implantar o serviço em ambiente de nuvem.

## Status atual

**Marco 1 concluído** — base funcional criada  
**Marco 2 concluído** — memória episódica:

- API FastAPI com endpoints `/health`, `/chat`, `/memories`
- Sistema de persona carregável (**Lauda** — Au'Ra)
- Interface de LLM com implementação mock
- Memória persistente (SQLite): episódica, semântica e de objetivos
- Extração automática de fatos da conversa
- Recuperação de memórias relevantes no contexto do chat
- Testes da API e do módulo de memória
- Documentação em português brasileiro

## Como rodar localmente

```bash
# Clone o repositório
git clone https://github.com/Rostan00/Eorzea-Companion-AI.git
cd Eorzea-Companion-AI

# Crie e ative o ambiente virtual
cd backend
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Instale as dependências
pip install -r requirements.txt

# Rode o servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A documentação interativa da API fica disponível em:  
http://localhost:8000/docs

### Exemplos de uso

**Verificar saúde do serviço:**
```bash
curl http://localhost:8000/api/v1/health
```

**Conversar com a Lauda:**
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Bora fazer uma dungeon hoje?"}'
```

**Listar memórias:**
```bash
curl http://localhost:8000/api/v1/memories
```

## Estrutura do projeto

```text
Eorzea-Companion-AI/
├── backend/
│   ├── app/
│   │   ├── api/          # Rotas e schemas
│   │   ├── character/    # Persona e identidade
│   │   ├── core/         # Configurações
│   │   ├── llm/          # Provedores de LLM
│   │   ├── memory/       # Memória episódica/semântica
│   │   └── main.py       # Entrada da aplicação
│   ├── requirements.txt
│   └── .env.example
├── docs/
│   ├── architecture.md
│   ├── personality.md
│   └── memory.md
├── tests/
│   ├── test_api.py
│   └── test_memory.py
└── README.md
```

## Personagem atual

**Lauda** — aventureira Au'Ra, direta, objetiva e com desejo claro de evoluir no jogo. Fala o que pensa e prioriza jogar junto (dungeons, crafting, Island Sanctuary, Occult Crescent, etc.).

Mais detalhes em [docs/personality.md](docs/personality.md).

## Licença

A definir.
