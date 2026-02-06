import random
import re
from typing import List, Dict, Optional
from .models import RiskScore

class AIEngine:
    def __init__(self):
        # Expanded keywords associated with drug trafficking and suspicious behavior
        self.trigger_keywords = [
            "ice", "crystal", "meth", "pill", "delivery", "shipping", 
            "discrete", "telegram me", "wickr", "plug", "stash",
            "xanax", "adderall", "oxy", "coke", "snow", "white",
            "green", "herb", "bud", "fast shipping", "overnight",
            "direct message", "private deal", "unmarked", "fent",
            "perc", "bars", "stamps", "bricks", "weight", "oz",
            "gram", "wholesale"
        ]

    def classify_intent(self, text: str) -> Dict:
        """Simple keyword-based intent classification for demo purposes."""
        text_lower = text.lower()
        matches = [kw for kw in self.trigger_keywords if kw in text_lower]
        
        if len(matches) > 2:
            intent = "selling"
            confidence = 0.85 + (random.random() * 0.1)
        elif len(matches) > 0:
            intent = "suspicious"
            confidence = 0.6 + (random.random() * 0.2)
        else:
            intent = "neutral"
            confidence = 0.9 + (random.random() * 0.05)
            
        return {"intent": intent, "confidence": confidence, "matches": matches}

    def detect_objects(self, image_url: Optional[str]) -> Dict:
        """Mock image detection logic."""
        if not image_url:
            return {"detected": False, "confidence": 0.0, "objects": []}
        
        # In a real scenario, this would call a YOLO/Computer Vision model
        # For demo, we simulate a detection if the URL contains "drug" or "suspicious"
        if image_url and ("drug" in image_url.lower() or "pill" in image_url.lower()):
            return {
                "detected": True, 
                "confidence": 0.75 + (random.random() * 0.2), 
                "objects": ["pills", "packaging"]
            }
        
        return {"detected": False, "confidence": 0.1, "objects": []}

    def calculate_risk(self, post_content: str, image_url: Optional[str]) -> RiskScore:
        nlp_result = self.classify_intent(post_content)
        img_result = self.detect_objects(image_url)
        
        # Behavioral score (mocked as randomized for now)
        behavioral_score = random.randint(20, 90) if nlp_result["intent"] != "neutral" else random.randint(0, 30)
        
        # Weighted Risk Calculation
        # NLP (40%) + Image (30%) + Behavioral (30%)
        base_score = (nlp_result["confidence"] * 40 if nlp_result["intent"] != "neutral" else 0) + \
                     (img_result["confidence"] * 30) + \
                     (behavioral_score * 0.3)
        
        final_score = min(int(base_score), 100)
        
        level = "Low"
        if final_score > 70:
            level = "High"
        elif final_score > 40:
            level = "Medium"
            
        reasoning = []
        if nlp_result["intent"] != "neutral":
            reasoning.append(f"Suspicious intent detected: {nlp_result['intent']} ({len(nlp_result['matches'])} markers)")
        if img_result["detected"]:
            reasoning.append(f"Visual markers identified: {', '.join(img_result['objects'])}")
        if behavioral_score > 60:
            reasoning.append("Abnormal posting patterns identified for this profile.")
        if not reasoning:
            reasoning.append("No immediate risk markers found.")

        return RiskScore(
            score=final_score,
            level=level,
            nlp_confidence=nlp_result["confidence"],
            image_confidence=img_result["confidence"],
            behavioral_score=float(behavioral_score),
            reasoning=reasoning
        )

ai_engine = AIEngine()
