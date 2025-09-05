"""
Servicio de LLM con LangChain
Soporte para Groq y OpenAI
"""

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from typing import List, Dict, Any, Optional
import structlog
from app.core.config import settings

logger = structlog.get_logger()

class LLMService:
    """Servicio para interactuar con LLMs usando LangChain"""
    
    def __init__(self, provider: str = None):
        self.provider = provider or settings.DEFAULT_LLM_PROVIDER
        self.llm = self._initialize_llm()
        
    def _initialize_llm(self):
        """Inicializar el LLM según el proveedor"""
        if self.provider == "groq":
            if not settings.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY no está configurada")
            return ChatGroq(
                groq_api_key=settings.GROQ_API_KEY,
                model_name=settings.GROQ_MODEL,
                temperature=0.7,
                max_tokens=1024
            )
        elif self.provider == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY no está configurada")
            return ChatOpenAI(
                openai_api_key=settings.OPENAI_API_KEY,
                model_name=settings.OPENAI_MODEL,
                temperature=0.7,
                max_tokens=1024
            )
        else:
            raise ValueError(f"Proveedor de LLM no soportado: {self.provider}")
    
    def generate_business_analyst_response(
        self, 
        user_message: str, 
        brief_data: Dict[str, Any], 
        current_step: str,
        current_question_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generar respuesta del Business Analyst
        """
        try:
            # Crear prompt del sistema
            system_prompt = self._create_system_prompt()
            
            # Crear prompt del usuario
            user_prompt = self._create_user_prompt(
                user_message, brief_data, current_step, current_question_key
            )
            
            # Generar respuesta
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            response = self.llm.invoke(messages)
            content = response.content
            
            # Procesar respuesta
            return self._process_response(content, current_step, current_question_key)
            
        except Exception as e:
            logger.error("Error generando respuesta del LLM", error=str(e))
            return {
                "message": "Lo siento, hubo un error procesando tu mensaje. Por favor, intenta de nuevo.",
                "step": current_step,
                "current_key": current_question_key
            }
    
    def _create_system_prompt(self) -> str:
        """Crear prompt del sistema para el Business Analyst"""
        return """Eres un Business Analyst experto que ayuda a clientes a estructurar sus proyectos de desarrollo de software.

Tu objetivo es:
1. Hacer preguntas específicas para entender el proyecto del cliente
2. Recopilar información sobre objetivos, audiencia, funcionalidades, etc.
3. Generar un resumen claro del proyecto
4. Proporcionar sugerencias de alto nivel (sin tecnicismos)

Preguntas clave que debes hacer:
- Objetivo principal del proyecto
- Público objetivo
- Funcionalidades principales (2-3)
- Fuentes de datos existentes
- Integraciones necesarias
- Rango de presupuesto
- Timeline deseado

Mantén un tono profesional pero amigable. Evita tecnicismos y enfócate en el valor de negocio."""
    
    def _create_user_prompt(
        self, 
        user_message: str, 
        brief_data: Dict[str, Any], 
        current_step: str,
        current_question_key: Optional[str]
    ) -> str:
        """Crear prompt del usuario"""
        prompt = f"Usuario dice: {user_message}\n\n"
        
        if current_step == "intro":
            prompt += "Es el inicio de la conversación. Saluda y explica que harás algunas preguntas para entender su proyecto."
        elif current_step == "asking":
            prompt += f"Estás en la fase de preguntas. Pregunta clave actual: {current_question_key}\n"
            prompt += f"Datos recopilados hasta ahora: {brief_data}\n"
            prompt += "Haz la siguiente pregunta de manera natural y conversacional."
        elif current_step == "done":
            prompt += f"La conversación ha terminado. Datos finales: {brief_data}\n"
            prompt += "Genera un resumen del proyecto y sugerencias de alto nivel."
        
        return prompt
    
    def _process_response(
        self, 
        content: str, 
        current_step: str, 
        current_question_key: Optional[str]
    ) -> Dict[str, Any]:
        """Procesar la respuesta del LLM"""
        response = {
            "message": content,
            "step": current_step,
            "current_key": current_question_key
        }
        
        # Si estamos en la fase de preguntas, determinar la siguiente pregunta
        if current_step == "asking":
            response["step"] = "asking"
            # Aquí podrías agregar lógica para determinar la siguiente pregunta
            # basada en el contenido de la respuesta
        
        # Si hemos terminado de recopilar información
        elif current_step == "done":
            response["step"] = "done"
            response["suggestions"] = self._generate_suggestions()
            response["summary"] = "Resumen del proyecto generado exitosamente"
        
        return response
    
    def _generate_suggestions(self) -> List[str]:
        """Generar sugerencias de alto nivel"""
        return [
            "1) MVP informativo + captura de leads: sitio web con secciones clave, formulario y analítica; ideal para validar el proyecto con baja inversión.",
            "2) MVP con flujo crítico: implementa 1–2 casos de uso principales con backend sencillo y métricas; útil para probar valor real con usuarios.",
            "3) Base de datos + API escalable: prepara una API y modelo de datos que soporten crecimiento; integra 1–2 sistemas externos prioritarios."
        ]
    
    def generate_summary(self, brief_data: Dict[str, Any]) -> str:
        """Generar resumen del brief"""
        summary_parts = []
        
        if brief_data.get("business_goal"):
            summary_parts.append(f"• Objetivo: {brief_data['business_goal']}")
        if brief_data.get("audience"):
            summary_parts.append(f"• Audiencia: {brief_data['audience']}")
        if brief_data.get("use_cases"):
            use_cases = ", ".join(brief_data["use_cases"]) if isinstance(brief_data["use_cases"], list) else brief_data["use_cases"]
            summary_parts.append(f"• Funcionalidades: {use_cases}")
        if brief_data.get("data_sources"):
            data_sources = ", ".join(brief_data["data_sources"]) if isinstance(brief_data["data_sources"], list) else brief_data["data_sources"]
            summary_parts.append(f"• Datos: {data_sources}")
        if brief_data.get("integrations"):
            integrations = ", ".join(brief_data["integrations"]) if isinstance(brief_data["integrations"], list) else brief_data["integrations"]
            summary_parts.append(f"• Integraciones: {integrations}")
        if brief_data.get("budget_range"):
            summary_parts.append(f"• Presupuesto: {brief_data['budget_range']}")
        if brief_data.get("timeline"):
            summary_parts.append(f"• Plazo: {brief_data['timeline']}")
        
        return "Resumen preliminar:\n" + "\n".join(summary_parts)
