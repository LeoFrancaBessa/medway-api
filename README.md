# Desafio Medway - Backend

API desenvolvida em Django Rest Framework para submissão e consulta de resultados de exames.

## Funcionalidades

* **Criar submissão de exame (POST)**
  Recebe todas as respostas de um estudante para um exame, armazena no banco e calcula o número de acertos.

* **Consultar resultado do exame (GET)**
  Retorna o desempenho do estudante em um exame, incluindo total de questões, acertos, percentual e detalhamento das respostas.

## Estrutura do projeto

* `models.py` → Modelos principais (`ExamSubmission`, `ExamSubmissionAnswers`).
* `serializers/` → Validação de input.
* `services/` → Regras de negócio.
* `views.py` → Endpoints da API.

## Como rodar

1. Clone o repositório e instale as dependências:

   ```bash
   git clone <repo-url>
   cd <repo>
   pip install -r requirements.txt
   ```
2. Com o docker instalado, rode:
   
   ```docker compose up --build```
   Isso deve inicializá-lo na porta 8000

3. Use o ```python manage.py createsuperuser``` para criar um usuário e logar ```http://localhost:8000/admin```

3. Com o painel do admin, sinta-se livre para criar usuários(students), exames, questões e respostas para testar a API.

## Exemplos de uso

### Criar submissão de exame

```json
POST /exam_submission/

{
  "student_id": 1,
  "exam_id": 1,
  "answers": [
    {"question_id": 1, "answer_id": 1},
    {"question_id": 2, "answer_id": 3}
  ]
}
```

### Consultar resultado

```
GET /exam_submission/?student_id=1&exam_id=5
```

Resposta:

```json
{
  "submission_id": 7,
  "raw_score": 1,
  "total_questions": 2,
  "percentage": 50.0,
  "answers": [
    {
      "question_id": 10,
      "question_text": "Qual a capital da França?",
      "selected_answer_id": 55,
      "selected_answer_text": "Paris",
      "is_correct": true
    }
  ]
}
```

## Melhorias futuras

* Adicionar autenticação e permissões.
* Implementar cache em cenários de maior escala.
* Evoluir a camada de serviços para uma arquitetura mais próxima de Clean Architecture.
* Criar histórico de revisões de notas para lidar com mudanças de gabarito.