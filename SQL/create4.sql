DROP DATABASE BIGBOWL;
CREATE DATABASE BIGBOWL;
\c bigbowl
CREATE TABLE DEPARTMENT (
    DEPT varchar(50) PRIMARY KEY
);

CREATE TABLE PANEL (
    LABEL varchar(100) NOT NULL,
    IS_ACTIVE boolean DEFAULT TRUE,
    PANEL_ID bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    CTIME timestamp DEFAULT NOW()
);

CREATE TABLE PANEL_REVIEW (
    REVIEW_NUMBER int NOT NULL,
    PANEL_ID bigint NOT NULL,
    OPEN_TIME timestamp NOT NULL DEFAULT NOW(),
    CLOSE_TIME timestamp NOT NULL DEFAULT NOW(),
    PRIMARY KEY (PANEL_ID, REVIEW_NUMBER),
    FOREIGN KEY (PANEL_ID) REFERENCES PANEL (PANEL_ID) ON DELETE CASCADE,
    CHECK (REVIEW_NUMBER > 0 AND REVIEW_NUMBER <= 5)
);

CREATE TABLE FACULTY (
    FAC_ID varchar(50) PRIMARY KEY,
    NAME varchar(100) NOT NULL,
    EMAIL varchar(100) NOT NULL,
    PHONE varchar(13) NOT NULL,
    DEPT varchar(50) NOT NULL,
    IS_ACTIVE boolean DEFAULT TRUE NOT NULL,
    IS_ADMIN boolean DEFAULT FALSE NOT NULL,
    FOREIGN KEY (DEPT) REFERENCES DEPARTMENT (DEPT) ON DELETE CASCADE,
    CHECK (EMAIL LIKE '%@%.%' AND PHONE LIKE '+____________')
);

CREATE TABLE FACULTY_PANEL (
    FAC_ID varchar(50) NOT NULL,
    PANEL_ID bigint NOT NULL,
    IS_COORDINATOR boolean DEFAULT FALSE NOT NULL,
    PRIMARY KEY (FAC_ID, PANEL_ID),
    FOREIGN KEY (FAC_ID) REFERENCES FACULTY (FAC_ID),
    FOREIGN KEY (PANEL_ID) REFERENCES PANEL (PANEL_ID)
);

CREATE TABLE TEAM (
    TEAM_NAME varchar(50) NOT NULL,
    DESCRIPTION varchar(200) DEFAULT NULL,
    GUIDE varchar(50) DEFAULT NULL,
    PANEL_ID bigint DEFAULT NULL,
    TEAM_ID bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    FOREIGN KEY (PANEL_ID) REFERENCES PANEL (PANEL_ID) ON DELETE SET NULL,
    FOREIGN KEY (GUIDE) REFERENCES FACULTY (FAC_ID) ON DELETE SET NULL
);

CREATE TABLE STUDENT (
    SRN varchar(15) PRIMARY KEY,
    NAME varchar(100) NOT NULL,
    EMAIL varchar(100) NOT NULL,
    PHONE varchar(13) NOT NULL,
    DEPT varchar(50) NOT NULL,
    TEAM_ID bigint DEFAULT NULL,
    FOREIGN KEY (TEAM_ID) REFERENCES TEAM (TEAM_ID) ON DELETE SET NULL,
    CHECK (SRN LIKE 'PES%' AND EMAIL LIKE '%@%.%' AND PHONE LIKE '+____________'),
    FOREIGN KEY (DEPT) REFERENCES DEPARTMENT (DEPT)
);

CREATE TABLE TEAM_FACULTY_REVIEW (
    TEAM_ID bigint NOT NULL,
    FAC_ID varchar(50),
    REVIEW_NUMBER int NOT NULL,
    REMARK varchar(200) DEFAULT NULL,
    FOREIGN KEY (TEAM_ID) REFERENCES TEAM (TEAM_ID) ON DELETE CASCADE,
    FOREIGN KEY (FAC_ID) REFERENCES FACULTY (FAC_ID) ON DELETE SET NULL,
    PRIMARY KEY (TEAM_ID, FAC_ID, REVIEW_NUMBER),
    CHECK (REVIEW_NUMBER > 0 AND REVIEW_NUMBER <= 5)
);

CREATE TABLE REVIEW_1 (
    SRN varchar(15) NOT NULL,
    FAC_ID varchar(50),
    PROJECT_WORK int NOT NULL,
    QUALITY_OF_DEMO int NOT NULL,
    PROJECT_REPORT int NOT NULL,
    VIVA_VOCE int NOT NULL,
    COMMENTS varchar(200) DEFAULT NULL,
    PRIMARY KEY (SRN, FAC_ID),
    FOREIGN KEY (SRN) REFERENCES STUDENT (SRN) ON DELETE CASCADE,
    FOREIGN KEY (FAC_ID) REFERENCES FACULTY (FAC_ID) ON DELETE SET NULL,
    CHECK (PROJECT_WORK <= 15 AND PROJECT_WORK >= 0 AND QUALITY_OF_DEMO <= 10 AND QUALITY_OF_DEMO >= 0 AND PROJECT_REPORT <= 10 AND PROJECT_REPORT >= 0 AND VIVA_VOCE <= 5 AND VIVA_VOCE >= 0)
);

CREATE TABLE REVIEW_2 (
    SRN varchar(15) NOT NULL,
    FAC_ID varchar(50),
    PROJECT_WORK int NOT NULL,
    QUALITY_OF_DEMO int NOT NULL,
    PROJECT_REPORT int NOT NULL,
    VIVA_VOCE int NOT NULL,
    COMMENTS varchar(200) DEFAULT NULL,
    PRIMARY KEY (SRN, FAC_ID),
    FOREIGN KEY (SRN) REFERENCES STUDENT (SRN) ON DELETE CASCADE,
    FOREIGN KEY (FAC_ID) REFERENCES FACULTY (FAC_ID) ON DELETE SET NULL,
    CHECK (PROJECT_WORK <= 15 AND PROJECT_WORK >= 0 AND QUALITY_OF_DEMO <= 10 AND QUALITY_OF_DEMO >= 0 AND PROJECT_REPORT <= 10 AND PROJECT_REPORT >= 0 AND VIVA_VOCE <= 5 AND VIVA_VOCE >= 0)
);

CREATE TABLE REVIEW_3 (
    SRN varchar(15) NOT NULL,
    FAC_ID varchar(50),
    PROJECT_WORK int NOT NULL,
    QUALITY_OF_DEMO int NOT NULL,
    PROJECT_REPORT int NOT NULL,
    VIVA_VOCE int NOT NULL,
    COMMENTS varchar(200) DEFAULT NULL,
    PRIMARY KEY (SRN, FAC_ID),
    FOREIGN KEY (SRN) REFERENCES STUDENT (SRN) ON DELETE CASCADE,
    FOREIGN KEY (FAC_ID) REFERENCES FACULTY (FAC_ID) ON DELETE SET NULL,
    CHECK (PROJECT_WORK <= 15 AND PROJECT_WORK >= 0 AND QUALITY_OF_DEMO <= 10 AND QUALITY_OF_DEMO >= 0 AND PROJECT_REPORT <= 10 AND PROJECT_REPORT >= 0 AND VIVA_VOCE <= 5 AND VIVA_VOCE >= 0)
);

CREATE TABLE REVIEW_4 (
    SRN varchar(15) NOT NULL,
    FAC_ID varchar(50),
    PROJECT_WORK int NOT NULL,
    QUALITY_OF_DEMO int NOT NULL,
    PROJECT_REPORT int NOT NULL,
    VIVA_VOCE int NOT NULL,
    COMMENTS varchar(200) DEFAULT NULL,
    PRIMARY KEY (SRN, FAC_ID),
    FOREIGN KEY (SRN) REFERENCES STUDENT (SRN) ON DELETE CASCADE,
    FOREIGN KEY (FAC_ID) REFERENCES FACULTY (FAC_ID) ON DELETE SET NULL,
    CHECK (PROJECT_WORK <= 15 AND PROJECT_WORK >= 0 AND QUALITY_OF_DEMO <= 10 AND QUALITY_OF_DEMO >= 0 AND PROJECT_REPORT <= 10 AND PROJECT_REPORT >= 0 AND VIVA_VOCE <= 5 AND VIVA_VOCE >= 0)
);

CREATE TABLE REVIEW_5 (
    SRN varchar(15) NOT NULL,
    FAC_ID varchar(50),
    PROJECT_WORK int NOT NULL,
    QUALITY_OF_DEMO int NOT NULL,
    PROJECT_REPORT int NOT NULL,
    VIVA_VOCE int NOT NULL,
    COMMENTS varchar(200) DEFAULT NULL,
    PRIMARY KEY (SRN, FAC_ID),
    FOREIGN KEY (SRN) REFERENCES STUDENT (SRN) ON DELETE CASCADE,
    FOREIGN KEY (FAC_ID) REFERENCES FACULTY (FAC_ID) ON DELETE SET NULL,
    CHECK (PROJECT_WORK <= 15 AND PROJECT_WORK >= 0 AND QUALITY_OF_DEMO <= 10 AND QUALITY_OF_DEMO >= 0 AND PROJECT_REPORT <= 10 AND PROJECT_REPORT >= 0 AND VIVA_VOCE <= 5 AND VIVA_VOCE >= 0)
);

