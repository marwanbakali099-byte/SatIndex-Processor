# 🛰️ SatIndex-Processor

**SatIndex-Processor** est une plateforme web avancée basée sur **Django**, conçue pour le traitement et l'analyse d'images satellitaires (GeoTIFF). Ce projet permet de calculer des indices de végétation, de classifier l'occupation du sol et de détecter les changements urbains et agricoles, avec une spécialisation sur le contexte géographique marocain.

---

## 🚀 Fonctionnalités Clés

* **Calcul d'Indices Géospatiaux** : Calcul automatisé du **NDVI** (Normalized Difference Vegetation Index) via `rasterio` et `numpy`.
* **Détection de Changement (Change Detection)** : Analyse temporelle entre deux dates pour identifier les gains ou pertes de couverture.
* **Classification de l'Occupation du Sol** : Segmentation automatique (Végétation, Urbain, Sol nu, Eau) avec calcul précis des surfaces en $km^2$.
* **Génération de Rapports PDF** : Export de rapports dynamiques (`ReportLab`) incluant cartes colorisées, statistiques et métadonnées techniques (CRS, Résolution).
* **Architecture REST API** : Intégration complète via **Django Rest Framework** (DRF) pour une interopérabilité maximale.

---

## 🛠️ Stack Technique

| Domaine | Technologies |
| :--- | :--- |
| **Backend** | Django, Django Rest Framework |
| **Géospatial** | Rasterio, NumPy, Pandas |
| **Machine Learning** | Scikit-learn (XGBoost, LightGBM) |
| **Visualisation** | Matplotlib, Pillow |
| **Reporting** | ReportLab |



source env/bin/activate
