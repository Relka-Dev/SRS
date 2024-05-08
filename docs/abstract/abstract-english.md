---
title: "Abstract - Space Recognition System"
author: Karel Vilém Svoboda
date: May 8, 2024
geometry: margin=2cm
output:
  pdf_document:
    latex_engine: xelatex
---

## Presentation
The Space Recognition System (SRS) is a project that aims to secure a room by detecting the positions and identities of individuals. The system utilizes artificial intelligence technologies to identify and locate people in images or videos.

## Initialization
The administrator begins by initializing the system. After starting the application, if an SRS is detected, the system prompts the administrator to log in using generic credentials provided in the user manual. Once the credentials are verified, the administrator can add the first administrator account. After entering their name and a secure password, they are redirected to the login page, where they are asked to enter the login credentials of the new admin. If the credentials are correct, the administrator gains access to the main page of the application.

## Configuration
The user starts by adding individuals to the system. They must enter each person's name, a picture, and categorize them (e.g., dangerous, associate). Afterward, cameras are placed at each corner of the room, and each camera is assigned a position designation, such as northwest for a camera that is located at the top left of the room.

## Space Recognition
Once the server and cameras are configured, the server processes images captured by the cameras. The system determines the positions of individuals using triangulation between the cameras and attempts to identify their faces using stored data. Once the processing is complete, the application displays each person's position and their identity, if identified.

## Security
From a technical standpoint, the security of the communications is managed using JSON Web Tokens (JWT). Once the administrator enters the correct default credentials, a JWT with a 15-minute lifespan is generated. With this token, the administrator can add the first admin to the database. When the administrator logs in, another JWT is generated with a 24-hour lifespan, granting access to the application's functionality. The Wi-Fi cameras also receive JWTs; when the server needs to access a camera, it logs in using secured credentials. Once verified, a JWT is issued to the server. The server then stores this JWT in the database associated with the camera. This token is used to fetch images or videos for the duration of its validity. Once it expires, the server performs another login to update the token in the database.
