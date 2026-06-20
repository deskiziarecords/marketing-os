"""
Seed script: crear los 90 temas de contenido laboral como ContentMasters.

Usage:
    uv run python scripts/seed_contenido_laboral.py
"""
import os
import sys

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from django.db import transaction

from apps.tenants.models import Tenant, Project
from domains.content_factory.models import ContentMaster


# ---------------------------------------------------------------------------
# 90 TEMAS organizados por categoria (del plan original del usuario)
# ---------------------------------------------------------------------------
CONTENT_TOPICS = [
    # ==================================================================
    # DESPIDOS (20)
    # ==================================================================
    {
        "category": "Despidos",
        "title": "Que hacer el mismo dia que te despiden",
        "content": "Guia paso a paso de acciones a tomar inmediatamente despues de un despido. Incluye: no firmar nada, reunir documentos, identificar tipo de despido, buscar asesoria legal. Contenido educativo para personas que acaban de ser despedidas.",
        "status": "approved",
    },
    {
        "category": "Despidos",
        "title": "Despido injustificado: senales mas comunes",
        "content": "Identifica las senales de un despido injustificado. Causales que el patron no puede usar legalmente. Diferencias entre despido justificado e injustificado. Derechos del trabajador ante un despido sin causa.",
        "status": "approved",
    },
    {
        "category": "Despidos",
        "title": "Me pueden despedir por faltar un dia",
        "content": "Analisis de las causales de despido por inasistencias. Cuantas faltas se necesitan para un despido justificado. Diferencias entre falta justificada e injustificada. Que hacer si te despiden por una sola falta.",
        "status": "draft",
    },
    {
        "category": "Despidos",
        "title": "Que pasa si me despiden por WhatsApp",
        "content": "Validez legal de un despido por mensaje de texto o WhatsApp. Como probar el despido. Que documentos generar. Derechos del trabajador cuando el despido es informal.",
        "status": "draft",
    },
    {
        "category": "Despidos",
        "title": "Despido durante incapacidad medica",
        "content": "Proteccion legal del trabajador durante una incapacidad. Que hacer si te despiden estando incapacitado. Derecho a salarios caidos y reinstalacion. Indemnizacion agravada.",
        "status": "approved",
    },
    {
        "category": "Despidos",
        "title": "Despido durante embarazo",
        "content": "Proteccion especial a trabajadoras embarazadas. Despido por embarazo como acto discriminatorio. Indemnizacion de 3 meses de salario mas danos morales. Que hacer si te despiden embarazada.",
        "status": "approved",
    },
    {
        "category": "Despidos",
        "title": "Es legal un despido verbal",
        "content": "Validez del despido verbal vs escrito. Como probar un despido verbal. Testigos, audios, mensajes como evidencia. Que derechos tiene el trabajador.",
        "status": "draft",
    },
    {
        "category": "Despidos",
        "title": "Debo firmar la renuncia que me presentan",
        "content": "Por que muchos patrones piden renuncia. Consecuencias de firmar una renuncia. Diferencia entre renuncia y despido. Que hacer si te presionan para firmar.",
        "status": "approved",
    },
    {
        "category": "Despidos",
        "title": "Diferencia entre despido y renuncia",
        "content": "Cuadro comparativo entre despido y renuncia. Implicaciones legales y economicas de cada uno. Derechos del trabajador en ambos escenarios. Ejemplos practicos.",
        "status": "draft",
    },
    {
        "category": "Despidos",
        "title": "Documentos que debes conservar tras un despido",
        "content": "Lista completa de documentos a guardar: contrato, recibos de nomina, comprobantes de prestaciones, comunicaciones con el patron, testigos. Guia de organizacion documental.",
        "status": "approved",
    },
    {
        "category": "Despidos",
        "title": "Que es la indemnizacion constitucional",
        "content": "Explicacion de la indemnizacion de 3 meses de salario del articulo 123 constitucional. Cuando aplica. Como se calcula. Ejemplos con montos reales.",
        "status": "draft",
    },
    {
        "category": "Despidos",
        "title": "Cuanto tiempo tengo para reclamar",
        "content": "Plazos legales para reclamar un despido injustificado. Prescripcion de acciones laborales. Que pasa si deja pasar el tiempo. Urgencia de actuar rapido.",
        "status": "draft",
    },
    {
        "category": "Despidos",
        "title": "Despido por reduccion de personal",
        "content": "Procedencia del despido por reduccion de personal. Requisitos legales. Derechos del trabajador. Indemnizacion y finiquito. Diferencias con despido injustificado.",
        "status": "draft",
    },
    {
        "category": "Despidos",
        "title": "Despido despues de muchos anos de servicio",
        "content": "Derechos especiales de trabajadores con antiguedad. Prima de antiguedad. Indemnizacion incrementada. Jubilacion anticipada. Casos de trabajadores con mas de 15 anos.",
        "status": "draft",
    },
    {
        "category": "Despidos",
        "title": "Me pueden despedir estando de vacaciones",
        "content": "Proteccion del trabajador durante periodo vacacional. Validez del despido en vacaciones. Derechos especificos. Que hacer.",
        "status": "draft",
    },
    {
        "category": "Despidos",
        "title": "Que hacer si te niegan la liquidacion",
        "content": "Pasos a seguir cuando el patron se niega a pagar la liquidacion. Conciliacion. Demanda laboral. Sanciones al patron. Garantia de pago.",
        "status": "approved",
    },
    {
        "category": "Despidos",
        "title": "Errores comunes despues de un despido",
        "content": "Los 10 errores mas frecuentes que cometen los trabajadores tras ser despedidos. Como evitarlos. Consejos practicos de abogados laborales.",
        "status": "draft",
    },
    {
        "category": "Despidos",
        "title": "Despido por bajo rendimiento",
        "content": "Procedencia legal del despido por bajo rendimiento. Como debe probarlo el patron. Derechos del trabajador. Diferencias con despido injustificado.",
        "status": "draft",
    },
    {
        "category": "Despidos",
        "title": "Despido por conflictos con supervisores",
        "content": "Analisis de despidos originados por conflictos laborales. Acoso vs diferencia de opiniones. Derechos del trabajador. Como documentar el conflicto.",
        "status": "draft",
    },
    {
        "category": "Despidos",
        "title": "Mitos sobre el despido laboral",
        "content": "Los 15 mitos mas comunes sobre despidos laborales. Cada mito explicado y desmentido con base legal. Informacion util para trabajadores.",
        "status": "approved",
    },
    # ==================================================================
    # LIQUIDACIONES Y FINIQUITOS (15)
    # ==================================================================
    {
        "category": "Liquidaciones y Finiquitos",
        "title": "Diferencia entre finiquito y liquidacion",
        "content": "Explicacion clara de las diferencias legales y practicas entre finiquito y liquidacion. Cuando corresponde cada uno. Ejemplos de calculo.",
        "status": "approved",
    },
    {
        "category": "Liquidaciones y Finiquitos",
        "title": "Como saber si tu liquidacion esta correcta",
        "content": "Guia paso a paso para revisar y verificar el calculo de tu liquidacion. Partes que debe incluir. Errores comunes. Cuando buscar ayuda profesional.",
        "status": "approved",
    },
    {
        "category": "Liquidaciones y Finiquitos",
        "title": "Aguinaldo proporcional",
        "content": "Calculo del aguinaldo proporcional en liquidaciones. Derecho legal. Ejemplos con fechas y montos. Incluye calculadora explicada.",
        "status": "draft",
    },
    {
        "category": "Liquidaciones y Finiquitos",
        "title": "Vacaciones pendientes",
        "content": "Derecho al pago de vacaciones no disfrutadas en la liquidacion. Como se calculan. Prima vacacional. Ejemplos practicos.",
        "status": "draft",
    },
    {
        "category": "Liquidaciones y Finiquitos",
        "title": "Prima vacacional",
        "content": "Explicacion de la prima vacacional. Porcentaje legal. Como se integra en la liquidacion. Calculo paso a paso.",
        "status": "draft",
    },
    {
        "category": "Liquidaciones y Finiquitos",
        "title": "Prima de antiguedad",
        "content": "Derecho a prima de antiguedad. Requisitos. Calculo. Ejemplos con diferentes antiguedades. Diferencia con otras prestaciones.",
        "status": "draft",
    },
    {
        "category": "Liquidaciones y Finiquitos",
        "title": "Prestaciones que muchas personas olvidan reclamar",
        "content": "Lista de prestaciones que frecuentemente se omiten en liquidaciones. Revision de cada una. Como asegurarse de recibirlas todas.",
        "status": "approved",
    },
    {
        "category": "Liquidaciones y Finiquitos",
        "title": "Que hacer si te ofrecen menos dinero",
        "content": "Pasos a seguir cuando el patron ofrece una liquidacion menor a la legal. Negociacion. Conciliacion. Demanda. Tiempos y riesgos.",
        "status": "draft",
    },
    {
        "category": "Liquidaciones y Finiquitos",
        "title": "Liquidacion en contratos temporales",
        "content": "Particularidades de la liquidacion en contratos por tiempo determinado. Derechos especificos. Diferencias con contratos indefinidos.",
        "status": "draft",
    },
    {
        "category": "Liquidaciones y Finiquitos",
        "title": "Liquidacion por cierre de empresa",
        "content": "Derechos del trabajador cuando la empresa cierra. Orden de pago de creditos laborales. Fondo de garantia. Que hacer.",
        "status": "draft",
    },
    {
        "category": "Liquidaciones y Finiquitos",
        "title": "Liquidacion durante incapacidad",
        "content": "Como se maneja la liquidacion cuando el trabajador esta incapacitado. Derechos laborales. Prestaciones del IMSS. Recomendaciones.",
        "status": "draft",
    },
    {
        "category": "Liquidaciones y Finiquitos",
        "title": "Pagos en parcialidades: riesgos",
        "content": "Riesgos de aceptar pagos fraccionados de liquidacion. Que dice la ley. Proteccion del trabajador. Recomendaciones.",
        "status": "draft",
    },
    {
        "category": "Liquidaciones y Finiquitos",
        "title": "Debo firmar un convenio",
        "content": "Implicaciones de firmar un convenio de terminacion laboral. Ventajas y desventajas. Cuando conviene. Cuando no. Asesoria legal.",
        "status": "draft",
    },
    {
        "category": "Liquidaciones y Finiquitos",
        "title": "Como revisar un calculo laboral",
        "content": "Guia practica para entender y verificar un calculo de liquidacion. Formulas. Ejemplos. Checklist de verificacion.",
        "status": "draft",
    },
    {
        "category": "Liquidaciones y Finiquitos",
        "title": "Casos donde si existe derecho a liquidacion",
        "content": "Escenarios concretos donde el trabajador tiene derecho a liquidacion completa. Ejemplos de casos reales. Diferencias con finiquito simple.",
        "status": "approved",
    },
    # ==================================================================
    # SALARIOS Y PAGOS (10)
    # ==================================================================
    {
        "category": "Salarios y Pagos",
        "title": "Retraso en el pago del salario",
        "content": "Que hacer cuando el patron retrasa el pago de nomina. Derechos del trabajador. Intereses moratorios. Denuncia ante STPS.",
        "status": "approved",
    },
    {
        "category": "Salarios y Pagos",
        "title": "Falta de pago de horas extras",
        "content": "Derecho al pago de horas extras. Como se calculan. Limites legales. Que hacer si no te las pagan. Pruebas necesarias.",
        "status": "approved",
    },
    {
        "category": "Salarios y Pagos",
        "title": "Descuentos indebidos en nomina",
        "content": "Tipos de descuentos permitidos y prohibidos por ley. Que hacer si te hacen descuentos ilegales. Reclamo y recuperacion.",
        "status": "draft",
    },
    {
        "category": "Salarios y Pagos",
        "title": "Que hacer si te pagan menos de lo acordado",
        "content": "Pasos a seguir cuando el salario pagado es menor al contratado. Diferencia salarial. Reclamo. Pruebas. Plazos.",
        "status": "draft",
    },
    {
        "category": "Salarios y Pagos",
        "title": "Trabajo realizado sin pago",
        "content": "Derecho al pago de trabajo realizado y no remunerado. Como probarlo. Que prestaciones aplicar. Acciones legales.",
        "status": "draft",
    },
    {
        "category": "Salarios y Pagos",
        "title": "Comisiones no pagadas",
        "content": "Derecho al pago de comisiones laborales. Como se demuestran. Que hacer si no las pagan. Diferencia con bonos.",
        "status": "draft",
    },
    {
        "category": "Salarios y Pagos",
        "title": "Bonos retenidos",
        "content": "Bonos y prestaciones que el patron puede retener. Legalidad de la retencion. Como reclamar su pago.",
        "status": "draft",
    },
    {
        "category": "Salarios y Pagos",
        "title": "Problemas con depositos bancarios",
        "content": "Que hacer cuando el patron deposita mal el salario. Errores bancarios. Responsabilidad del patron. Soluciones.",
        "status": "draft",
    },
    {
        "category": "Salarios y Pagos",
        "title": "Que evidencia sirve para reclamar salarios",
        "content": "Tipos de prueba valida para reclamar salarios impagos. Recibos, estados de cuenta, testigos, comunicaciones. Como organizar la evidencia.",
        "status": "draft",
    },
    {
        "category": "Salarios y Pagos",
        "title": "Derechos cuando la empresa deja de pagar",
        "content": "Que opciones tiene el trabajador cuando la empresa simplemente deja de pagar. Rescision de relacion laboral. Demanda. Indemnizacion.",
        "status": "approved",
    },
    # ==================================================================
    # ACOSO Y AMBIENTE LABORAL (10)
    # ==================================================================
    {
        "category": "Acoso y Ambiente Laboral",
        "title": "Que es el acoso laboral",
        "content": "Definicion legal del acoso laboral en Mexico. Tipos de acoso. Diferencias con mal ambiente laboral. Derechos del trabajador.",
        "status": "approved",
    },
    {
        "category": "Acoso y Ambiente Laboral",
        "title": "Diferencia entre acoso y exigencia laboral",
        "content": "Limites entre la exigencia laboral legitima y el acoso. Indicadores de cada uno. Ejemplos practicos. Cuando buscar ayuda.",
        "status": "draft",
    },
    {
        "category": "Acoso y Ambiente Laboral",
        "title": "Hostigamiento por parte de supervisores",
        "content": "El hostigamiento laboral como figura legal. Conductas tipicas. Responsabilidad del patron. Derechos del trabajador. Denuncia.",
        "status": "draft",
    },
    {
        "category": "Acoso y Ambiente Laboral",
        "title": "Acoso psicologico en el trabajo",
        "content": "El mobbing o acoso psicologico. Senales de alerta. Efectos en la salud. Que hacer. Proteccion legal.",
        "status": "draft",
    },
    {
        "category": "Acoso y Ambiente Laboral",
        "title": "Discriminacion laboral",
        "content": "Tipos de discriminacion en el trabajo. Proteccion legal. Que hacer si sufres discriminacion. Indemnizacion por dano moral.",
        "status": "approved",
    },
    {
        "category": "Acoso y Ambiente Laboral",
        "title": "Acoso por embarazo",
        "content": "Proteccion especial a trabajadoras embarazadas contra acoso. Derechos. Denuncia. Indemnizacion agravada.",
        "status": "approved",
    },
    {
        "category": "Acoso y Ambiente Laboral",
        "title": "Acoso por edad",
        "content": "Discriminacion y acoso por edad en el trabajo. Proteccion legal de trabajadores mayores. Derechos. Como reclamar.",
        "status": "draft",
    },
    {
        "category": "Acoso y Ambiente Laboral",
        "title": "Acoso por discapacidad",
        "content": "Derechos de trabajadores con discapacidad. Prohibicion de discriminacion. Ajustes razonables. Que hacer ante acoso.",
        "status": "draft",
    },
    {
        "category": "Acoso y Ambiente Laboral",
        "title": "Que pruebas reunir ante un caso de acoso",
        "content": "Guia de documentacion para casos de acoso laboral. Tipos de prueba. Como obtenerlas sin arriesgar tu trabajo. Organizacion del caso.",
        "status": "approved",
    },
    {
        "category": "Acoso y Ambiente Laboral",
        "title": "Cuando buscar asesoria legal",
        "content": "Senales de alerta que indican que necesitas un abogado laboral. Momentos clave para buscar ayuda profesional. Costos y opciones.",
        "status": "draft",
    },
    # ==================================================================
    # PRESTACIONES LABORALES (10)
    # ==================================================================
    {
        "category": "Prestaciones Laborales",
        "title": "Derecho al aguinaldo",
        "content": "Todo sobre el aguinaldo: derecho legal, calculo, plazo de pago, sanciones por no pago. Ejemplos con montos.",
        "status": "approved",
    },
    {
        "category": "Prestaciones Laborales",
        "title": "Derecho a vacaciones",
        "content": "Derecho a vacaciones en Mexico. Dias minimos por ley. Incremento por antiguedad. Como se disfrutan. Pago de vacaciones no tomadas.",
        "status": "draft",
    },
    {
        "category": "Prestaciones Laborales",
        "title": "Prima vacacional explicada",
        "content": "Que es la prima vacacional. Porcentaje. Calculo. Ejemplos. Relacion con vacaciones y liquidacion.",
        "status": "draft",
    },
    {
        "category": "Prestaciones Laborales",
        "title": "Participacion de utilidades PTU",
        "content": "Derecho a PTU. Como se calcula. Plazos. Que hacer si no te pagan. Topes legales. Excepciones.",
        "status": "approved",
    },
    {
        "category": "Prestaciones Laborales",
        "title": "Prima de antiguedad",
        "content": "Explicacion detallada de la prima de antiguedad. Requisitos. Calculo. Ejemplos. Diferencia con otras prestaciones.",
        "status": "draft",
    },
    {
        "category": "Prestaciones Laborales",
        "title": "Licencias e incapacidades",
        "content": "Tipos de licencias laborales. Incapacidades del IMSS. Derechos durante incapacidad. Pago. Reincorporacion.",
        "status": "draft",
    },
    {
        "category": "Prestaciones Laborales",
        "title": "Descansos obligatorios",
        "content": "Dias de descanso obligatorio por ley. Descanso semanal. Dias festivos. Pago de dias trabajados en descanso.",
        "status": "draft",
    },
    {
        "category": "Prestaciones Laborales",
        "title": "Dias festivos y pago correspondiente",
        "content": "Lista de dias festivos oficiales. Como se pagan. Trabajo en dia festivo. Derechos del trabajador.",
        "status": "draft",
    },
    {
        "category": "Prestaciones Laborales",
        "title": "Prestaciones minimas por ley",
        "content": "Resumen de todas las prestaciones minimas que la ley mexicana exige. Checklist para trabajadores. Que no te pueden negar.",
        "status": "approved",
    },
    {
        "category": "Prestaciones Laborales",
        "title": "Prestaciones superiores a la ley",
        "content": "Prestaciones que algunas empresas ofrecen adicionales a la ley. Derechos adquiridos. No pueden quitarlas sin consentimiento.",
        "status": "draft",
    },
    # ==================================================================
    # CONTRATOS Y RELACION LABORAL (10)
    # ==================================================================
    {
        "category": "Contratos y Relacion Laboral",
        "title": "Que pasa si nunca firme contrato",
        "content": "Consecuencias de no tener contrato firmado. Existencia de relacion laboral. Como probarla. Derechos del trabajador.",
        "status": "approved",
    },
    {
        "category": "Contratos y Relacion Laboral",
        "title": "Contratos por tiempo determinado",
        "content": "Caracteristicas de los contratos temporales. Cuando son legales. Limites. Derechos del trabajador. Renovacion.",
        "status": "draft",
    },
    {
        "category": "Contratos y Relacion Laboral",
        "title": "Contratos por capacitacion",
        "content": "Contratos de capacitacion inicial. Requisitos. Duracion. Derechos. Transicion a contrato indefinido.",
        "status": "draft",
    },
    {
        "category": "Contratos y Relacion Laboral",
        "title": "Contratos de prueba",
        "content": "Periodo de prueba en la ley federal del trabajo. Duracion maxima. Derechos durante prueba. Terminacion.",
        "status": "draft",
    },
    {
        "category": "Contratos y Relacion Laboral",
        "title": "Trabajo sin recibos de nomina",
        "content": "Riesgos de trabajar sin recibos de nomina. Como probar la relacion laboral. Derechos. Denuncia ante STPS.",
        "status": "approved",
    },
    {
        "category": "Contratos y Relacion Laboral",
        "title": "Trabajo informal y derechos laborales",
        "content": "Derechos de trabajadores informales. Como regularizar la situacion. Riesgos. Opciones legales.",
        "status": "draft",
    },
    {
        "category": "Contratos y Relacion Laboral",
        "title": "Cambios unilaterales de horario",
        "content": "Derecho del trabajador ante cambios de horario no consentidos. Modificacion de condiciones laborales. Rescision. Indemnizacion.",
        "status": "draft",
    },
    {
        "category": "Contratos y Relacion Laboral",
        "title": "Cambios de puesto sin consentimiento",
        "content": "Cuando el patron puede cambiar tu puesto. Limites. Derechos del trabajador. Rescision de relacion laboral.",
        "status": "draft",
    },
    {
        "category": "Contratos y Relacion Laboral",
        "title": "Cambios de salario",
        "content": "Modificaciones salariales. Cuando son legales. Consentimiento del trabajador. Reduccion salarial. Derechos.",
        "status": "draft",
    },
    {
        "category": "Contratos y Relacion Laboral",
        "title": "Obligaciones del patron",
        "content": "Resumen de las principales obligaciones legales del patron. Checklist. Derechos del trabajador cuando no se cumplen.",
        "status": "approved",
    },
    # ==================================================================
    # CONCILIACION LABORAL (10)
    # ==================================================================
    {
        "category": "Conciliacion Laboral",
        "title": "Que es la conciliacion laboral",
        "content": "Explicacion del proceso de conciliacion laboral en Mexico. Etapas. Objetivo. Ventajas. Como prepararse.",
        "status": "approved",
    },
    {
        "category": "Conciliacion Laboral",
        "title": "Ventajas de conciliar",
        "content": "Beneficios de resolver conflictos laborales mediante conciliacion. Rapidez. Menor costo. Confidencialidad. Ejemplos de acuerdos exitosos.",
        "status": "approved",
    },
    {
        "category": "Conciliacion Laboral",
        "title": "Necesito abogado para conciliar",
        "content": "Importancia de la asesoria legal en conciliacion. Cuando es recomendable llevar abogado. Costos. Derechos del trabajador.",
        "status": "draft",
    },
    {
        "category": "Conciliacion Laboral",
        "title": "Que llevar a una audiencia",
        "content": "Lista completa de documentos y preparacion para una audiencia de conciliacion. Que esperar. Como vestir. Que decir.",
        "status": "approved",
    },
    {
        "category": "Conciliacion Laboral",
        "title": "Que sucede durante una audiencia",
        "content": "Descripcion paso a paso de una audiencia de conciliacion. Participantes. Tiempos. Posibles resultados. Preguntas frecuentes.",
        "status": "draft",
    },
    {
        "category": "Conciliacion Laboral",
        "title": "Que pasa si la empresa no se presenta",
        "content": "Consecuencias de la inasistencia del patron a conciliacion. Multas. Sanciones. Derechos del trabajador.",
        "status": "draft",
    },
    {
        "category": "Conciliacion Laboral",
        "title": "Convenios laborales",
        "content": "Que son los convenios laborales en conciliacion. Contenido minimo. Validez. Efectos. Cuando no conviene firmar.",
        "status": "draft",
    },
    {
        "category": "Conciliacion Laboral",
        "title": "Cuanto tarda un procedimiento",
        "content": "Tiempos estimados del proceso de conciliacion laboral. Etapas y duracion. Factores que afectan la duracion. Comparacion con juicio.",
        "status": "draft",
    },
    {
        "category": "Conciliacion Laboral",
        "title": "Casos que suelen resolverse mediante conciliacion",
        "content": "Tipos de conflictos laborales con alta probabilidad de resolucion en conciliacion. Ejemplos reales. Estadisticas.",
        "status": "draft",
    },
    {
        "category": "Conciliacion Laboral",
        "title": "Errores antes de una audiencia",
        "content": "Los errores mas comunes que cometen los trabajadores antes de una audiencia de conciliacion. Como evitarlos. Preparacion.",
        "status": "approved",
    },
    # ==================================================================
    # CASOS REALES Y EDUCATIVOS (5)
    # ==================================================================
    {
        "category": "Casos Reales",
        "title": "Caso real: despido injustificado",
        "content": "Historia real de un trabajador despedido injustamente. Proceso legal. Resultado. Lecciones aprendidas. Montos recuperados.",
        "status": "approved",
    },
    {
        "category": "Casos Reales",
        "title": "Caso real: falta de pago",
        "content": "Historia real de recuperacion de salarios impagos. Estrategia legal. Tiempos. Resultado. Consejos.",
        "status": "approved",
    },
    {
        "category": "Casos Reales",
        "title": "Caso real: convenio exitoso",
        "content": "Historia real de un convenio laboral alcanzado en conciliacion. Terminos del acuerdo. Beneficios para ambas partes.",
        "status": "draft",
    },
    {
        "category": "Casos Reales",
        "title": "Caso real: recuperacion de prestaciones",
        "content": "Historia real de recuperacion de prestaciones laborales no pagadas. Proceso. Documentacion clave. Resultado.",
        "status": "draft",
    },
    {
        "category": "Casos Reales",
        "title": "Preguntas frecuentes que recibimos cada semana",
        "content": "Compilacion de las preguntas mas frecuentes que recibe un despacho laboral. Respuestas claras y directas. Temas variados.",
        "status": "approved",
    },
]

# ==================================================================
# ANUNCIOS DE CONVERSION (BONUS - 20)
# ==================================================================
ADS = [
    {"title": "Te despidieron? Solicita asesoria gratuita", "content": "Anuncio de conversion para captacion de leads. Enfoque directo a personas que acaban de ser despedidas. CTA: Agenda tu consulta gratuita.", "status": "approved"},
    {"title": "No te pagaron lo que te deben?", "content": "Anuncio de conversion para reclamos salariales. Enfoque en recuperacion de salarios impagos. CTA: Primera revision sin costo.", "status": "approved"},
    {"title": "Te deben horas extras?", "content": "Anuncio de conversion para reclamo de horas extras no pagadas. CTA: Calculamos tu liquidacion sin compromiso.", "status": "approved"},
    {"title": "Te obligaron a firmar una renuncia?", "content": "Anuncio de conversion para casos de renuncia forzada. Enfoque en validez de la renuncia. CTA: Asesoria laboral gratuita.", "status": "approved"},
    {"title": "Tienes dudas sobre tu liquidacion?", "content": "Anuncio de conversion para revision de liquidaciones. CTA: Te ayudamos a verificar si tu liquidacion es correcta.", "status": "approved"},
    {"title": "Solicita una asesoria gratuita", "content": "Anuncio de conversion generico. CTA: Agenda tu cita de asesoria laboral sin costo. Primer paso para conocer tus derechos.", "status": "approved"},
    {"title": "Agenda una cita con nuestros abogados", "content": "Anuncio de conversion para agendar consulta. CTA: Habla con un abogado laboral experto. Primera consulta gratuita.", "status": "approved"},
    {"title": "Atencion en nuestras 3 oficinas", "content": "Anuncio de conversion con enfoque en ubicaciones. CTA: Visitanos en cualquiera de nuestras sucursales. Atencion personalizada.", "status": "approved"},
    {"title": "Primera revision de tu caso sin costo", "content": "Anuncio de conversion destacando el beneficio de revision gratuita. CTA: Que esperas? Conoce tus derechos laborales hoy.", "status": "approved"},
    {"title": "Conoce tus derechos laborales", "content": "Anuncio de conversion educativo. CTA: Muchos trabajadores desconocen sus derechos. Informate con una asesoria gratuita.", "status": "approved"},
    {"title": "Cuanto te deben de liquidacion?", "content": "Anuncio de conversion para calculo de liquidacion. CTA: Calculamos el monto exacto que te corresponde. Asesoria sin costo.", "status": "approved"},
    {"title": "Sufriste acoso laboral?", "content": "Anuncio de conversion para victimas de acoso. CTA: No estes solo. Te orientamos sobre los pasos a seguir.", "status": "approved"},
    {"title": "Te cambiaron el horario sin avisar?", "content": "Anuncio de conversion para modificaciones unilaterales. CTA: Eso no es legal. Asesorate con nosotros.", "status": "approved"},
    {"title": "Trabajas sin contrato?", "content": "Anuncio de conversion para trabajadores informales. CTA: Tienes derechos aunque no hayas firmado. Te explicamos como.", "status": "approved"},
    {"title": "No te pagaron utilidades?", "content": "Anuncio de conversion para PTU no pagada. CTA: La participacion de utilidades es tu derecho. Recuperala.", "status": "approved"},
    {"title": "Renunciaste y no te pagaron todo?", "content": "Anuncio de conversion para finiquitos incompletos. CTA: Revisamos si tu finiquito incluye todas las prestaciones.", "status": "approved"},
    {"title": "Te despidieron estando incapacitado?", "content": "Anuncio de conversion para despido durante incapacidad. CTA: Eso es ilegal. Te ayudamos a reclamar tu indemnizacion.", "status": "approved"},
    {"title": "Necesitas un abogado laboral?", "content": "Anuncio de conversion generico. CTA: Expertos en derecho laboral. Primera consulta gratuita. Resultados comprobados.", "status": "approved"},
    {"title": "Tu demanda laboral no avanza?", "content": "Anuncio de conversion para casos estancados. CTA: Segunda opinion legal. Evaluamos tu caso y te decimos que opciones tienes.", "status": "approved"},
    {"title": "Defiende tus derechos laborales", "content": "Anuncio de conversion final. CTA: No dejes que pasen por encima de ti. Conoce tus derechos y ejercelos.", "status": "approved"},
]


def run():
    tenant = Tenant.objects.get(subdomain="martinez-legal")
    project = Project.objects.filter(tenant=tenant).first()

    if not project:
        print("ERROR: No project found for tenant martinez-legal. Run the template first.")
        return

    print(f"Seedando contenido para: {tenant.name} > {project.name}")
    print(f"Total de temas: {len(CONTENT_TOPICS)} + {len(ADS)} anuncios = {len(CONTENT_TOPICS) + len(ADS)}")

    count = 0
    with transaction.atomic():
        for topic in CONTENT_TOPICS:
            master, created = ContentMaster.objects.get_or_create(
                tenant=tenant,
                project=project,
                title=topic["title"],
                defaults={
                    "content": topic["content"],
                    "status": topic["status"],
                },
            )
            if created:
                count += 1

        for ad in ADS:
            master, created = ContentMaster.objects.get_or_create(
                tenant=tenant,
                project=project,
                title=ad["title"],
                defaults={
                    "content": ad["content"],
                    "status": ad["status"],
                },
            )
            if created:
                count += 1

    print(f"\n[DONE] {count} ContentMaster(s) creados para el despacho laboral.")
    print(f"Total en DB: {ContentMaster.objects.filter(tenant=tenant, project=project).count()}")


if __name__ == "__main__":
    run()
