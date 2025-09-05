"""
Servicio de Chat para Business Analyst
Maneja la lógica de conversación y flujo de preguntas
"""

from typing import Dict, Any, Optional, List
import structlog
from app.services.llm_service import LLMService
from app.core.config import settings

logger = structlog.get_logger()

class ChatService:
    """Servicio para manejar la lógica del chat Business Analyst"""
    
    def __init__(self):
        self.llm_service = LLMService()
        self.questions = [
            {"key": "business_goal", "text": "¿Cuál es el objetivo principal de tu proyecto?"},
            {"key": "audience", "text": "¿Quién es tu público objetivo?"},
            {"key": "use_cases", "text": "Menciona 2–3 funcionalidades clave que imaginas (separa por coma)."},
            {"key": "data_sources", "text": "¿Qué datos o fuentes existen hoy? (CRM, planillas, APIs, etc.)"},
            {"key": "integrations", "text": "¿Con qué sistemas debería integrarse? (ERP, pasarelas de pago, etc.)"},
            {"key": "budget_range", "text": "¿Cuál es tu rango de presupuesto? (<10k, 10–30k, 30–80k, 80k+)"},
            {"key": "timeline", "text": "¿Plazo deseado o fecha objetivo para una primera versión?"}
        ]
    
    def process_message(
        self, 
        user_message: str, 
        brief_data: Dict[str, Any], 
        current_step: str,
        current_question_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Procesar mensaje del usuario y generar respuesta
        """
        try:
            logger.info("Procesando mensaje", 
                       user_message=user_message[:50], 
                       current_step=current_step,
                       current_question_key=current_question_key)
            
            # Si es el inicio, comenzar con saludo
            if current_step == "intro":
                return self._handle_intro()
            
            # Si estamos en fase de preguntas
            elif current_step == "asking":
                return self._handle_question_phase(user_message, brief_data, current_question_key)
            
            # Si ya terminamos
            elif current_step == "done":
                return self._handle_done_phase(user_message, brief_data)
            
            else:
                return self._handle_unknown_step(user_message)
                
        except Exception as e:
            logger.error("Error procesando mensaje", error=str(e))
            return {
                "message": "Lo siento, hubo un error procesando tu mensaje. Por favor, intenta de nuevo.",
                "step": current_step,
                "current_key": current_question_key
            }
    
    def _handle_intro(self) -> Dict[str, Any]:
        """Manejar fase de introducción"""
        intro_message = (
            "¡Hola! Soy tu Business Analyst virtual. 👋\n\n"
            "Te haré algunas preguntas (5–7) para entender tu proyecto y poder "
            "estructurar un brief completo. Luego te daré sugerencias de alto nivel "
            "y podrás agendar una llamada con el equipo.\n\n"
            "¿Estás listo para comenzar?"
        )
        
        return {
            "message": intro_message,
            "step": "asking",
            "current_key": "business_goal"
        }
    
    def _handle_question_phase(
        self, 
        user_message: str, 
        brief_data: Dict[str, Any], 
        current_question_key: Optional[str]
    ) -> Dict[str, Any]:
        """Manejar fase de preguntas"""
        
        # Si tenemos una pregunta actual, procesar la respuesta
        if current_question_key:
            # Actualizar brief con la respuesta
            brief_data[current_question_key] = self._parse_answer(current_question_key, user_message)
            logger.info("Respuesta procesada", 
                       question=current_question_key, 
                       answer=user_message[:50])
        
        # Buscar siguiente pregunta
        next_question = self._get_next_question(brief_data)
        
        if next_question:
            # Hay más preguntas
            return {
                "message": next_question["text"],
                "step": "asking",
                "current_key": next_question["key"]
            }
        else:
            # No hay más preguntas, generar resumen
            return self._generate_summary(brief_data)
    
    def _handle_done_phase(self, user_message: str, brief_data: Dict[str, Any]) -> Dict[str, Any]:
        """Manejar fase final"""
        if "reiniciar" in user_message.lower() or "empezar" in user_message.lower():
            return self._handle_intro()
        else:
            return {
                "message": (
                    "Ya hemos terminado la recopilación de información. "
                    "¿Te gustaría reiniciar la conversación o agendar una llamada?"
                ),
                "step": "done"
            }
    
    def _handle_unknown_step(self, user_message: str) -> Dict[str, Any]:
        """Manejar paso desconocido"""
        return {
            "message": "Parece que hubo un problema con el flujo de la conversación. Vamos a empezar de nuevo.",
            "step": "intro"
        }
    
    def _parse_answer(self, question_key: str, answer: str) -> Any:
        """Parsear respuesta del usuario según el tipo de pregunta"""
        array_keys = ["use_cases", "data_sources", "integrations", "constraints"]
        
        if question_key in array_keys:
            # Para preguntas que esperan listas
            return [item.strip() for item in answer.split(",") if item.strip()]
        else:
            # Para preguntas de texto simple
            return answer.strip()
    
    def _get_next_question(self, brief_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Obtener siguiente pregunta no respondida"""
        for question in self.questions:
            if not brief_data.get(question["key"]):
                return question
        return None
    
    def _generate_summary(self, brief_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generar resumen final y sugerencias"""
        try:
            # Generar resumen usando LLM
            summary_prompt = self._create_summary_prompt(brief_data)
            suggestions_prompt = self._create_suggestions_prompt(brief_data)
            
            # Generar resumen
            summary_response = self.llm_service.llm.invoke([
                {"role": "user", "content": summary_prompt}
            ])
            summary = summary_response.content
            
            # Generar sugerencias
            suggestions_response = self.llm_service.llm.invoke([
                {"role": "user", "content": suggestions_prompt}
            ])
            suggestions_text = suggestions_response.content
            
            # Formatear sugerencias
            suggestions = self._format_suggestions(suggestions_text)
            
            final_message = (
                f"¡Excelente! Hemos recopilado toda la información necesaria. "
                f"Aquí está el resumen de tu proyecto:\n\n"
                f"{summary}\n\n"
                f"**Sugerencias de alto nivel:**\n"
                f"{suggestions}\n\n"
                f"¿Te gustaría agendar una llamada para revisar estos detalles "
                f"y discutir los siguientes pasos?"
            )
            
            return {
                "message": final_message,
                "step": "done",
                "summary": summary,
                "suggestions": suggestions
            }
            
        except Exception as e:
            logger.error("Error generando resumen", error=str(e))
            # Fallback a resumen simple
            return self._generate_simple_summary(brief_data)
    
    def _create_summary_prompt(self, brief_data: Dict[str, Any]) -> str:
        """Crear prompt para generar resumen"""
        return f"""
        Genera un resumen profesional y conciso del siguiente proyecto basado en la información recopilada:
        
        Objetivo: {brief_data.get('business_goal', 'No especificado')}
        Audiencia: {brief_data.get('audience', 'No especificado')}
        Funcionalidades: {', '.join(brief_data.get('use_cases', []))}
        Fuentes de datos: {', '.join(brief_data.get('data_sources', []))}
        Integraciones: {', '.join(brief_data.get('integrations', []))}
        Presupuesto: {brief_data.get('budget_range', 'No especificado')}
        Timeline: {brief_data.get('timeline', 'No especificado')}
        
        El resumen debe ser claro, profesional y enfocado en el valor de negocio.
        """
    
    def _create_suggestions_prompt(self, brief_data: Dict[str, Any]) -> str:
        """Crear prompt para generar sugerencias"""
        goal = brief_data.get('business_goal', 'el proyecto')
        budget = brief_data.get('budget_range', 'no especificado')
        
        return f"""
        Basándote en el proyecto con objetivo "{goal}" y presupuesto "{budget}", 
        genera 3 sugerencias de alto nivel para el desarrollo. 
        
        Cada sugerencia debe incluir:
        1. Un título descriptivo
        2. Una descripción breve del enfoque
        3. Por qué es adecuado para este proyecto
        
        Formato la respuesta como una lista numerada clara y concisa.
        """
    
    def _format_suggestions(self, suggestions_text: str) -> str:
        """Formatear sugerencias para mostrar"""
        # Limpiar y formatear el texto de sugerencias
        lines = suggestions_text.strip().split('\n')
        formatted = []
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith(('1.', '2.', '3.', '•', '-')) or line.startswith(('1)', '2)', '3)'))):
                formatted.append(line)
            elif line and not line.startswith('**'):
                formatted.append(f"• {line}")
        
        return '\n'.join(formatted) if formatted else suggestions_text
    
    def _generate_simple_summary(self, brief_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generar resumen simple sin LLM"""
        summary_parts = []
        
        if brief_data.get("business_goal"):
            summary_parts.append(f"• **Objetivo**: {brief_data['business_goal']}")
        if brief_data.get("audience"):
            summary_parts.append(f"• **Audiencia**: {brief_data['audience']}")
        if brief_data.get("use_cases"):
            use_cases = ', '.join(brief_data["use_cases"]) if isinstance(brief_data["use_cases"], list) else brief_data["use_cases"]
            summary_parts.append(f"• **Funcionalidades**: {use_cases}")
        if brief_data.get("budget_range"):
            summary_parts.append(f"• **Presupuesto**: {brief_data['budget_range']}")
        if brief_data.get("timeline"):
            summary_parts.append(f"• **Timeline**: {brief_data['timeline']}")
        
        summary = "**Resumen del Proyecto:**\n" + "\n".join(summary_parts)
        
        suggestions = [
            "1. **MVP Básico**: Implementar funcionalidades core con diseño simple y funcional",
            "2. **MVP Avanzado**: Desarrollar con integraciones y características avanzadas",
            "3. **Solución Completa**: Arquitectura escalable con todas las funcionalidades"
        ]
        
        final_message = (
            f"¡Excelente! Hemos recopilado toda la información necesaria.\n\n"
            f"{summary}\n\n"
            f"**Sugerencias de alto nivel:**\n"
            f"{chr(10).join(suggestions)}\n\n"
            f"¿Te gustaría agendar una llamada para revisar estos detalles?"
        )
        
        return {
            "message": final_message,
            "step": "done",
            "summary": summary,
            "suggestions": suggestions
        }
