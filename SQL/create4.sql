DROP DATABASE BIGBOWL;
CREATE DATABASE BIGBOWL;
\c bigbowl

CREATE TABLE DEPARTMENT (
    DEPT varchar(50) PRIMARY KEY
);

CREATE TABLE PANEL (
    LABEL varchar(100) NOT NULL,
    CTIME timestamp,
    IS_SEALED boolean DEFAULT FALSE,
    PANEL_ID bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY
);

CREATE TABLE PANEL_REVIEW (
    PANEL_ID bigint GENERATED ALWAYS AS IDENTITY,
    REVIEW_NUMBER int NOT NULL,
    OPEN_TIME timestamp NOT NULL DEFAULT NOW(),
    CLOSE_TIME timestamp NOT NULL DEFAULT NOW(),
    PRIMARY KEY (PANEL_ID, REVIEW_NUMBER),
    FOREIGN KEY (PANEL_ID) REFERENCES PANEL (PANEL_ID),
    CHECK (REVIEW_NUMBER > 0 AND REVIEW_NUMBER <= 5)
);

CREATE TABLE FACULTY (
    FAC_ID varchar(50) PRIMARY KEY,
    FIRST_NAME varchar(50) NOT NULL,
    LAST_NAME varchar(50) NOT NULL,
    EMAIL varchar(100) NOT NULL,
    PHONE varchar(13) NOT NULL,
    DEPT varchar(50) NOT NULL,
    PANEL_ID bigint DEFAULT NULL,
    IS_COORDINATOR boolean DEFAULT FALSE,
    FOREIGN KEY (PANEL_ID) REFERENCES PANEL (PANEL_ID),
    FOREIGN KEY (DEPT) REFERENCES DEPARTMENT (DEPT),
    CHECK (EMAIL LIKE '%@%.%' AND PHONE LIKE '+__________')
);

CREATE TABLE TEAM (
    TEAM_NAME varchar(50) NOT NULL,
    DESCRIPTION varchar(200),
    GUIDE varchar(50) DEFAULT NULL,
    PANEL_ID bigint DEFAULT NULL,
    TEAM_ID bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    FOREIGN KEY (PANEL_ID) REFERENCES PANEL (PANEL_ID),
    FOREIGN KEY (GUIDE) REFERENCES FACULTY (FAC_ID)
);

CREATE TABLE STUDENT (
    SRN varchar(15) PRIMARY KEY,
    FIRST_NAME varchar(50) NOT NULL,
    LAST_NAME varchar(50) NOT NULL,
    EMAIL varchar(100) NOT NULL,
    PHONE varchar(13) NOT NULL,
    DEPT varchar(50) NOT NULL,
    TEAM_ID bigint DEFAULT NULL,
    FOREIGN KEY (TEAM_ID) REFERENCES TEAM (TEAM_ID),
    CHECK (SRN LIKE 'PES%' AND EMAIL LIKE '%@%.%' AND PHONE LIKE '+__________'),
    FOREIGN KEY (DEPT) REFERENCES DEPARTMENT (DEPT)
);

CREATE TABLE TEAM_FACULTY (
    TEAM_ID bigint NOT NULL,
    FAC_ID varchar(50),
    REMARK_1 varchar(200) DEFAULT NULL,
    REMARK_2 varchar(200) DEFAULT NULL,
    REMARK_3 varchar(200) DEFAULT NULL,
    REMARK_4 varchar(200) DEFAULT NULL,
    REMARK_5 varchar(200) DEFAULT NULL,
    FOREIGN KEY (TEAM_ID) REFERENCES TEAM (TEAM_ID),
    FOREIGN KEY (FAC_ID) REFERENCES FACULTY (FAC_ID),
    PRIMARY KEY (TEAM_ID, FAC_ID)
);

CREATE TABLE REVIEW_1 (
    SRN varchar(15) NOT NULL,
    TEAM_ID bigint NOT NULL,
    FAC_ID varchar(50),
    PROJECT_WORK int NOT NULL,
    QUALITY_OF_DEMO int NOT NULL,
    PROJECT_REPORT int NOT NULL,
    VIVA_VOCE int NOT NULL,
    COMMENTS varchar(150) DEFAULT NULL,
    PRIMARY KEY (SRN, FAC_ID),
    FOREIGN KEY (SRN) REFERENCES STUDENT (SRN),
    FOREIGN KEY (TEAM_ID, FAC_ID) REFERENCES TEAM_FACULTY (TEAM_ID, FAC_ID),
    CHECK (PROJECT_WORK <= 15 AND PROJECT_WORK >= 0 AND QUALITY_OF_DEMO <= 10 AND QUALITY_OF_DEMO >= 0 AND PROJECT_REPORT <= 10 AND PROJECT_REPORT >= 0 AND VIVA_VOCE <= 5 AND VIVA_VOCE >= 0)
);

CREATE TABLE REVIEW_2 (
    SRN varchar(15) NOT NULL,
    TEAM_ID bigint NOT NULL,
    FAC_ID varchar(50),
    PROJECT_WORK int NOT NULL,
    QUALITY_OF_DEMO int NOT NULL,
    PROJECT_REPORT int NOT NULL,
    VIVA_VOCE int NOT NULL,
    COMMENTS varchar(150) DEFAULT NULL,
    PRIMARY KEY (SRN, FAC_ID),
    FOREIGN KEY (SRN) REFERENCES STUDENT (SRN),
    FOREIGN KEY (TEAM_ID, FAC_ID) REFERENCES TEAM_FACULTY (TEAM_ID, FAC_ID),
    CHECK (PROJECT_WORK <= 15 AND PROJECT_WORK >= 0 AND QUALITY_OF_DEMO <= 10 AND QUALITY_OF_DEMO >= 0 AND PROJECT_REPORT <= 10 AND PROJECT_REPORT >= 0 AND VIVA_VOCE <= 5 AND VIVA_VOCE >= 0)
);

CREATE TABLE REVIEW_3 (
    SRN varchar(15) NOT NULL,
    TEAM_ID bigint NOT NULL,
    FAC_ID varchar(50),
    PROJECT_WORK int NOT NULL,
    QUALITY_OF_DEMO int NOT NULL,
    PROJECT_REPORT int NOT NULL,
    VIVA_VOCE int NOT NULL,
    COMMENTS varchar(150) DEFAULT NULL,
    PRIMARY KEY (SRN, FAC_ID),
    FOREIGN KEY (SRN) REFERENCES STUDENT (SRN),
    FOREIGN KEY (TEAM_ID, FAC_ID) REFERENCES TEAM_FACULTY (TEAM_ID, FAC_ID),
    CHECK (PROJECT_WORK <= 15 AND PROJECT_WORK >= 0 AND QUALITY_OF_DEMO <= 10 AND QUALITY_OF_DEMO >= 0 AND PROJECT_REPORT <= 10 AND PROJECT_REPORT >= 0 AND VIVA_VOCE <= 5 AND VIVA_VOCE >= 0)
);

CREATE TABLE REVIEW_4 (
    SRN varchar(15) NOT NULL,
    TEAM_ID bigint NOT NULL,
    FAC_ID varchar(50),
    PROJECT_WORK int NOT NULL,
    QUALITY_OF_DEMO int NOT NULL,
    PROJECT_REPORT int NOT NULL,
    VIVA_VOCE int NOT NULL,
    COMMENTS varchar(150) DEFAULT NULL,
    PRIMARY KEY (SRN, FAC_ID),
    FOREIGN KEY (SRN) REFERENCES STUDENT (SRN),
    FOREIGN KEY (TEAM_ID, FAC_ID) REFERENCES TEAM_FACULTY (TEAM_ID, FAC_ID),
    CHECK (PROJECT_WORK <= 15 AND PROJECT_WORK >= 0 AND QUALITY_OF_DEMO <= 10 AND QUALITY_OF_DEMO >= 0 AND PROJECT_REPORT <= 10 AND PROJECT_REPORT >= 0 AND VIVA_VOCE <= 5 AND VIVA_VOCE >= 0)
);

CREATE TABLE REVIEW_5 (
    SRN varchar(15) NOT NULL,
    TEAM_ID bigint NOT NULL,
    FAC_ID varchar(50),
    PROJECT_WORK int NOT NULL,
    QUALITY_OF_DEMO int NOT NULL,
    PROJECT_REPORT int NOT NULL,
    VIVA_VOCE int NOT NULL,
    COMMENTS varchar(150) DEFAULT NULL,
    PRIMARY KEY (SRN, FAC_ID),
    FOREIGN KEY (SRN) REFERENCES STUDENT (SRN),
    FOREIGN KEY (TEAM_ID, FAC_ID) REFERENCES TEAM_FACULTY (TEAM_ID, FAC_ID),
    CHECK (PROJECT_WORK <= 15 AND PROJECT_WORK >= 0 AND QUALITY_OF_DEMO <= 10 AND QUALITY_OF_DEMO >= 0 AND PROJECT_REPORT <= 10 AND PROJECT_REPORT >= 0 AND VIVA_VOCE <= 5 AND VIVA_VOCE >= 0)
);

