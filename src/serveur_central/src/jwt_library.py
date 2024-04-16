"""
Auteur      : Karel Vilém Svoboda
Affiliation : CFPTi - SRS
Date        : 16.04.2024

Script      : jwt_library.py
Description : Bibliothèque pour les fonctionnalités liés aux JWT (json web token)
Version     : 0.1
"""

import jwt
import datetime
from functools import wraps
from flask import jsonify, request

class JwtLibrary:
    """
    Classe fournissant des fonctionnalités liées aux JSON Web Tokens (JWT).

    Attributes:
        __SECRET_KEY_FOR_INITIALIZATION (str): Clé secrète utilisée pour générer les JWT d'initialisation.
        __SECRET_KEY_FOR_API (str): Clé secrète utilisée pour générer les JWT pour l'API.
    
    Note : Les fonctionnalités liés à l'initialiation genèrent des clés à durée de vie réduite pour des questions de sécurité. Par conséquent, veuillez les utiliser uniquement à ces fins.
    """

    # Clés secrètes
    __SECRET_KEY_FOR_INITIALIZATION = 'S[26dF9RmVM/#{GT'
    __SECRET_KEY_FOR_API = 'qEcYfxQzC3bS'

    @staticmethod
    def generateJwtForInitialization(username):
        """
        Génère un token d'une courte durée de vie.

        Returns :
            str : Le JWT
        """
        return jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)}, JwtLibrary.__SECRET_KEY_FOR_INITIALIZATION)
    
    @staticmethod
    def generateJwtForAPI(username):
        """
        Génère un token d'une longue durée de vie.

        Returns :
            str : Le JWT
        """
        return jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, JwtLibrary.__SECRET_KEY_FOR_API)
        

    def initialization_token_required(f):
        """
        Fonction décoratrice permettant de forcer une autre fonction d'être identifié par JWT

        Args:
            f : Fonction à décorer

        Returns:
            f : Fonction décorée
        """
        @wraps(f)
        def decorated(*args, **kwargs):
            
            token = request.args.get('token')
            if not token:
                return jsonify({'message' : 'Token is missing'}), 403
            # Try catch car jwt.decode retourne une erreur en cas de non correspondance
            try:
                data = jwt.decode(token, JwtLibrary.__SECRET_KEY_FOR_INITIALIZATION, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired'}), 403
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Token is invalid'}), 403
            return f(*args, **kwargs)

        return decorated
    
    def API_token_required(f):
        """
        Fonction décoratrice permettant de forcer une autre fonction d'être identifié par JWT

        Args:
            f : Fonction à décorer

        Returns:
            f : Fonction décorée
        """
        @wraps(f)
        def decorated(*args, **kwargs):
            
            token = request.args.get('token')
            if not token:
                return jsonify({'message' : 'Token is missing'}), 403
            # Try catch car jwt.decode retourne une erreur en cas de non correspondance
            try:
                data = jwt.decode(token, JwtLibrary.__SECRET_KEY_FOR_INITIALIZATION, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired'}), 403
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Token is invalid'}), 403
            return f(*args, **kwargs)

        return decorated
        