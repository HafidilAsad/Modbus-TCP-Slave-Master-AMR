from flask import Flask, request
import modbus_server

# Menentukan port Modbus
s = modbus_server.Server(port=503)

# Menjalankan server
s.start()

app = Flask(__name__)

# Membuat address 0 menjadi True (1)
s.set_discrete_input(0, True)


@app.route("/")
def home():
    return '''
    <html>
    <body>
        <h1>PANGGil, AMR!</h1>
        <button id="set-false-button">BALIK</button>
        <button id="set-true-button">PANGGIL</button>
        <script>
            document.getElementById("set-false-button").addEventListener("click", function() {
                fetch("/set_discrete_input?value=false", { method: "POST" })
                    .then(response => response.text())
                    .then(data => console.log(data));
            });
            document.getElementById("set-true-button").addEventListener("click", function() {
                fetch("/set_discrete_input?value=true", { method: "POST" })
                    .then(response => response.text())
                    .then(data => console.log(data));
            });
        </script>
    </body>
    </html>
    '''


@app.route("/set_discrete_input", methods=['POST'])
def set_discrete_input():
    value = request.args.get('value')
    if value == 'false':
        s.set_discrete_input(0, False)
        return "Discrete input set to False"
    elif value == 'true':
        s.set_discrete_input(0, True)
        return "Discrete input set to True"
    else:
        return "Invalid value", 400


if __name__ == "__main__":
    app.run(debug=True)
