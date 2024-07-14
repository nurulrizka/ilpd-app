from flask import Flask, request, render_template
import pickle, os

def validasi_inputan(form_data):
    errors = {}

    if not form_data.get("Age"):
        errors["Age"] = "Umur tidak boleh kosong."
    else:
        try:
            age = int(form_data.get("Age"))
        except ValueError:
            errors["Age"] = "Umur harus berupa angka."

    if not form_data.get("Gender"):
        errors["Gender"] = "Jenis Kelamin tidak boleh kosong."

    if not form_data.get("Total_Bilirubin"):
        errors["Total_Bilirubin"] = "Total Bilirubin tidak boleh kosong."
    else:
        try:
            total_bilirubin = float(form_data.get("Total_Bilirubin"))
        except ValueError:
            errors["Total_Bilirubin"] = "Total Bilirubin harus berupa angka."

    if not form_data.get("Direct_Bilirubin"):
        errors["Direct_Bilirubin"] = "Direct Bilirubin tidak boleh kosong."
    else:
        try:
            direct_bilirubin = float(form_data.get("Direct_Bilirubin"))
        except ValueError:
            errors["Direct_Bilirubin"] = "Direct Bilirubin harus berupa angka."

    if not form_data.get("Alkaline_Phosphotase"):
        errors["Alkaline_Phosphotase"] = "Alkaline Phosphotase tidak boleh kosong."
    else:
        try:
            alkaline_phosphotase = int(form_data.get("Alkaline_Phosphotase"))
        except ValueError:
            errors["Alkaline_Phosphotase"] = "Alkaline Phosphotase harus berupa angka."

    if not form_data.get("Alamine_Aminotransferase"):
        errors["Alamine_Aminotransferase"] = "Serum Glutamic Pyruvic Transaminase(SGPT)(IU/L) tidak boleh kosong."
    else:
        try:
            alamine_aminotransferase = int(form_data.get("Alamine_Aminotransferase"))
        except ValueError:
            errors["Alamine_Aminotransferase"] = "Serum Glutamic Pyruvic Transaminase(SGPT)(IU/L) harus berupa angka."

    if not form_data.get("Aspartate_Aminotransferase"):
        errors["Aspartate_Aminotransferase"] = "Serum Glutamic Oxaloacetic Transaminase(SGOT)(IU/L) tidak boleh kosong."
    else:
        try:
            aspartate_aminotransferase = int(form_data.get("Aspartate_Aminotransferase"))
        except ValueError:
            errors["Aspartate_Aminotransferase"] = "Serum Glutamic Oxaloacetic Transaminase(SGOT)(IU/L) harus berupa angka."

    if not form_data.get("Total_Proteins"):
        errors["Total_Proteins"] = "Total Proteins tidak boleh kosong."
    else:
        try:
            total_proteins = float(form_data.get("Total_Proteins"))
        except ValueError:
            errors["Total_Proteins"] = "Total Proteins harus berupa angka."

    if not form_data.get("Albumin"):
        errors["Albumin"] = "Albumin tidak boleh kosong."
    else:
        try:
            albumin = float(form_data.get("Albumin"))
        except ValueError:
            errors["Albumin"] = "Albumin harus berupa angka."

    if not form_data.get("Albumin_and_Globulin_Ratio"):
        errors["Albumin_and_Globulin_Ratio"] = "Rasio Albumin dan Globulin tidak boleh kosong."
    else:
        try:
            albumin_and_globulin_ratio = float(form_data.get("Albumin_and_Globulin_Ratio"))
        except ValueError:
            errors["Albumin_and_Globulin_Ratio"] = "Rasio Albumin dan Globulin harus berupa angka."

    return errors

def validate_data(record):
    errors = {}
    if record["Age"] < 4 or record["Age"] > 90:
        errors["Age"] = "Umur harus diantara 4 dan 90 tahun"

    if record["Total_Bilirubin"] < 0.1 or record["Total_Bilirubin"] > 10.0:
        errors["Total_Bilirubin"] = "Total Bilirubin harus diantara 0.1 dan 10.0 mg/dL."

    if record["Direct_Bilirubin"] < 0.1 or record["Direct_Bilirubin"] > 5.0:
        errors["Direct_Bilirubin"] = "Direct Bilirubin harus diantara 0.1 dan 5.0 mg/dL."

    if record["Alkaline_Phosphotase"] < 20 or record["Alkaline_Phosphotase"] > 1000:
        errors["Alkaline_Phosphotase"] = "Alkaline Phosphotase harus diantara 20 dan 1000 IU/L."

    if record["Alamine_Aminotransferase"] < 10 or record["Alamine_Aminotransferase"] > 500:
        errors["Alamine_Aminotransferase"] = "Alamine Aminotransferase harus diantara 10 dan 500 IU/L."

    if record["Aspartate_Aminotransferase"] < 10 or record["Aspartate_Aminotransferase"] > 500:
        errors["Aspartate_Aminotransferase"] = "Aspartate Aminotransferase harus diantara 10 dan 500 IU/L."

    if record["Total_Proteins"] < 2.0 or record["Total_Proteins"] > 12.0:
        errors["Total_Proteins"] = "Total Proteins harus diantara 2.0 dan 12.0 g/dL."

    if record["Albumin"] < 0.5 or record["Albumin"] > 6.0:
        errors["Albumin"] = "Albumin harus diantara 0.5 dan 6.0 g/dL."

    if record["Albumin_and_Globulin_Ratio"] < 0.1 or record["Albumin_and_Globulin_Ratio"] > 3.0:
        errors["Albumin_and_Globulin_Ratio"] = "Rasio Albumin dan Globulin harus diantara 0.1 dan 3.0."

    return errors

# Load models
classifier_load = pickle.load(open('stacking.sav', 'rb'))

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def index():
    disease = None
    errors = {}
    if request.method == "POST":
        # Validasi inputan tidak boleh kosong
        errors = validasi_inputan(request.form)
        if not errors:
            record = {
                "Age": int(request.form.get("Age")),
                "Gender": int(request.form.get("Gender")),
                "Total_Bilirubin": float(request.form.get("Total_Bilirubin")),
                "Direct_Bilirubin": float(request.form.get("Direct_Bilirubin")),
                "Alkaline_Phosphotase": int(request.form.get("Alkaline_Phosphotase")),
                "Alamine_Aminotransferase": int(request.form.get("Alamine_Aminotransferase")),
                "Aspartate_Aminotransferase": int(request.form.get("Aspartate_Aminotransferase")),
                "Total_Proteins": float(request.form.get("Total_Proteins")),
                "Albumin": float(request.form.get("Albumin")),
                "Albumin_and_Globulin_Ratio": float(request.form.get("Albumin_and_Globulin_Ratio")),
            }

            errors = validate_data(record)
            if not errors:
                input_data = [
                    record["Age"],
                    record["Gender"],
                    record["Total_Bilirubin"],
                    record["Direct_Bilirubin"],
                    record["Alkaline_Phosphotase"],
                    record["Alamine_Aminotransferase"],
                    record["Aspartate_Aminotransferase"],
                    record["Total_Proteins"],
                    record["Albumin"],
                    record["Albumin_and_Globulin_Ratio"],
                ]

                print(input_data)

                # Membuat prediksi dari model
                disease = classifier_load.predict([input_data])[0]

    return render_template('index.html', disease=disease, errors=errors, record=request.form)

if __name__ == "__main__":
    app.run(debug=True)
