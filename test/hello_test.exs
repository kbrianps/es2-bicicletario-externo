defmodule OlaMundoPm.HelloTest do
  use ExUnit.Case, async: true
  import Plug.Test

  @opts OlaMundoPm.Router.init([])

  test "GET /api/v1/hello returns Olá, mundo!" do
    conn = conn(:get, "/api/v1/hello") |> OlaMundoPm.Router.call(@opts)
    assert conn.status == 200
    assert Jason.decode!(conn.resp_body) == %{"message" => "Olá, mundo!"}
  end
end
