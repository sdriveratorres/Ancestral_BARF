from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
from html import escape


# =====================================================
# 1. FUNCIÓN PARA CALCULAR LA PORCIÓN
# =====================================================

def calcular_porcion(edad, peso):

     # Definir porcentaje según la edad del perro

    if edad <= 3:
        porcentaje = 0.09

    elif edad <= 5:
        porcentaje = 0.07

    elif edad <= 8:
        porcentaje = 0.05

    elif edad <= 12:
        porcentaje = 0.035

    else:
        porcentaje = 0.025

    # Calcular gramos diarios

    gramos = peso * 1000 * porcentaje

    # Calcular cantidad de bolsas

    bolsas = round(gramos / 500, 10)

    enteras = int(bolsas) + (1 if bolsas > int(bolsas) else 0)

    return gramos, bolsas, enteras, porcentaje


# =====================================================
# 2. FUNCIÓN PRINCIPAL DE VERCEL
# =====================================================

class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        # Recibir los datos del formulario
        longitud = int(self.headers.get("Content-Length", 0))

        datos = self.rfile.read(longitud).decode("utf-8")

        formulario = parse_qs(datos)

        try:

            # Obtener edad y peso
            edad = int(formulario["edad"][0])

            peso = float(formulario["peso"][0])

            # Validar los datos
            if edad < 2 or not (0 < peso <= 200):
                raise ValueError()

            # Calcular la porción
            gramos, bolsas, enteras, tasa = calcular_porcion(edad, peso)

            # Construir el resultado
            resultado = f"""
                <small>PORCIÓN DIARIA ORIENTATIVA · {tasa:.1%}</small>

                <h2>{gramos:,.1f} g</h2>

                <p>{bolsas:.2f} bolsas de 500 g equivalentes al día.</p>

                <p>Para disponer de la ración de un día:
                {enteras} bolsa(s) entera(s).</p>

                <p>Conserva el sobrante de forma segura.</p>
            """

        except (ValueError, KeyError, OverflowError):

            resultado = """
                <h2>Datos no válidos</h2>
                <p>Ingresa una edad entera desde 2 meses
                    y un peso válido mayor a 0 y hasta 200 kg.</p>
            """

        # Enviar resultado al navegador
        self.responder(resultado)

    # =================================================
    # 3. RESPUESTA HTML
    # =================================================

    def responder(self, contenido):

        pagina = f"""
        <!DOCTYPE html>
        <html lang="es">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">

            <title>Resultado - Ancestral BARF</title>

            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: #f4f0e8;
                    padding: 30px;
                    text-align: center;
                }}

                .resultado {{
                    background: white;
                    max-width: 500px;
                    margin: 40px auto;
                    padding: 30px;
                    border-radius: 15px;
                }}

                h2 {{
                    color: #536b43;
                }}

                a {{
                    display: inline-block;
                    background: #536b43;
                    color: white;
                    padding: 12px 20px;
                    border-radius: 8px;
                    text-decoration: none;
                }}
            </style>
        </head>

        <body>

            <div class="resultado">

                <h1>Ancestral BARF</h1>

                <h2>Resultado de tu calculadora</h2>

                {contenido}

                <a href="/">Volver a la página principal</a>

            </div>

        </body>
        </html>
        """

        contenido = pagina.encode("utf-8")

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(contenido))
        )

        self.end_headers()

        self.wfile.write(contenido)
