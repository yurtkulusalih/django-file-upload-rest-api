# django-file-upload-rest-api

## Requirements

- Docker
- Docker Compose

## Initial Setup

Go under the `django-file-upload-rest-api` folder and start the stack with Docker Compose:

```bash
docker-compose up --build (For the first run)
```

This will help to create database, tables as well as to install dependencies for the application. For further runs, you can use `docker-compose up (add -d to run it in detached mode)`.

## Testing

To run the unittests, you can use the following command:

```bash
docker exec -it file-upload-api python manage.py test
```

## Endpoints

Once the application started successfully, you can open your browser, navigate to Swagger UI - `http://localhost:8000/api/` and interact with the following URLs:

- [POST] `/file/upload/`: For file upload (only `.txt` files with `text/plain` content is allowed)

  - Names of the uploaded files should be unique.
  - The database stores only the metadata (e.g. `date of creation`, `id`, `path_to_content`) of an uploaded file and the file content is stored in the local filesystem. To access the uploaded files, you can check under `api/media/uploads`
  - Successful uploads should return `HTTP_201_CREATED`

  ```bash
  curl -X 'POST' \
  'http://localhost:8000/api/file/upload/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'content=@path_to_file; type=text/plain'
  ```

- [GET] `/file/random-line/`: Returns one random line from the `latest` uploaded file via http as `text/plain`, `application/json` or `appication/xml` depending on the request accept header.
  - Response body: `{"line": "Random_line_from_file"}`
  - If the request accept header is `application/json` or `application/xml`, the following details are added to the response body:
    - `line_number`: The line number of the content in `.txt` file.
    - `file_name`: Name of the `.txt` file
    - `most_frequent`: The letter that occurs most often in this line
  ```bash
  curl -X 'GET' \
  'http://localhost:8000/api/file/random-line/' \
  -H 'accept: accept_header in {text/plain, application/json, application/xml}'
  ```
- [GET] `/file/random-line-backwards/`: Returns one random line backwards from each file uploaded.

  - Response body: `[{"random_backward_line": "content_in_backwards"}]`

  ```bash
  curl -X 'GET' \
  'http://localhost:8000/api/file/random-line-backwards/' \
  -H 'accept: application/json'
  ```

- [GET] `/file/longest-hundred-lines/`: Returns `100 longest` lines from all files uploaded.

  - Response body: `{"longest_hundred_lines": []}`

  ```bash
  curl -X 'GET' \
  'http://localhost:8000/api/file/longest-hundred-lines/' \
  -H 'accept: application/json'
  ```

- [GET] `/file/longest-twenty-lines`: Returns `20 longest` lines from the `latest` uploaded file.
  - Response body: `{"longest_twenty_lines": []}`
  ```bash
  curl -X 'GET' \
  'http://localhost:8000/api/file/longest-twenty-lines/' \
  -H 'accept: application/json'
  ```
