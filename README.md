#  Systeme de presence Ml
Ce projet est une application de reconnaissance faciale en temps réel 
qui enregistre et stocke les données des visages détectés dans une base de données Firebase.
L'application utilise OpenCV pour la détection des visages, un modèle pré-entraîné (comme FaceNet ou Dlib) pour
l'extraction des embeddings faciaux, et Firebase Realtime Database pour stocker et gérer les identités des utilisateurs.

## Fonctionnalités :
- Détection faciale en temps réel via la webcam.
- Reconnaissance faciale en comparant les embeddings avec une base de données.
- Enregistrement de nouveaux visages avec association d'un ID/nom dans Firebase.
- Système de vérification pour identifier les utilisateurs connus/inconnus.
- Stockage des logs (date/heure de détection) dans Firebase.

## Technologies utilisées :

Python (OpenCV, Dlib/FaceNet, NumPy)

Firebase Realtime Database (pour le stockage des données)

Firebase Admin SDK (pour l'interaction Python ↔ F
