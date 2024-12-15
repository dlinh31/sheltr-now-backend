from flask import Blueprint, jsonify, request
import requests
from ..config import Config
from ..models import db
from app.models import User, Flood_Alert
from datetime import datetime


flood_alert_bp = Blueprint('flood_alert', __name__)
RESULT_LIMIT = 200


@flood_alert_bp.route('/api/get-api-key', methods=['GET'])
def get_api_key():
    if Config.GOOGLE_API_KEY:  # Check if the key is available
        return jsonify({"googleMapsApiKey": Config.GOOGLE_API_KEY})
    else:
        return jsonify({"error": "API key not found"}), 500


@flood_alert_bp.route('/fetch-flood-warnings', methods=['GET'])
def fetch_flood_warnings():
    try:
        # Test onlyyyy
        Flood_Alert.query.delete()
        db.session.commit()

        response = requests.get(
            'https://api.weather.gov/alerts/active?event=Flood%20Warning')
        response.raise_for_status()

        data = response.json()

        features = data['features'][:RESULT_LIMIT]
        flood_alerts = []

        for i, feature in enumerate(features):
            properties = feature['properties']
            geometry = feature['geometry']

            event = properties['event']
            area_desc = properties['areaDesc']
            severity = properties['severity']
            certainty = properties['certainty']
            urgency = properties['urgency']
            headline = properties['headline']
            description = properties['description']
            coordinates = geometry['coordinates']
            effective = datetime.strptime(
                properties['effective'], '%Y-%m-%dT%H:%M:%S%z')
            expires = datetime.strptime(
                properties['expires'], '%Y-%m-%dT%H:%M:%S%z')

            existing_alert = Flood_Alert.query.filter_by(
                headline=headline).first()
            if not existing_alert:
                new_alert = Flood_Alert(
                    event=event,
                    area_desc=area_desc,
                    severity=severity,
                    certainty=certainty,
                    urgency=urgency,
                    headline=headline,
                    description=description,
                    coordinates=str(coordinates),
                    effective=effective,
                    expires=expires
                )

                db.session.add(new_alert)
                db.session.commit()

                flood_alerts.append({
                    "event": event,
                    "area_desc": area_desc,
                    "severity": severity,
                    "certainty": certainty,
                    "urgency": urgency,
                    "headline": headline,
                    "description": description,
                    "coordinates": coordinates,
                    "effective": effective.strftime('%Y-%m-%dT%H:%M:%S%z'),
                    "expires": expires.strftime('%Y-%m-%dT%H:%M:%S%z')
                })

        return jsonify(flood_alerts), 200

    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500


@flood_alert_bp.route('/fetch-flood-alerts-from-db', methods=['GET'])
def fetch_food_alerts_from_db():
    try:
        flood_alerts = Flood_Alert.query.all()
        alerts_list = []
        for alert in flood_alerts:
            alerts_list.append({
                "id": alert.id,
                "event": alert.event,
                "area_desc": alert.area_desc,
                "severity": alert.severity,
                "certainty": alert.certainty,
                "urgency": alert.urgency,
                "headline": alert.headline,
                "description": alert.description,
                "coordinates": alert.coordinates,
                "effective": alert.effective.strftime('%Y-%m-%dT%H:%M:%S%z'),
                "expires": alert.expires.strftime('%Y-%m-%dT%H:%M:%S%z')
            })
        return jsonify(alerts_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
