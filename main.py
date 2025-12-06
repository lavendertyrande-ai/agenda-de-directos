from flask import Flask, render_template, request, redirect, flash
from db import db
from models import Reserva

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservas.db'
app.config['SECRET_KEY'] = 'clave-secreta'
db.init_app(app)

with app.app_context():
    db.create_all()


# Función para verificar disponibilidad
def hora_disponible(hora):
    return not Reserva.query.filter(
        (Reserva.hora1 == hora) | (Reserva.hora2 == hora) | (Reserva.hora3 == hora)
    ).first()


@app.route("/", methods=["GET", "POST"])
def index():
    horas = [f"{dia} {h}:00" for dia in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"] for h in range(16, 25)]

    if request.method == "POST":
        twitch_id = request.form.get("twitch_id")
        hora1 = request.form.get("hora1")
        hora2 = request.form.get("hora2")
        hora3 = request.form.get("hora3")

        # Validar disponibilidad
        for h in [hora1, hora2, hora3]:
            if h and not hora_disponible(h):
                flash(f"Hora no disponible, elige otra: {h}")
                return redirect("/")

        reserva = Reserva(twitch_id=twitch_id, hora1=hora1, hora2=hora2, hora3=hora3)
        db.session.add(reserva)
        db.session.commit()
        flash("Reserva realizada con éxito ✅")
        return redirect("/")

    return render_template("index.html", horas=horas)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

