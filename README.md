# Controle de Reservas de Salas

API Flask para controle de reservas de salas, integrando com banco de dados Supabase.

## Endpoints

- **GET /**  
  Healthcheck ("OK")

- **GET /salas**  
  Lista todas as salas cadastradas.

- **GET /reservas?dia=YYYY-MM-DD**  
  Lista todas as reservas de um dia.

- **POST /reservas**  
  Cria uma nova reserva.  
  Exemplo de JSON:
  ```json
  {
    "sala_id": 1,
    "usuario_id": 1,
    "inicio": "2025-06-06T11:00:00Z",
    "fim": "2025-06-06T12:00:00Z",
    "assunto": "Reunião de Teste"
  }