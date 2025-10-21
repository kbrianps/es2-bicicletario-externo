defmodule OlaMundoPm.Router do
  @moduledoc false
  use Plug.Router
  use Plug.ErrorHandler

  alias OlaMundoPm.Controllers.HelloController
  alias Plug.Conn, as: Conn

  plug Plug.Logger
  plug :match
  plug Plug.Parsers, parsers: [:json], json_decoder: Jason
  plug :dispatch

  get "/health" do
    send_resp(conn, 200, "ok")
  end

  get "/api/v1/hello" do
    resp = HelloController.index()

    conn
    |> Conn.put_resp_content_type("application/json")
    |> send_resp(200, Jason.encode!(resp))
  end

  match _ do
    send_resp(conn, 404, "not_found")
  end

  @impl true
  def handle_errors(conn, %{reason: _reason}) do
    conn
    |> Conn.put_resp_content_type("application/json")
    |> send_resp(conn.status || 500, Jason.encode!(%{error: "internal_error"}))
  end
end
