const API_URL = "http://192.168.0.36/api";

document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("accessToken");
    const username = localStorage.getItem("username");

    // Redirige vers login.html si l'utilisateur n'est pas connecté
    if (!token) {
        window.location.href = "login.html";
        return;
    }

    const usernameDisplay = document.getElementById("usernameDisplay");
    if (usernameDisplay && username) {
        usernameDisplay.textContent = username;
    }

    chargerPannes();
    chargerEquipements();

    const form = document.getElementById("formPanne");
    if (form) {
        form.addEventListener("submit", ajouterPanne);
    }
});

function deconnexion() {
    localStorage.clear();
    window.location.href = "login.html";
}

async function fetchAuth(url, options = {}) {
    const token = localStorage.getItem("accessToken");

    const headers = {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
        ...options.headers
    };

    const response = await fetch(url, { ...options, headers });

    if (response.status === 401) {
        deconnexion();
    }

    return response;
}

async function chargerEquipements() {
    try {
        const response = await fetchAuth(`${API_URL}/equipements/`);
        if (!response.ok) return;

        const equipements = await response.json();
        const equipementSelect = document.getElementById("equipementSelect");
        if (!equipementSelect) return;

        equipementSelect.innerHTML = '<option value="">Sélectionnez un équipement</option>';

        equipements.forEach(eq => {
            const option = document.createElement("option");
            option.value = eq.id;
            option.textContent = eq.nom_equipement || eq.nom || `Équipement #${eq.id}`;
            equipementSelect.appendChild(option);
        });
    } catch (error) {
        console.error("Erreur lors du chargement des équipements :", error);
    }
}

async function chargerPannes() {
    try {
        const response = await fetchAuth(`${API_URL}/pannes/`);
        if (!response.ok) return;

        const data = await response.json();
        const tableBody = document.getElementById("pannesTableBody");
        if (!tableBody) return;

        tableBody.innerHTML = "";

        data.forEach(panne => {
            const row = document.createElement("tr");

            const nomEquipement = panne.equipement_detail 
                ? (panne.equipement_detail.nom_equipement || panne.equipement_detail.nom) 
                : (panne.nom_equipement || panne.equipement);

            const nomDemandeur = panne.demandeur_detail 
                ? (panne.demandeur_detail.nom || panne.demandeur_detail.username || `${panne.demandeur_detail.prenom || ''} ${panne.demandeur_detail.nom || ''}`.trim()) 
                : `Utilisateur #${panne.demandeur}`;

            let badgeColor = "bg-warning text-dark";
            if (panne.statut === "EN_COURS" || panne.statut === "En cours") badgeColor = "bg-primary text-white";
            if (panne.statut === "RESOLU" || panne.statut === "Résolu") badgeColor = "bg-success text-white";

            row.innerHTML = `
                <td>${panne.id}</td>
                <td><strong>${panne.code_ticket || '-'}</strong></td>
                <td>${panne.titre || '-'}</td>
                <td>${nomEquipement}</td>
                <td>${nomDemandeur}</td>
                <td>${panne.description}</td>
                <td><span class="badge ${badgeColor}">${panne.statut || "En attente"}</span></td>
                <td>
                    <select class="form-select form-select-sm" onchange="changerStatut(${panne.id}, this.value)">
                        <option value="">Modifier statut...</option>
                        <option value="En attente">En attente</option>
                        <option value="En cours">En cours</option>
                        <option value="Résolu">Résolu</option>
                    </select>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Erreur lors du chargement des pannes :", error);
    }
}

async function changerStatut(idPanne, nouveauStatut) {
    if (!nouveauStatut) return;

    try {
        const response = await fetchAuth(`${API_URL}/pannes/${idPanne}/`, {
            method: "PATCH",
            body: JSON.stringify({ statut: nouveauStatut })
        });

        if (response.ok) {
            chargerPannes();
        } else {
            alert("Impossible de modifier le statut.");
        }
    } catch (error) {
        console.error("Erreur réseau lors de la modification :", error);
    }
}

async function ajouterPanne(event) {
    event.preventDefault();

    const equipementId = document.getElementById("equipementSelect")?.value;
    const currentUserId = localStorage.getItem("userId");

    if (!equipementId || !currentUserId) {
        alert("Veuillez sélectionner un équipement.");
        return;
    }

    const codeUnique = "TCK-" + Math.floor(1000 + Math.random() * 9000);

    const nouvellePanne = {
        code_ticket: codeUnique,
        titre: document.getElementById("titreInput").value,
        equipement: parseInt(equipementId),
        demandeur: parseInt(currentUserId),
        description: document.getElementById("descriptionInput").value,
        statut: "En attente"
    };

    try {
        const response = await fetchAuth(`${API_URL}/pannes/`, {
            method: "POST",
            body: JSON.stringify(nouvellePanne)
        });

        if (response.ok) {
            document.getElementById("formPanne").reset();

            const modalElement = document.getElementById("modalPanne");
            const modalInstance = bootstrap.Modal.getInstance(modalElement);
            if (modalInstance) {
                modalInstance.hide();
            }

            chargerPannes();
        } else {
            const errorData = await response.json();
            alert("Erreur lors de l'ajout : " + JSON.stringify(errorData));
        }
    } catch (error) {
        console.error("Erreur réseau :", error);
    }
}