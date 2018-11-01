# HABROPROXY

## Описание

Проект выполнялся как тестовое задание в компанию [Ivelum](https://ivelum.com/).

Представляет собой прокси-сервер, который модифицирует html-страницы от сервера [habr.com](https://habr.com/) следующим образом:

* если длина слова на html странице равна 6 символов, к такому слову в конце добавляется значок ™.

Ответы от других серверов и/или с контентом, отличным от html, не модифицируются.

## Установка

### Prerequisites

* `Python` версии **не выше 3.6.6**. Новейшая 3.7 на данный момент не поддерживает библиотеку OpenSSL.
* Пользователям Windows рекомендуется установить недостающий и очень удобный инструмент `make`, скачав его [отсюда](https://vorboss.dl.sourceforge.net/project/gnuwin32/make/3.81/make-3.81.exe) и прописав в путь.
* Браузер Firefox (с другими пока не тестировалось)

### Развертывание

```bash
git clone https://github.com/ydanilin/habroproxy.git
cd habroproxy
make install
```

### Запуск

Для запуска прокси набираем

```bash
make run
```

Получаем ответ  
`Habroproxy server is listening to '': 8080`
