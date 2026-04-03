import os
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

app = Flask(__name__)
app.jinja_env.globals.update(enumerate=enumerate)

# ── Konstanta ──────────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "data.csv")
TARGET_KABUPATEN = "KABUPATEN SUKABUMI"

# ── Load & prepare data ────────────────────────────────────────────────────────
def load_data():
    df = pd.read_csv(DATA_PATH)
    df_sukabumi = df[df["nama_kabupaten_kota"] == TARGET_KABUPATEN].copy()
    df_sukabumi = df_sukabumi.sort_values("tahun").reset_index(drop=True)
    return df_sukabumi

def build_model(df):
    X = df[["tahun"]].values
    y = df["produksi_tanaman"].values

    model = LinearRegression()
    model.fit(X, y)

    y_pred = model.predict(X)
    r2  = r2_score(y, y_pred)
    mae = mean_absolute_error(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))

    return model, r2, mae, rmse, y_pred.tolist()

# ── Pre-load ───────────────────────────────────────────────────────────────────
try:
    df_data = load_data()
    model, r2_val, mae_val, rmse_val, y_pred_hist = build_model(df_data)
    DATA_OK = True
except Exception as e:
    DATA_OK = False
    ERR_MSG = str(e)

# ── Routes ─────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    if not DATA_OK:
        return render_template("index.html", error=ERR_MSG)

    table = df_data[["tahun", "produksi_tanaman"]].rename(
        columns={"tahun": "Tahun", "produksi_tanaman": "Produksi (Ton)"}
    ).to_dict(orient="records")

    chart_data = {
        "tahun":       df_data["tahun"].tolist(),
        "aktual":      df_data["produksi_tanaman"].tolist(),
        "prediksi":    [round(v, 2) for v in y_pred_hist],
    }

    metrics = {
        "r2":   round(r2_val, 4),
        "mae":  round(mae_val, 4),
        "rmse": round(rmse_val, 4),
        "intercept": round(float(model.intercept_), 4),
        "slope":     round(float(model.coef_[0]), 4),
    }

    return render_template(
        "index.html",
        table=table,
        chart_data=chart_data,
        metrics=metrics,
        error=None,
        result=None,
    )


@app.route("/prediksi", methods=["POST"])
def prediksi():
    if not DATA_OK:
        return render_template("index.html", error=ERR_MSG)

    table = df_data[["tahun", "produksi_tanaman"]].rename(
        columns={"tahun": "Tahun", "produksi_tanaman": "Produksi (Ton)"}
    ).to_dict(orient="records")

    chart_data = {
        "tahun":    df_data["tahun"].tolist(),
        "aktual":   df_data["produksi_tanaman"].tolist(),
        "prediksi": [round(v, 2) for v in y_pred_hist],
    }

    metrics = {
        "r2":   round(r2_val, 4),
        "mae":  round(mae_val, 4),
        "rmse": round(rmse_val, 4),
        "intercept": round(float(model.intercept_), 4),
        "slope":     round(float(model.coef_[0]), 4),
    }

    try:
        tahun_input = int(request.form.get("tahun_proyeksi", 0))
        if tahun_input < 1900 or tahun_input > 2100:
            raise ValueError("Tahun tidak valid. Masukkan antara 1900 – 2100.")

        nilai_prediksi = model.predict([[tahun_input]])[0]
        nilai_prediksi = max(0, round(float(nilai_prediksi), 2))

        result = {
            "tahun": tahun_input,
            "nilai": nilai_prediksi,
        }

        # Perluas grafik dengan titik prediksi
        chart_data["tahun_pred"] = tahun_input
        chart_data["nilai_pred"] = nilai_prediksi

    except ValueError as ve:
        return render_template(
            "index.html",
            table=table, chart_data=chart_data, metrics=metrics,
            error=str(ve), result=None,
        )

    return render_template(
        "index.html",
        table=table, chart_data=chart_data, metrics=metrics,
        error=None, result=result,
    )


if __name__ == "__main__":
    app.run(debug=True)
