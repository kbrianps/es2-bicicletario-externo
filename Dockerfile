FROM elixir:1.15-slim

WORKDIR /app

ENV MIX_ENV=prod \
    LANG=C.UTF-8

RUN mix local.hex --force && mix local.rebar --force

COPY mix.exs mix.lock* ./
COPY config ./config

RUN mix deps.get --only prod && mix deps.compile

COPY lib ./lib

RUN mix compile

ENV PORT=4000
EXPOSE 4000

CMD ["sh", "-lc", "elixir --erl '-proto_dist inet_tcp' -S mix run --no-halt"]
