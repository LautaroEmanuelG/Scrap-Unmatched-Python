# 🕵️‍♂️ Scrap Unmatched

Este proyecto utiliza Playwright para hacer scraping de imágenes de héroes y cartas desde la página [The Unmatched Club](https://www.the-unmatched.club). Las imágenes se descargan y se convierten de formato webp a png.

## 📋 Requisitos

- Python 3.x
- Playwright
- Requests
- Pillow

## 🚀 Instalación

1. Clona este repositorio:

    ```bash
    git clone https://github.com/tu_usuario/scrap-unmatched.git
    cd scrap-unmatched
    ```

2. Crea y activa un entorno virtual (opcional pero recomendado):

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

4. Instala Playwright y sus navegadores:

    ```bash
    playwright install
    ```

## 🛠️ Uso

Para ejecutar el script, simplemente corre el siguiente comando en tu terminal:

```bash
python scrapUnmatched.py
```

El script está configurado para hacer scraping de la página del héroe "Eredin". Puedes cambiar el nombre del héroe y la URL modificando las variables `hero_name` y `page_url` en el archivo `scrapUnmatched.py`.

## 📂 Estructura del Proyecto

- `scrapUnmatched.py`: Script principal que realiza el scraping.
- `README.md`: Este archivo.
- `requirements.txt`: Lista de dependencias necesarias.

## 📸 Ejemplo de Salida

El script descargará las imágenes en carpetas organizadas por el nombre del héroe. Por ejemplo:

```bash
Eredin/
├── hero/
│   ├── Actor_token.webp
│   ├── cover_Eredin x10.webp
│   └── Eredin.webp
└── cards/
    ├── card_0 x1.webp
    ├── card_1 x2.webp
    └── card_2 x1.webp
```

## 📜 Lista de Elementos Scrapeados

A continuación se muestra una lista de los elementos que ya han sido scrapeados:

- **Eredin**
  - Hero Images:
    - Actor_token.webp
    - cover_Eredin x10.webp
    - Eredin.webp
  - Cards:
    - card_0 x1.webp
    - card_1 x2.webp
    - card_2 x1.webp

## 📝 Notas

- Asegúrate de tener una conexión a internet estable para descargar las imágenes.
- Si encuentras algún problema, revisa los mensajes de error en la terminal para más detalles.

¡Feliz scraping! 🚀
