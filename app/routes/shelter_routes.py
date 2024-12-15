from flask import Blueprint, request, jsonify
from app.models import Shelter, ProviderProfile, User, db

shelter_bp = Blueprint('shelter', __name__)


# Create shelter
@shelter_bp.route('/<int:user_id>/add-shelter', methods=['POST'])
def add_shelter(user_id):
    data = request.get_json()
    provider = ProviderProfile.query.filter_by(user_id=user_id).first()

    if not provider:
        return jsonify({"error": "Provider not found"}), 404

    new_shelter = Shelter(
        name=data['name'],
        latitude=data['latitude'],
        longitude=data['longitude'],
        address=data.get('address'),
        capacity=data['capacity'],
        current_occupancy=data['current_occupancy'],
        provider_profile_id=provider.id
    )

    db.session.add(new_shelter)
    db.session.commit()

    return jsonify({"message": "Shelter added successfully", "shelter_id": new_shelter.id}), 201

@shelter_bp.route('/<int:user_id>/get-shelter', methods=['GET'])
def get_shelter_from_user(user_id):
    provider = ProviderProfile.query.filter_by(user_id=user_id).first()
    if not provider:
        return jsonify({"error": "Provider not found"}), 404
    shelters = Shelter.query.filter_by(provider_profile_id=provider.id)
    print(shelters)
    if not shelters:
        return jsonify([]), 200
    res = []
    for shelter in shelters:
        res.append({
            "id": shelter.id,
            "name": shelter.name,
            "address": shelter.address,
            "latitude": shelter.latitude,
            "longitude": shelter.longitude,
            "capacity": shelter.capacity,
            "current_occupancy": shelter.current_occupancy
        })
    return jsonify(res), 200

# Update existing shelter
@shelter_bp.route('/<int:user_id>/update-shelter/<int:shelter_id>', methods=['PUT'])
def update_shelter(user_id, shelter_id):
    data = request.get_json()
    shelter = Shelter.query.filter_by(
        id=shelter_id, provider_profile_id=user_id).first()
    if shelter:
        shelter.name = data.get('name', shelter.name)
        shelter.latitude = data.get('latitude', shelter.latitude)
        shelter.longitude = data.get('longitude', shelter.longitude)
        shelter.address = data.get('address', shelter.address)
        shelter.capacity = data.get('capacity', shelter.capacity)
        shelter.current_occupancy = data.get(
            'current_occupancy', shelter.current_occupancy)
        db.session.commit()
        return jsonify({"message": "Shelter updated successfully"}), 200
    return jsonify({"error": "Shelter not found"}), 404


# Fetch all shelters for a provider
@shelter_bp.route('/<int:user_id>', methods=['GET'])
def get_shelters(user_id):
    provider = ProviderProfile.query.filter_by(user_id=user_id).first()

    if not provider:
        return jsonify({"error": "Provider not found"}), 404

    shelters = Shelter.query.filter_by(provider_profile_id=provider.id).all()
    shelter_list = []

    for shelter in shelters:
        shelter_list.append({
            "id": shelter.id,
            "name": shelter.name,
            "address": shelter.address,
            "latitude": shelter.latitude,
            "longitude": shelter.longitude,
            "capacity": shelter.capacity,
            "current_occupancy": shelter.current_occupancy
        })

    return jsonify(shelter_list), 200


# Delete shelter
@shelter_bp.route('/<int:user_id>/delete-shelter/<int:shelter_id>', methods=['DELETE'])
def delete_shelter(user_id, shelter_id):
    shelter = Shelter.query.filter_by(
        id=shelter_id, provider_profile_id=user_id).first()
    if shelter:
        db.session.delete(shelter)
        db.session.commit()
        return jsonify({"message": "Shelter deleted successfully"}), 200
    return jsonify({"error": "Shelter not found"}), 404


# Get all shelters
@shelter_bp.route('/', methods=['GET'])
def get_all_shelters():
    shelters = Shelter.query.all()
    shelter_list = []

    for shelter in shelters:
        shelter_list.append({
            "id": shelter.id,
            "name": shelter.name,
            "address": shelter.address,
            "latitude": shelter.latitude,
            "longitude": shelter.longitude,
            "capacity": shelter.capacity,
            "current_occupancy": shelter.current_occupancy
        })

    return jsonify(shelter_list), 200

@shelter_bp.route('/<int:shelter_id>/provider', methods=['GET'])
def get_provider_from_shelter(shelter_id):
    shelter = Shelter.query.get(shelter_id)
    if not shelter:
        return jsonify({"error": "Shelter not found"}), 404

    provider = shelter.provider
    if not provider:
        return jsonify({"error": "Provider not found"}), 404
    
    user = User.query.get(provider.user_id)

    return jsonify({
        "provider_id": provider.id,
        "organization_name": provider.organization_name,
        "address": provider.address,
        "user_id": provider.user_id,
        "name": user.name,
        "phone_number": user.phone_number,
        "email": user.email
    }), 200
    
    
        
