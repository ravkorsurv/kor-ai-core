"""
Regulatory Explainability Module

Converts soft probabilities into deterministic narratives suitable for regulatory compliance.
Provides structured inference paths, rationale attachment, STOR-ready exports, and VOI/sensitivity reporting.
"""

import json
import csv
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class InferencePath:
    """Represents a structured inference path from evidence to conclusion"""
    evidence_node: str
    evidence_state: str
    evidence_weight: float
    inference_rule: str
    conclusion_impact: str
    confidence_level: str

@dataclass
class RegulatoryRationale:
    """Structured rationale for regulatory compliance"""
    alert_id: str
    timestamp: str
    risk_level: str
    overall_score: float
    deterministic_narrative: str
    inference_paths: List[InferencePath]
    key_evidence: Dict[str, Any]
    regulatory_basis: str
    audit_trail: List[str]

@dataclass
class STORRecord:
    """STOR (Suspicious Transaction Order Report) record format"""
    record_id: str
    timestamp: str
    entity_id: str
    transaction_type: str
    risk_score: float
    risk_level: str
    narrative: str
    evidence_summary: str
    regulatory_basis: str

class RegulatoryExplainability:
    """
    Converts probabilistic Bayesian outputs into deterministic regulatory narratives
    """
    
    def __init__(self):
        self.risk_thresholds = {
            'low': 0.3,
            'medium': 0.6,
            'high': 0.8
        }
        
        self.regulatory_basis_map = {
            'insider_dealing': 'Market Abuse Regulation (MAR) Article 14',
            'spoofing': 'MiFID II Article 48 - Market manipulation',
            'market_manipulation': 'MAR Article 12 - Market manipulation'
        }
    
    def generate_regulatory_rationale(
        self, 
        alert_id: str,
        risk_result: Dict[str, Any],
        evidence_factors: Dict[str, Any],
        model_type: str = 'insider_dealing'
    ) -> RegulatoryRationale:
        """
        Generate structured regulatory rationale from Bayesian risk assessment
        """
        try:
            # Extract key information
            overall_score = risk_result.get('overall_score', 0.0)
            risk_level = risk_result.get('risk_level', 'low')
            
            # Generate deterministic narrative
            narrative = self._generate_deterministic_narrative(
                risk_result, evidence_factors, model_type
            )
            
            # Build inference paths
            inference_paths = self._build_inference_paths(evidence_factors, risk_result)
            
            # Identify key evidence
            key_evidence = self._identify_key_evidence(evidence_factors, risk_result)
            
            # Get regulatory basis
            regulatory_basis = self.regulatory_basis_map.get(model_type, 'General market abuse regulations')
            
            # Create audit trail
            audit_trail = self._create_audit_trail(risk_result, evidence_factors)
            
            return RegulatoryRationale(
                alert_id=alert_id,
                timestamp=datetime.now().isoformat(),
                risk_level=risk_level,
                overall_score=overall_score,
                deterministic_narrative=narrative,
                inference_paths=inference_paths,
                key_evidence=key_evidence,
                regulatory_basis=regulatory_basis,
                audit_trail=audit_trail
            )
            
        except Exception as e:
            logger.error(f"Error generating regulatory rationale: {str(e)}")
            # Return fallback rationale
            return self._create_fallback_rationale(alert_id, risk_result, model_type)
    
    def _generate_deterministic_narrative(
        self, 
        risk_result: Dict[str, Any], 
        evidence_factors: Dict[str, Any],
        model_type: str
    ) -> str:
        """Convert probabilistic assessment into deterministic narrative"""
        
        overall_score = risk_result.get('overall_score', 0.0)
        risk_level = risk_result.get('risk_level', 'low')
        
        if model_type == 'insider_dealing':
            return self._generate_insider_dealing_narrative(risk_result, evidence_factors)
        elif model_type == 'spoofing':
            return self._generate_spoofing_narrative(risk_result, evidence_factors)
        else:
            return self._generate_general_narrative(risk_result, evidence_factors)
    
    def _generate_insider_dealing_narrative(
        self, 
        risk_result: Dict[str, Any], 
        evidence_factors: Dict[str, Any]
    ) -> str:
        """Generate insider dealing specific narrative"""
        
        material_info = evidence_factors.get('MaterialInfo', 0)
        trading_activity = evidence_factors.get('TradingActivity', 0)
        timing = evidence_factors.get('Timing', 0)
        price_impact = evidence_factors.get('PriceImpact', 0)
        
        narrative_parts = []
        
        # Material information access
        if material_info == 2:
            narrative_parts.append("Clear access to material non-public information")
        elif material_info == 1:
            narrative_parts.append("Potential access to material information")
        
        # Trading activity
        if trading_activity == 2:
            narrative_parts.append("highly unusual trading patterns")
        elif trading_activity == 1:
            narrative_parts.append("unusual trading activity")
        
        # Timing
        if timing == 2:
            narrative_parts.append("suspicious timing relative to material events")
        elif timing == 1:
            narrative_parts.append("questionable timing")
        
        # Price impact
        if price_impact == 2:
            narrative_parts.append("significant price impact")
        elif price_impact == 1:
            narrative_parts.append("moderate price impact")
        
        if narrative_parts:
            return f"Detected potential insider dealing based on {' and '.join(narrative_parts)}."
        else:
            return "No significant insider dealing indicators detected."
    
    def _generate_spoofing_narrative(
        self, 
        risk_result: Dict[str, Any], 
        evidence_factors: Dict[str, Any]
    ) -> str:
        """Generate spoofing specific narrative"""
        
        order_pattern = evidence_factors.get('OrderPattern', 0)
        cancellation_rate = evidence_factors.get('CancellationRate', 0)
        price_movement = evidence_factors.get('PriceMovement', 0)
        volume_ratio = evidence_factors.get('VolumeRatio', 0)
        
        narrative_parts = []
        
        if order_pattern == 2:
            narrative_parts.append("manipulative order patterns")
        elif order_pattern == 1:
            narrative_parts.append("suspicious order behavior")
        
        if cancellation_rate == 2:
            narrative_parts.append("excessive order cancellations")
        elif cancellation_rate == 1:
            narrative_parts.append("high cancellation rate")
        
        if price_movement == 2:
            narrative_parts.append("artificial price movements")
        elif price_movement == 1:
            narrative_parts.append("suspicious price activity")
        
        if volume_ratio == 2:
            narrative_parts.append("manipulative volume patterns")
        elif volume_ratio == 1:
            narrative_parts.append("unusual volume activity")
        
        if narrative_parts:
            return f"Detected potential spoofing behavior based on {' and '.join(narrative_parts)}."
        else:
            return "No significant spoofing indicators detected."
    
    def _generate_general_narrative(
        self, 
        risk_result: Dict[str, Any], 
        evidence_factors: Dict[str, Any]
    ) -> str:
        """Generate general market abuse narrative"""
        
        overall_score = risk_result.get('overall_score', 0.0)
        risk_level = risk_result.get('risk_level', 'low')
        
        if overall_score > 0.8:
            return "High probability of market abuse detected based on multiple risk indicators."
        elif overall_score > 0.6:
            return "Moderate probability of market abuse detected based on several risk factors."
        elif overall_score > 0.3:
            return "Low probability of market abuse detected with some concerning indicators."
        else:
            return "No significant market abuse indicators detected."
    
    def _build_inference_paths(
        self, 
        evidence_factors: Dict[str, Any], 
        risk_result: Dict[str, Any]
    ) -> List[InferencePath]:
        """Build structured inference paths from evidence to conclusion"""
        
        paths = []
        
        for factor, state in evidence_factors.items():
            if state > 0:  # Only include non-zero evidence
                weight = self._calculate_evidence_weight(factor, state)
                rule = self._get_inference_rule(factor, state)
                impact = self._get_conclusion_impact(factor, state)
                confidence = self._get_confidence_level(state)
                
                paths.append(InferencePath(
                    evidence_node=factor,
                    evidence_state=str(state),
                    evidence_weight=weight,
                    inference_rule=rule,
                    conclusion_impact=impact,
                    confidence_level=confidence
                ))
        
        return paths
    
    def _calculate_evidence_weight(self, factor: str, state: int) -> float:
        """Calculate the weight of evidence based on factor and state"""
        base_weights = {
            'MaterialInfo': [0.1, 0.3, 0.6],
            'TradingActivity': [0.1, 0.4, 0.7],
            'Timing': [0.1, 0.3, 0.5],
            'PriceImpact': [0.1, 0.3, 0.5],
            'OrderPattern': [0.1, 0.4, 0.7],
            'CancellationRate': [0.1, 0.3, 0.6],
            'PriceMovement': [0.1, 0.3, 0.5],
            'VolumeRatio': [0.1, 0.3, 0.5]
        }
        
        weights = base_weights.get(factor, [0.1, 0.3, 0.5])
        return weights[min(state, len(weights) - 1)]
    
    def _get_inference_rule(self, factor: str, state: int) -> str:
        """Get the inference rule applied to this evidence"""
        rules = {
            'MaterialInfo': ['No access', 'Potential access', 'Clear access'],
            'TradingActivity': ['Normal', 'Unusual', 'Highly unusual'],
            'Timing': ['Normal', 'Suspicious', 'Highly suspicious'],
            'PriceImpact': ['Low', 'Medium', 'High'],
            'OrderPattern': ['Normal', 'Suspicious', 'Manipulative'],
            'CancellationRate': ['Low', 'High', 'Excessive'],
            'PriceMovement': ['Normal', 'Suspicious', 'Artificial'],
            'VolumeRatio': ['Normal', 'Unusual', 'Manipulative']
        }
        
        factor_rules = rules.get(factor, ['Normal', 'Suspicious', 'High'])
        return factor_rules[min(state, len(factor_rules) - 1)]
    
    def _get_conclusion_impact(self, factor: str, state: int) -> str:
        """Get the impact of this evidence on the conclusion"""
        if state == 0:
            return "No impact"
        elif state == 1:
            return "Moderate impact"
        else:
            return "High impact"
    
    def _get_confidence_level(self, state: int) -> str:
        """Get confidence level based on evidence state"""
        if state == 0:
            return "Low"
        elif state == 1:
            return "Medium"
        else:
            return "High"
    
    def _identify_key_evidence(
        self, 
        evidence_factors: Dict[str, Any], 
        risk_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Identify the most important evidence factors"""
        
        # Sort evidence by state (higher state = more important)
        sorted_evidence = sorted(
            evidence_factors.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        key_evidence = {}
        for factor, state in sorted_evidence[:3]:  # Top 3 factors
            if state > 0:
                key_evidence[factor] = {
                    'state': state,
                    'weight': self._calculate_evidence_weight(factor, state),
                    'description': self._get_inference_rule(factor, state)
                }
        
        return key_evidence
    
    def _create_audit_trail(
        self, 
        risk_result: Dict[str, Any], 
        evidence_factors: Dict[str, Any]
    ) -> List[str]:
        """Create audit trail of decision-making process"""
        
        trail = []
        trail.append(f"Risk assessment initiated at {datetime.now().isoformat()}")
        trail.append(f"Evidence factors processed: {len(evidence_factors)}")
        
        for factor, state in evidence_factors.items():
            if state > 0:
                trail.append(f"Factor {factor}: State {state} - {self._get_inference_rule(factor, state)}")
        
        trail.append(f"Overall risk score: {risk_result.get('overall_score', 0.0):.3f}")
        trail.append(f"Risk level: {risk_result.get('risk_level', 'low')}")
        
        return trail
    
    def _create_fallback_rationale(
        self, 
        alert_id: str, 
        risk_result: Dict[str, Any], 
        model_type: str
    ) -> RegulatoryRationale:
        """Create fallback rationale when generation fails"""
        
        return RegulatoryRationale(
            alert_id=alert_id,
            timestamp=datetime.now().isoformat(),
            risk_level=risk_result.get('risk_level', 'low'),
            overall_score=risk_result.get('overall_score', 0.0),
            deterministic_narrative="Risk assessment completed with standard procedures.",
            inference_paths=[],
            key_evidence={},
            regulatory_basis=self.regulatory_basis_map.get(model_type, 'General market abuse regulations'),
            audit_trail=["Fallback rationale generated due to processing error"]
        )
    
    def generate_voi_analysis(self, evidence_factors: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Value of Information (VOI) analysis"""
        
        voi_results = {}
        
        for factor, state in evidence_factors.items():
            if state == 0:  # Missing evidence
                voi_results[factor] = {
                    'current_state': 'Missing',
                    'potential_value': 'High',
                    'recommended_action': 'Collect additional evidence',
                    'priority': 'High'
                }
            elif state == 1:  # Partial evidence
                voi_results[factor] = {
                    'current_state': 'Partial',
                    'potential_value': 'Medium',
                    'recommended_action': 'Enhance monitoring',
                    'priority': 'Medium'
                }
            else:  # Complete evidence
                voi_results[factor] = {
                    'current_state': 'Complete',
                    'potential_value': 'Low',
                    'recommended_action': 'Maintain current level',
                    'priority': 'Low'
                }
        
        return voi_results
    
    def generate_sensitivity_report(
        self, 
        risk_result: Dict[str, Any], 
        evidence_factors: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate sensitivity analysis report"""
        
        base_score = risk_result.get('overall_score', 0.0)
        sensitivity_results = {}
        
        for factor, state in evidence_factors.items():
            # Simulate how risk score changes with different evidence states
            scenarios = {}
            for new_state in [0, 1, 2]:
                if new_state != state:
                    # Simple sensitivity: higher state = higher risk
                    score_change = (new_state - state) * 0.1
                    new_score = max(0.0, min(1.0, base_score + score_change))
                    scenarios[f"state_{new_state}"] = {
                        'new_score': new_score,
                        'change': score_change,
                        'impact': 'High' if abs(score_change) > 0.2 else 'Medium' if abs(score_change) > 0.1 else 'Low'
                    }
            
            sensitivity_results[factor] = {
                'current_state': state,
                'current_impact': self._calculate_evidence_weight(factor, state),
                'scenarios': scenarios
            }
        
        return sensitivity_results
    
    def export_stor_format(self, rationale: RegulatoryRationale) -> STORRecord:
        """Export rationale in STOR format"""
        
        return STORRecord(
            record_id=rationale.alert_id,
            timestamp=rationale.timestamp,
            entity_id="ENTITY_ID",  # Would be extracted from data
            transaction_type="SUSPICIOUS_ACTIVITY",
            risk_score=rationale.overall_score,
            risk_level=rationale.risk_level,
            narrative=rationale.deterministic_narrative,
            evidence_summary=json.dumps(rationale.key_evidence),
            regulatory_basis=rationale.regulatory_basis
        )
    
    def export_csv_format(self, rationale: RegulatoryRationale) -> str:
        """Export rationale in CSV format"""
        
        # Create CSV content
        csv_lines = []
        csv_lines.append("Alert ID,Timestamp,Risk Level,Overall Score,Narrative,Regulatory Basis")
        csv_lines.append(f"{rationale.alert_id},{rationale.timestamp},{rationale.risk_level},{rationale.overall_score:.3f},\"{rationale.deterministic_narrative}\",{rationale.regulatory_basis}")
        
        # Add inference paths
        csv_lines.append("")
        csv_lines.append("Inference Paths:")
        csv_lines.append("Evidence Node,Evidence State,Evidence Weight,Inference Rule,Conclusion Impact,Confidence Level")
        
        for path in rationale.inference_paths:
            csv_lines.append(f"{path.evidence_node},{path.evidence_state},{path.evidence_weight:.3f},{path.inference_rule},{path.conclusion_impact},{path.confidence_level}")
        
        # Add key evidence
        csv_lines.append("")
        csv_lines.append("Key Evidence:")
        csv_lines.append("Factor,State,Weight,Description")
        
        for factor, details in rationale.key_evidence.items():
            csv_lines.append(f"{factor},{details['state']},{details['weight']:.3f},{details['description']}")
        
        return "\n".join(csv_lines)
