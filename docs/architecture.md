# Arquitetura

## Objetivos

O companheiro deve se sentir como um personagem contínuo, e não apenas um chatbot sem estado. Ele precisa estar disponível através de um cliente leve, enquanto o raciocínio, a memória e trabalhos agendados podem rodar remotamente.

## Componentes de alto nível

```text
Cliente Desktop / Web
  |  chat, voz, notificações
  v
Backend FastAPI
  |
  +-- Núcleo do Agente
  |     +-- Percepção / montagem de contexto
  |     +-- Camada de decisão e políticas
  |     +-- Planejador / gerenciador de objetivos
  |
  +-- Personagem
  |     +-- Identidade e persona
  |     +-- Estado emocional / de relacionamento
  |
  +-- Memória
  |     +-- Memórias episódicas
  |     +-- Fatos semânticos
  |     +-- Recuperação e sumarização
  |
  +-- Adaptador de Provedor de LLM
  |
  +-- Ferramentas / Simulação Independente
        +-- Ações explicitamente permitidas
        +-- Estado observável e resultados das ações

PostgreSQL armazena o estado durável. Busca vetorial opcional pode ser
introduzida depois que o modelo básico de memória estiver funcionando.
```

## Stack proposta

| Área          | Escolha inicial              | Motivo                                      |
|---------------|------------------------------|---------------------------------------------|
| API           | Python + FastAPI             | API assíncrona simples e ecossistema maduro |
| Lógica do agente | Módulos Python puros      | Manter o comportamento inspecionável        |
| Banco de dados| PostgreSQL                   | Estado relacional durável                   |
| LLM           | Adaptador de provedor        | Evitar acoplamento a um único fornecedor    |
| Cliente       | Web primeiro; desktop depois | Iteração rápida                             |
| Voz           | Adaptadores STT e TTS separados | Provedores podem ser trocados facilmente |
| Deploy        | Docker                       | Ambientes locais e na nuvem reproduzíveis   |

## Ciclo de autonomia

1. Observar o estado atual da conversa ou da simulação.
2. Montar um contexto compacto a partir da persona, memória e objetivos atuais.
3. Decidir se uma resposta ou ação é apropriada.
4. Verificar a ação contra permissões e regras de segurança.
5. Executar apenas ações da lista de permissões na simulação independente.
6. Registrar o resultado e decidir se vale a pena lembrar.

## Limite de segurança

O sistema é projetado para conversa e simulação independente. Ele **não deve**:

- Automatizar gameplay
- Inspecionar memória de processo
- Injetar código
- Enviar inputs
- Controlar o cliente oficial do Final Fantasy XIV

Qualquer integração futura com o cliente oficial está fora de escopo, a menos que a Square Enix autorize explicitamente.

## Primeiro marco de implementação

Criar um serviço FastAPI mínimo com:

- Endpoint de saúde (`/health`)
- Endpoint de chat (`/chat`)
- Configuração de persona carregável
- Interface de provedor com implementação mock
- Testes para a API e limites de política

Memória, voz e simulação autônoma devem ser adicionadas de forma incremental depois que essa base estiver testável.
