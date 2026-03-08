🛰️ SatIndex-ProcessorSatIndex-Processor est une plateforme web avancée basée sur Django, conçue pour le traitement et l'analyse d'images satellitaires (GeoTIFF). Ce projet permet de calculer des indices de végétation, de classifier l'occupation du sol et de détecter les changements urbains et agricoles, particulièrement dans le contexte marocain.
🚀 Fonctionnalités ClésCalcul d'Indices Géospatiaux : Calcul automatisé du NDVI (Normalized Difference Vegetation Index) à l'aide de rasterio.Détection de Changement (Change Detection) : Comparaison temporelle entre deux dates pour identifier les gains ou pertes de végétation.Classification de l'Occupation du Sol : Segmentation de l'image en catégories (Végétation, Urbain, Sol nu, Eau) avec calcul des surfaces en $km^2$.Génération de Rapports PDF : Création de rapports dynamiques via ReportLab incluant des cartes colorisées, des tableaux de statistiques et les métadonnées techniques (CRS, Résolution).Architecture REST API : Intégration complète via Django Rest Framework pour une interopérabilité maximale.
🛠️ Stack TechniqueBackend : Django, Django Rest Framework.Bibliothèques Géospatiales : Rasterio, NumPy, Pandas, Scikit-learn (XGBoost, LightGBM).Visualisation : Matplotlib (pour le rendu des cartes thématiques).Reporting : ReportLab (pour l'export PDF en mémoire vive).
⚙️ Installation et Utilisation
1 Cloner le projet : git clone https://github.com/votre-username/SatIndex-Processor.git
2 Créer un environnement virtuel : 
python -m venv env
source env/Scripts/activate  # Sur Windows
3 Installer les dépendances : pip install -r requirements.txt
4 Lancer le serveur : python manage.py runserver
