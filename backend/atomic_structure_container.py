import re
from typing import Dict, Any
from atomic_structure_challenges import ATOMIC_STRUCTURE_CHALLENGES

class AtomicStructureContainer:
    """Manages atomic structure challenge execution"""
    
    def __init__(self):
        pass
        
    def execute_challenge(self, challenge_id: int, user_answer: str) -> Dict[str, Any]:
        """Execute an atomic structure challenge"""
        
        # Get challenge details
        challenge = next((c for c in ATOMIC_STRUCTURE_CHALLENGES if c["id"] == challenge_id), None)
        if not challenge:
            return {
                "success": False,
                "error": f"Challenge {challenge_id} not found"
            }
        
        try:
            # Process answer based on question type
            question_type = challenge.get("type", "multiple_choice")
            
            if question_type == "multiple_choice":
                return self._check_multiple_choice(challenge, user_answer)
            elif question_type == "fill_blank":
                return self._check_fill_blank(challenge, user_answer)
            elif question_type == "true_false":
                return self._check_true_false(challenge, user_answer)
            elif question_type == "matching":
                return self._check_matching(challenge, user_answer)
            elif question_type == "short_answer":
                return self._check_short_answer(challenge, user_answer)
            else:
                return {
                    "success": False,
                    "error": f"Unknown question type: {question_type}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _check_multiple_choice(self, challenge: Dict[str, Any], user_answer: str) -> Dict[str, Any]:
        """Check multiple choice answer"""
        correct_index = challenge["correct_answer"]
        
        # Accept answer as letter (A, B, C, D) or number (0, 1, 2, 3)
        user_answer = user_answer.strip().upper()
        
        if user_answer in ['A', 'B', 'C', 'D']:
            user_index = ord(user_answer) - ord('A')
        elif user_answer.isdigit():
            user_index = int(user_answer)
        else:
            return {
                "success": False,
                "error": "Please enter A, B, C, or D"
            }
        
        passed = user_index == correct_index
        
        return {
            "success": True,
            "passed": passed,
            "user_answer": user_answer,
            "correct_answer": chr(ord('A') + correct_index),
            "explanation": challenge["explanation"],
            "options": challenge["options"]
        }
    
    def _check_fill_blank(self, challenge: Dict[str, Any], user_answer: str) -> Dict[str, Any]:
        """Check fill-in-the-blank answer"""
        correct_answer = challenge["correct_answer"].lower().strip()
        user_answer = user_answer.lower().strip()
        
        # Check for exact match or close variations
        passed = (user_answer == correct_answer or 
                 user_answer in correct_answer or 
                 correct_answer in user_answer)
        
        return {
            "success": True,
            "passed": passed,
            "user_answer": user_answer,
            "correct_answer": challenge["correct_answer"],
            "explanation": challenge["explanation"]
        }
    
    def _check_true_false(self, challenge: Dict[str, Any], user_answer: str) -> Dict[str, Any]:
        """Check true/false answer"""
        correct_answer = challenge["correct_answer"]
        user_answer = user_answer.strip().lower()
        
        # Accept various forms of true/false
        if user_answer in ['true', 't', 'yes', '1']:
            user_bool = True
        elif user_answer in ['false', 'f', 'no', '0']:
            user_bool = False
        else:
            return {
                "success": False,
                "error": "Please enter True or False"
            }
        
        passed = user_bool == correct_answer
        
        return {
            "success": True,
            "passed": passed,
            "user_answer": "True" if user_bool else "False",
            "correct_answer": "True" if correct_answer else "False",
            "explanation": challenge["explanation"]
        }
    
    def _check_matching(self, challenge: Dict[str, Any], user_answer: str) -> Dict[str, Any]:
        """Check matching answer"""
        correct_answer = challenge["correct_answer"].lower().replace(" ", "")
        user_answer = user_answer.lower().replace(" ", "")
        
        passed = user_answer == correct_answer
        
        return {
            "success": True,
            "passed": passed,
            "user_answer": user_answer,
            "correct_answer": challenge["correct_answer"],
            "explanation": challenge["explanation"]
        }
    
    def _check_short_answer(self, challenge: Dict[str, Any], user_answer: str) -> Dict[str, Any]:
        """Check short answer using keyword matching"""
        expected_keywords = challenge["expected_output"]
        user_answer_lower = user_answer.lower()
        
        # Count how many expected keywords/concepts are present
        keywords_found = []
        for keyword in expected_keywords:
            if keyword.lower() in user_answer_lower:
                keywords_found.append(keyword)
        
        # Pass if at least 50% of key concepts are mentioned
        min_keywords = max(1, len(expected_keywords) // 2)
        passed = len(keywords_found) >= min_keywords
        
        return {
            "success": True,
            "passed": passed,
            "user_answer": user_answer,
            "correct_answer": challenge["correct_answer"],
            "explanation": challenge["explanation"],
            "keywords_found": keywords_found,
            "keywords_expected": expected_keywords,
            "score": f"{len(keywords_found)}/{len(expected_keywords)} key concepts mentioned"
        }

class AtomicStructureChallengeManager:
    """Manages atomic structure challenge execution and validation"""
    
    def __init__(self):
        self.container = AtomicStructureContainer()
    
    def execute_challenge(self, challenge_id: int, user_id: str, user_answer: str) -> Dict[str, Any]:
        """Execute an atomic structure challenge with user answer"""
        
        try:
            # Execute the challenge
            result = self.container.execute_challenge(challenge_id, user_answer)
            
            # Add standard format expected by the main system
            if result["success"] and "passed" in result:
                # Format result to match expected structure
                formatted_result = {
                    "success": True,
                    "passed": result["passed"],
                    "results": [[result.get("user_answer", "")]],
                    "columns": ["Your Answer"],
                    "explanation": result.get("explanation", ""),
                    "correct_answer": result.get("correct_answer", ""),
                    "question_type": self._get_question_type(challenge_id)
                }
                
                # Add additional info for specific question types
                if "options" in result:
                    formatted_result["options"] = result["options"]
                if "keywords_found" in result:
                    formatted_result["keywords_found"] = result["keywords_found"]
                    formatted_result["score"] = result["score"]
                
                return formatted_result
            else:
                return result
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Challenge execution failed: {str(e)}"
            }
    
    def _get_question_type(self, challenge_id: int) -> str:
        """Get the question type for a challenge"""
        challenge = next((c for c in ATOMIC_STRUCTURE_CHALLENGES if c["id"] == challenge_id), None)
        return challenge.get("type", "multiple_choice") if challenge else "unknown"

# Global atomic structure challenge manager instance
atomic_structure_challenge_manager = AtomicStructureChallengeManager() 