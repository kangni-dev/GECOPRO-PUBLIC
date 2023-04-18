CREATE DATABASE IF NOT EXISTS gecodb;
USE gecodb;
DROP TABLE IF EXISTS Suivre;
DROP TABLE IF EXISTS Etudiants;
DROP TABLE IF EXISTS Employes;
DROP TABLE IF EXISTS Classes;
DROP TABLE IF EXISTS Etablissements;

DROP TABLE IF EXISTS Utilisateurs;
DROP TABLE IF EXISTS Roles;



DROP TABLE IF EXISTS Matieres;



CREATE TABLE  Roles(
    id_role varchar(20),
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
    no_civique varchar(20),
    rue varchar(20),
    ville varchar(20),
    pays varchar(20),
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
CREATE TABLE Classes(
    id_classe char(5),
    id_etablissement int ,
    niveau_classe varchar(20),
    PRIMARY KEY (id_classe),
    FOREIGN KEY (id_etablissement) REFERENCES Etablissements(id_etab)
);

CREATE TABLE Etudiants(
    id_etu int ,
    date_naissance_etu DATE,
    id_classe char(5),
    PRIMARY KEY (id_etu),
    FOREIGN KEY (id_etu) REFERENCES Utilisateurs(id_utilisateur),
    FOREIGN KEY (id_classe) REFERENCES Classes(id_classe)
);

CREATE TABLE  Employes(
    id_emp int,
    poste_emp varchar(20),
    PRIMARY KEY (id_emp),
    FOREIGN KEY (id_emp) REFERENCES Utilisateurs(id_utilisateur)
);



CREATE TABLE Matieres(
    id_matiere varchar(50),
    nom_matiere varchar(50),
    PRIMARY KEY (id_matiere)
);

CREATE TABLE Suivre(
    id_etu int,
    id_matiere varchar(50),
    note_1 double,
    note_2 double,
    note_3 double,
    note_4 double,
    note_5 double,
    note_6 double,
    PRIMARY KEY (id_etu,id_matiere),
    FOREIGN KEY (id_matiere) REFERENCES Matieres(id_matiere),
    FOREIGN KEY (id_etu) REFERENCES Etudiants(id_etu)
);

INSERT INTO Roles VALUES ('ADMIN','Administrateur','pour systeme');
INSERT INTO Roles VALUES ('EMP','Employe','pour les empployes');
INSERT INTO Roles VALUES ('ETUDIANT','Etudiant','pour les apprenants');


