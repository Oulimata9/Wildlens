const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const resultDiv = document.getElementById("result");
const nomEspece = document.getElementById("nom_espece");
const description = document.getElementById("description");
const uploadInput = document.getElementById("uploadInput");

// Activer la caméra au démarrage
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        alert("Erreur d’accès à la caméra : " + err.message);
    });

// Prendre une photo depuis la caméra
function takePhoto() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(blob => {
        sendToBackend(blob);
    }, "image/jpeg");
}

// Importer une image depuis la galerie
function importPhoto(event) {
    const file = event.target.files[0];
    if (file) {
        sendToBackend(file);
    }
}

// Envoyer l’image au backend
async function sendToBackend(blobOrFile, imagePreviewURL) {
    const formData = new FormData();
    formData.append("file", blobOrFile, "image.jpg");

    try {
        const response = await fetch("http://localhost:8000/predict", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            const text = await response.text(); // Erreur 500/404
            throw new Error("Erreur serveur : " + response.status + "\n" + text);
        }

        const data = await response.json();
        console.log("Réponse brute du backend :", data);

        //  Vérifie si une espèce a vraiment été détectée
        // Sauvegarde dans tous les cas (même si espèce non détectée)
        const espece = data.nom_espece || "Aucune espèce détectée";
        const description = data.description || "L'image n'a pas permis d'identifier une empreinte animale connue.";

        localStorage.setItem("dernier_resultat", JSON.stringify({
            nom_espece: espece,
            description: description,
            nom_scientifique: data.nom_scientifique || "",
            habitat: data.habitat || "",
            taille: data.taille || "",
            famille: data.famille || "",
            confidence: data.confidence || "",
            image_url: imagePreviewURL || ""
        }));

        window.location.href = "resultat.html";

            // Optionnel : efface l’image temporaire du canvas
        canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
        }

    catch (error) {
        alert("Erreur lors de la prédiction : " + error.message);
        resultDiv.style.display = "none";
    }
}
