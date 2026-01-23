"""
Dashboard Blueprint
Handles user dashboard and analysis history
"""
from flask import Blueprint, request, jsonify
from backend.auth_utils import require_auth
from backend.database import get_analyses_collection
from datetime import datetime
from bson import ObjectId

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/analyses', methods=['GET'])
@require_auth
def get_analyses():
    """Get all analyses for the current user"""
    try:
        user_id = request.user_id
        
        # Get query parameters
        limit = int(request.args.get('limit', 50))
        skip = int(request.args.get('skip', 0))
        
        analyses_collection = get_analyses_collection()
        
        # Get analyses sorted by created_at descending
        cursor = analyses_collection.find({'user_id': user_id}) \
            .sort('created_at', -1) \
            .skip(skip) \
            .limit(limit)
        
        analyses = []
        for analysis in cursor:
            analysis['_id'] = str(analysis['_id'])
            if 'created_at' in analysis:
                analysis['created_at'] = analysis['created_at'].isoformat()
            if 'file_info' in analysis and analysis['file_info'] and '_id' in analysis['file_info']:
                analysis['file_info']['_id'] = str(analysis['file_info']['_id'])
            analyses.append(analysis)
        
        # Get total count
        total_count = analyses_collection.count_documents({'user_id': user_id})
        
        return jsonify({
            'analyses': analyses,
            'total': total_count,
            'limit': limit,
            'skip': skip
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve analyses: {str(e)}'}), 500

@dashboard_bp.route('/analyses/<analysis_id>', methods=['DELETE'])
@require_auth
def delete_analysis(analysis_id):
    """Delete an analysis"""
    try:
        user_id = request.user_id
        analyses_collection = get_analyses_collection()
        
        # Verify ownership and delete
        result = analyses_collection.delete_one({
            '_id': ObjectId(analysis_id),
            'user_id': user_id
        })
        
        if result.deleted_count == 0:
            return jsonify({'error': 'Analysis not found or unauthorized'}), 404
        
        return jsonify({
            'message': 'Analysis deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to delete analysis: {str(e)}'}), 500

@dashboard_bp.route('/stats', methods=['GET'])
@require_auth
def get_stats():
    """Get user statistics"""
    try:
        user_id = request.user_id
        analyses_collection = get_analyses_collection()
        
        # Get all analyses for user
        analyses = list(analyses_collection.find({'user_id': user_id}))
        
        total_analyses = len(analyses)
        safe_count = sum(1 for a in analyses if a.get('risk_level') == 'Safe')
        suspicious_count = sum(1 for a in analyses if a.get('risk_level') == 'Suspicious')
        high_risk_count = sum(1 for a in analyses if a.get('risk_level') == 'High Risk')
        
        avg_trust_score = 0
        if total_analyses > 0:
            avg_trust_score = sum(a.get('trust_score', 0) for a in analyses) / total_analyses
        
        return jsonify({
            'total_analyses': total_analyses,
            'safe_count': safe_count,
            'suspicious_count': suspicious_count,
            'high_risk_count': high_risk_count,
            'average_trust_score': round(avg_trust_score, 2)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve stats: {str(e)}'}), 500
