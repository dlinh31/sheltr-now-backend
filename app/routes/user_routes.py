from werkzeug.security import generate_password_hash
from flask import Blueprint, request, jsonify
from ..models import User, SeekerProfile, ProviderProfile, db
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


user_bp = Blueprint('user', __name__)


user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    phone_number = data.get('phone_number')
    role = data.get('role')  # 'seeker' or 'provider'

    if not all([name, email, password, role]):
        return jsonify({"error": "Missing required fields"}), 400

    if role not in ['provider', 'seeker']:
        return jsonify({"error": "Invalid role"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    try:
        new_user = User(
            name=name,
            email=email,
            phone_number=phone_number,
            role=role
        )
        new_user.set_password(password)  

        db.session.add(new_user)
        db.session.commit()

        if role == 'seeker':
            seeker_profile = SeekerProfile(
                user_id=new_user.id,
                emergency_contact=data.get('emergency_contact', '')
            )
            db.session.add(seeker_profile)
        elif role == 'provider':
            provider_profile = ProviderProfile(
                user_id=new_user.id,
                organization_name=data.get('organization_name', '')
            )
            db.session.add(provider_profile)

        db.session.commit()
        
        access_token = create_access_token(
            identity={"id": new_user.id, "role": new_user.role})

        return jsonify({
            "message": f"{role.capitalize()} registered successfully",
            "user": {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email,
                "phone_number": new_user.phone_number,
                "role": new_user.role
            },
            "access_token": access_token
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = create_access_token(
        identity={"id": user.id, "role": user.role})

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone_number": user.phone_number,
            "role": user.role
        }
    }), 200


@user_bp.route('/<int:user_id>/profile', methods=['GET'])
@jwt_required()
def get_seeker_profile(user_id):
    
    current_user = get_jwt_identity()

    if current_user['id'] != user_id and current_user['role'] != 'admin':
        return jsonify({"error": "Unauthorized access"}), 403

    seeker_profile = SeekerProfile.query.filter_by(user_id=user_id).first()

    if not seeker_profile:
        return jsonify({"error": "Seeker profile not found"}), 404

    seeker_data = {
        "emergency_contact": seeker_profile.emergency_contact,
        "current_location": seeker_profile.current_location,
        "preferred_radius": seeker_profile.preferred_radius
    }

    return jsonify(seeker_data), 200
    

@user_bp.route('/logout', methods=['POST'])
@jwt_required
def logout():
    return jsonify({"message": "Logged out successfully"}), 200
    