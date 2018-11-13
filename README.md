# HABROPROXY

[![Build Status](https://travis-ci.com/ydanilin/habroproxy2.svg?branch=master)](https://travis-ci.com/ydanilin/habroproxy2)
[![Maintainability](https://api.codeclimate.com/v1/badges/58160aab1f244142509b/maintainability)](https://codeclimate.com/github/ydanilin/habroproxy2/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/58160aab1f244142509b/test_coverage)](https://codeclimate.com/github/ydanilin/habroproxy2/test_coverage)

## Описание

Проект выполнялся как тестовое задание в компанию [Ivelum](https://ivelum.com/).

Представляет собой прокси-сервер, который модифицирует html-страницы от сервера [habr.com](https://habr.com/) следующим образом:

* если длина слова на html странице равна 6 символов, к такому слову в конце добавляется значок ™.

Ответы от других серверов и/или с контентом, отличным от html, не модифицируются.

Тестировалось на Ubuntu: Firefox, Windows: Chrome, Firefox, IE Windows

## Установка

### Prerequisites

* `Python` **3**.
* Пользователям Windows рекомендуется установить недостающий и очень удобный инструмент `make`, скачав его [отсюда](https://vorboss.dl.sourceforge.net/project/gnuwin32/make/3.81/make-3.81.exe) и прописав в путь.

### Развертывание

```bash
git clone https://github.com/ydanilin/habroproxy2.git
cd habroproxy2
make install
```

### Запуск

Смотрим/прописываем адрес и порт сервера в файле `run.py`

Для запуска прокси набираем

```bash
make run
```

Получаем ответ  
`Habroproxy server started at '<address>':<port>`

## Работа через прокси

В строке браузера набираем `<address>:<port>` указанные выше и видим модифицированную страницу Хабра.  
В случае IE надо ставить префикс `http://`, иначе он отправляет в поиск.
Прокси модифицирует ссылки так, чтобы браузер не уходил с локального в случае перехода на другие хабро-страницы.
Ссылки на иные ресурсы не модифицируются.
