# ES2 Bicicletario Externo (Elixir)

Pequeno microserviço em Elixir (Plug + Cowboy) com:
- Endpoint GET /api/v1/hello -> {"message":"Olá, mundo!"}
- Arquitetura básica (Router + Controller)
- Teste automatizado (ExUnit + Plug.Test)
- Lint (Credo)
- CI no GitHub Actions (formatação, lint, testes, cobertura)
- Integração opcional com SonarCloud
- Dockerfile para deploy simples

Como rodar localmente
- Requer Elixir >= 1.15 e Erlang/OTP 26
- Instale deps: mix deps.get
- Rodar: mix run --no-halt  (ou iex -S mix)
- Acesse: http://localhost:4000/api/v1/hello

Testes
- mix test
- Cobertura: MIX_ENV=test mix coveralls.html (gera cover/)

CI/Sonar
- Configure secret SONAR_TOKEN no repositório (se usar SonarCloud)
- Edite sonar-project.properties com projectKey/organization

Deploy com Docker
- docker build -t es2-bicicletario-externo .
- docker run -p 4000:4000 -e PORT=4000 es2-bicicletario-externo

Estrutura
- lib/es2_bicicletario_externo/router.ex
- lib/es2_bicicletario_externo/controllers/hello_controller.ex
- test/hello_test.exs

Licença
MIT
