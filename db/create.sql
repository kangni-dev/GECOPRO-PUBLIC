CREATE DATABASE IF NOT EXISTS gecodb;
USE gecodb;
DROP TABLE IF EXISTS Etablissements;
DROP TABLE IF EXISTS Utilisateurs;
DROP TABLE IF EXISTS Roles;

CREATE TABLE  Roles(
    id_role char(5),
    nom_role varchar(20),
    desc_role varchar(50),
    UNIQUE (nom_role),
    PRIMARY KEY (id_role)
);
CREATE TABLE Utilisateurs(
    id_utilisateur int AUTO_INCREMENT,
    nom_utilisateur varchar(20),
    prenom_utilisateur varchar(20),
    courriel_utilisateur varchar(20),
    telephone_utilisateur varchar(20),
    role_utilisateur varchar(20),
    mot_de_passe varchar(20),
    adresse_utilisateur varchar(20),
    PRIMARY KEY (id_utilisateur),
    FOREIGN KEY (role_utilisateur) REFERENCES Roles(id_role)

);

CREATE TABLE Etablissements(
    id_etab int AUTO_INCREMENT,
    nom_etab varchar(50),
    adresse_etab varchar(50),
    tel_etab varchar(50),
    ville_etab varchar(50),
    pays_etab varchar(50),
    PRIMARY KEY (id_etab)
);

