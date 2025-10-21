defmodule OlaMundoPm.Application do
  @moduledoc false
  use Application

  def start(_type, _args) do
    children = [
      {Plug.Cowboy, scheme: :http, plug: OlaMundoPm.Router, options: [port: port()]}
    ]

    opts = [strategy: :one_for_one, name: OlaMundoPm.Supervisor]
    Supervisor.start_link(children, opts)
  end

  defp port do
    case System.get_env("PORT") do
      nil -> 4000
      p -> String.to_integer(p)
    end
  end
end
