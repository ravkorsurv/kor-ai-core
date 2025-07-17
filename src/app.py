import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
import traceback

from core.bayesian_engine import BayesianEngine
from core.data_processor import DataProcessor
from core.alert_generator import AlertGenerator
from core.risk_calculator import RiskCalculator
from core.trading_data_service import TradingDataService
from utils.config import Config
from utils.logger import setup_logger
from api.v1.routes.trading_data import trading_data_bp

# Initialize core components
config = Config()

# Initialize Flask app
app = Flask(__name__)

# Setup CORS with configuration
cors_origins = config.get_security_config().get('cors_origins', ['http://localhost:3000'])
CORS(app, origins=cors_origins, allow_headers=["Content-Type", "Authorization"])

# Setup logging
logger = setup_logger()
bayesian_engine = BayesianEngine()
data_processor = DataProcessor()
alert_generator = AlertGenerator()
risk_calculator = RiskCalculator()
trading_data_service = TradingDataService()

# Register blueprints
app.register_blueprint(trading_data_bp, url_prefix='/api/v1')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'kor-ai-surveillance-platform'
    })

@app.route('/api/v1/analyze', methods=['POST'])
def analyze_trading_data():
    """Main endpoint to analyze trading data for market abuse risks"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Process incoming trading data
        processed_data = data_processor.process(data)
        
        # Check for latent intent flag
        use_latent_intent = data.get('use_latent_intent', False)
        
        # Check for regulatory explainability flag
        include_regulatory_rationale = data.get('include_regulatory_rationale', False)
        
        # Calculate risk scores using Bayesian models
        if use_latent_intent:
            insider_dealing_score = bayesian_engine.calculate_insider_dealing_risk_with_latent_intent(processed_data)
        else:
            insider_dealing_score = bayesian_engine.calculate_insider_dealing_risk(processed_data)
        spoofing_score = bayesian_engine.calculate_spoofing_risk(processed_data)
        
        # Generate overall risk assessment
        overall_risk = risk_calculator.calculate_overall_risk(
            insider_dealing_score, spoofing_score, processed_data
        )
        
        # Generate alerts if thresholds exceeded
        alerts = alert_generator.generate_alerts(
            processed_data, insider_dealing_score, spoofing_score, overall_risk
        )
        
        # Generate regulatory rationale if requested
        regulatory_rationales = []
        if include_regulatory_rationale and alerts:
            for alert in alerts:
                try:
                    # Determine which risk scores to use based on alert type
                    if alert['type'] == 'INSIDER_DEALING':
                        risk_scores = insider_dealing_score
                    elif alert['type'] == 'SPOOFING':
                        risk_scores = spoofing_score
                    else:
                        risk_scores = {'overall_score': overall_risk}
                    
                    rationale = alert_generator.generate_regulatory_rationale(
                        alert, risk_scores, processed_data
                    )
                    regulatory_rationales.append({
                        'alert_id': alert['id'],
                        'deterministic_narrative': rationale.deterministic_narrative,
                        'inference_paths': [
                            {
                                'node_name': path.node_name,
                                'evidence_value': path.evidence_value,
                                'probability': path.probability,
                                'contribution': path.contribution,
                                'rationale': path.rationale,
                                'confidence': path.confidence,
                                'regulatory_relevance': path.regulatory_relevance
                            }
                            for path in rationale.inference_paths
                        ],
                        'voi_analysis': rationale.voi_analysis,
                        'sensitivity_report': rationale.sensitivity_report,
                        'regulatory_frameworks': rationale.regulatory_frameworks,
                        'audit_trail': rationale.audit_trail
                    })
                except Exception as e:
                    logger.error(f"Error generating regulatory rationale for alert {alert['id']}: {str(e)}")
        
        response = {
            'timestamp': datetime.utcnow().isoformat(),
            'analysis_id': f"analysis_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            'risk_scores': {
                'insider_dealing': insider_dealing_score,
                'spoofing': spoofing_score,
                'overall_risk': overall_risk
            },
            'alerts': alerts,
            'regulatory_rationales': regulatory_rationales if include_regulatory_rationale else [],
            'processed_data_summary': {
                'trades_analyzed': len(processed_data.get('trades', [])),
                'timeframe': processed_data.get('timeframe', 'unknown'),
                'instruments': processed_data.get('instruments', [])
            }
        }
        
        logger.info(f"Analysis completed for {len(processed_data.get('trades', []))} trades")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in analyze_trading_data: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@app.route('/api/v1/models/info', methods=['GET'])
def get_models_info():
    """Get information about available Bayesian models"""
    try:
        models_info = bayesian_engine.get_models_info()
        return jsonify(models_info)
    except Exception as e:
        logger.error(f"Error getting models info: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/v1/simulate', methods=['POST'])
def simulate_scenario():
    """Simulate a specific market abuse scenario for testing"""
    try:
        data = request.get_json()
        scenario_type = data.get('scenario_type')
        parameters = data.get('parameters', {})
        
        if scenario_type not in ['insider_dealing', 'spoofing']:
            return jsonify({'error': 'Invalid scenario type'}), 400
        
        # Generate simulated data
        simulated_data = data_processor.generate_simulation_data(scenario_type, parameters)
        
        # Analyze simulated data
        if scenario_type == 'insider_dealing':
            risk_score = bayesian_engine.calculate_insider_dealing_risk(simulated_data)
        else:
            risk_score = bayesian_engine.calculate_spoofing_risk(simulated_data)
        
        response = {
            'scenario_type': scenario_type,
            'parameters': parameters,
            'risk_score': risk_score,
            'simulated_data': simulated_data,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in simulate_scenario: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/v1/alerts/history', methods=['GET'])
def get_alerts_history():
    """Get historical alerts"""
    try:
        limit = request.args.get('limit', 100, type=int)
        alert_type = request.args.get('type')
        
        alerts = alert_generator.get_historical_alerts(limit=limit, alert_type=alert_type)
        
        return jsonify({
            'alerts': alerts,
            'count': len(alerts),
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting alerts history: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/v1/export/stor/<alert_id>', methods=['POST'])
def export_stor_report(alert_id):
    """Export alert in STOR format"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Process data and generate alert
        processed_data = data_processor.process(data)
        
        # Calculate risk scores
        insider_dealing_score = bayesian_engine.calculate_insider_dealing_risk(processed_data)
        spoofing_score = bayesian_engine.calculate_spoofing_risk(processed_data)
        overall_risk = risk_calculator.calculate_overall_risk(
            insider_dealing_score, spoofing_score, processed_data
        )
        
        # Generate alerts
        alerts = alert_generator.generate_alerts(
            processed_data, insider_dealing_score, spoofing_score, overall_risk
        )
        
        # Find the specific alert
        target_alert = None
        for alert in alerts:
            if alert['id'] == alert_id:
                target_alert = alert
                break
        
        if not target_alert:
            return jsonify({'error': f'Alert {alert_id} not found'}), 404
        
        # Determine risk scores for the alert
        if target_alert['type'] == 'INSIDER_DEALING':
            risk_scores = insider_dealing_score
        elif target_alert['type'] == 'SPOOFING':
            risk_scores = spoofing_score
        else:
            risk_scores = {'overall_score': overall_risk}
        
        # Export STOR format
        stor_record = alert_generator.export_stor_report(target_alert, risk_scores, processed_data)
        
        return jsonify({
            'stor_record': {
                'record_id': stor_record.record_id,
                'timestamp': stor_record.timestamp,
                'trader_id': stor_record.trader_id,
                'instrument': stor_record.instrument,
                'transaction_type': stor_record.transaction_type,
                'suspicious_indicators': stor_record.suspicious_indicators,
                'risk_score': stor_record.risk_score,
                'regulatory_rationale': stor_record.regulatory_rationale,
                'evidence_details': stor_record.evidence_details,
                'compliance_officer_notes': stor_record.compliance_officer_notes
            }
        })
        
    except Exception as e:
        logger.error(f"Error exporting STOR report: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/export/csv/<alert_id>', methods=['POST'])
def export_regulatory_csv(alert_id):
    """Export regulatory rationale as CSV"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Process data and generate alert
        processed_data = data_processor.process(data)
        
        # Calculate risk scores
        insider_dealing_score = bayesian_engine.calculate_insider_dealing_risk(processed_data)
        spoofing_score = bayesian_engine.calculate_spoofing_risk(processed_data)
        overall_risk = risk_calculator.calculate_overall_risk(
            insider_dealing_score, spoofing_score, processed_data
        )
        
        # Generate alerts
        alerts = alert_generator.generate_alerts(
            processed_data, insider_dealing_score, spoofing_score, overall_risk
        )
        
        # Find the specific alert
        target_alert = None
        for alert in alerts:
            if alert['id'] == alert_id:
                target_alert = alert
                break
        
        if not target_alert:
            return jsonify({'error': f'Alert {alert_id} not found'}), 404
        
        # Determine risk scores for the alert
        if target_alert['type'] == 'INSIDER_DEALING':
            risk_scores = insider_dealing_score
        elif target_alert['type'] == 'SPOOFING':
            risk_scores = spoofing_score
        else:
            risk_scores = {'overall_score': overall_risk}
        
        # Export CSV
        filename = alert_generator.export_regulatory_csv(target_alert, risk_scores, processed_data)
        
        return jsonify({
            'csv_export': {
                'filename': filename,
                'message': f'Regulatory report exported to {filename}'
            }
        })
        
    except Exception as e:
        logger.error(f"Error exporting regulatory CSV: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    server_config = config.get_server_config()
    
    port = server_config.get('port', 5000)
    host = server_config.get('host', '0.0.0.0')
    debug = server_config.get('debug', False)
    
    logger.info(f"Starting Korinsic Surveillance Platform on {host}:{port} (debug={debug})")
    logger.info(f"Environment: {config.environment}")
    
    app.run(host=host, port=port, debug=debug)