

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from swiplserver import PrologMQI, PrologThread


class ActionHelloWorld(Action):

     def name(self) -> Text:
         return "action_hello_world"
     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message(text="Hello World!")

         return []

class ActionaOcupacion (Action):
    def name(self) -> Text:
         return "action_ocupacion"
    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
             ocupacion = tracker.latest_message['intent'].get('name')
             ocup = tracker.latest_message['entities'][0]['value']
             if ocupacion == "usuarioEstudia" :
                SlotSet("ocup", ocup )
             if ocupacion == "usuarioTrabaja":
                SlotSet("ocup", ocup)
             dispatcher.utter_message(text="Ahah, buenisimo")
             print(str(ocupacion))
             ocupacion = tracker.get_slot("ocup")
             print(str(ocupacion))
             
             


class ActionPresentacion(Action):
    def name(self) -> Text:
         return "action_Presentacion"
    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        nombre = tracker.latest_message['entities'][0]['value']
        SlotSet("name2", nombre)
        dispatcher.utter_message(text= "un gusto " + nombre)



class ActionGustarOcupacion(Action):
    def name(self) -> Text:
         return "action_gustarOcupacion"
    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
             ocupacion = tracker.get_slot("ocup")
             print(str(ocupacion))
             if ocupacion == "estudiante" or ocupacion == "estudio"  or ocupacion == "estudiando" or ocupacion == "universidad" :
                dispatcher.utter_message(text="A vos te gusta lo que estudias??")
             if ocupacion == "trabajo" or ocupacion == "trabajando" or ocupacion == "laburando" :
                dispatcher.utter_message(text="A vos te gusta tu trabajo??")
             



class ActionDespedida(Action):
    def name(self) -> Text:
         return "action_despedida"
    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
             nombre = " desconocido "
             if (tracker.get_slot("name2") != None):
                 nombre = tracker.get_slot("name2")
             dispatcher.utter_message(text= " nos vemos " + nombre)


class ActionFinalAprobado(Action):
    def name(self) -> Text:
         return "action_finalAprobado"
    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        materia = tracker.latest_message['entities'][0]['value']
        SlotSet("name", materia)
        with PrologMQI(port=8000) as mqi:
                with mqi.create_thread() as prolog_thread:
                    prolog_thread.query_async("consult('C:/Users/bauti/RasaProject/UniversoChatBot.pl')", find_all = False)
                    prolog_thread.query_async(f"final_aprobado({materia}, _)", find_all = False)
                    result = prolog_thread.query_async_result()
                    if str(result) == "True" :
                        message = "Si aprobe el final de " + materia
                    else:
                        message = "No, no aprobe el final de " + materia
                    print(str(result))
                    dispatcher.utter_message(text= message)
                    return[]


class ActionAnioMateria(Action):
    def name(self) -> Text:
         return "action_anioMateria"
    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
             materia = tracker.get_slot("name")
             with PrologMQI(port=8000) as mqi:
                with mqi.create_thread() as prolog_thread:
                    L = []
                    prolog_thread.query_async("consult('C:/Users/bauti/RasaProject/UniversoChatBot.pl')", find_all = False)
                    prolog_thread.query_async(f"findall(Anio,final_aprobado({materia}, Anio ),L)", find_all = False)
                    result = prolog_thread.query_async_result()[0].pop("L")
                    if str(result[0]) == "1":
                        message = "el final es de Primero" 
                    if str(result[0]) == "2":
                        message = "el final es de Segundo" 
                    if str(result[0]) == "3":
                        message = "el final es de Tercero" 
                    print(str(result))
                    dispatcher.utter_message(text= message )
                    return[]


class ActionaMateriasEnCurso (Action):
    def name(self) -> Text:
         return "action_materiasEnCurso"
    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
             with PrologMQI(port=8000) as mqi:
                with mqi.create_thread() as prolog_thread:
                    L = []
                    prolog_thread.query_async("consult('C:/Users/bauti/RasaProject/UniversoChatBot.pl')", find_all = False)
                    prolog_thread.query_async(f"findall(Nombre,curso_materia(Nombre),L)", find_all = False)
                    result = prolog_thread.query_async_result()[0].pop("L")
                    print(str(result))
                    dispatcher.utter_message(text= "Las materias que estoy cursando son: " + f"{result}")
                    return[]


class ActionaFinalesAprobados (Action):
    def name(self) -> Text:
         return "action_finalesAprobados"
    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
             with PrologMQI(port=8000) as mqi:
                with mqi.create_thread() as prolog_thread:
                    L = []
                    prolog_thread.query_async("consult('C:/Users/bauti/RasaProject/UniversoChatBot.pl')", find_all = False)
                    prolog_thread.query_async(f"findall(Nombre,final_aprobado(Nombre, Cod),L)", find_all = False)
                    result = prolog_thread.query_async_result()[0].pop("L")
                    print(str(result))
                    dispatcher.utter_message(text= "Los finales que tengo aprobados son: " + f"{result}")
                    return[]

class ActionaFinalesAprobadosPorAnio (Action):
    def name(self) -> Text:
         return "action_finalesAprobadosAnio"
    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
             anio = tracker.latest_message['intent'].get('name')
             if str(anio) == "finalPrimerAnio" :
                aux = 1
             if str(anio) == "finalSegundoAnio" :
                aux = 2
             if str(anio) == "finalTercerAnio" :
                aux = 3
             with PrologMQI(port=8000) as mqi:
                with mqi.create_thread() as prolog_thread:
                    L = []
                    prolog_thread.query_async("consult('C:/Users/bauti/RasaProject/UniversoChatBot.pl')", find_all = False)
                    prolog_thread.query_async(f"findall(Nombre,final_aprobado(Nombre, {aux}),L)", find_all = False)
                    result = prolog_thread.query_async_result()[0].pop("L")
                    print(str(result))
                    dispatcher.utter_message(text= "Los finales que tengo aprobados de ese año son: " + f"{result}")
                    return[]


