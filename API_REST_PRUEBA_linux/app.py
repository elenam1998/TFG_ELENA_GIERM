#requeriments
from flask import Flask, jsonify, request
import anemometer
from sensorbme import SENSORBME280
from SENSOR_BME import SENSOR_BME
from WIND_SPEED import WIND_SPEED
import Calculadora_RecomendacionesRiego
from RECOMENDACIONES_RIEGO import RECOMENDACIONES_RIEGO

#inicio de la api-rest
app = Flask (__name__)

#mensaje de bienvenida
@app.route('/ping')
def ping():
    return jsonify({"mensaje": "Bienvenido"})

#Peticion datos del sensor BME280
@app.route('/SENSOR_BME')
def getProducts():
    return jsonify({"SENSOR_BME": SENSOR_BME, "mensaje": "Variables meteorologicas"})

#Peticion datos del WIND_SPEED
@app.route('/WIND_SPEED')
def getWind():
    return jsonify({"WIND_SPEED": WIND_SPEED, "mensaje": "Velocidad del viento"})

#Peticion datos de la calculadora
@app.route('/RECOMENDACIONES_RIEGO')
def getRecommendation():
    return jsonify({"RECOMENDACIONES_RIEGO": RECOMENDACIONES_RIEGO, "mensaje": "Recomendacion de riego para su finca"})

#Peticion de una variable concreta del sensor BME280
@app.route('/SENSOR_BME/<string:SENSOR_BME_variable>')
def getProduct(SENSOR_BME_variable):
    SENSOR_BMEFound = [sensor for sensor in SENSOR_BME if sensor['variable'] == SENSOR_BME_variable]
    if (len(SENSOR_BMEFound) > 0):
        return jsonify({"variable" : SENSOR_BMEFound[0]})
    return jsonify({"mensaje": "Variable no encontrada"})

#Modificar valor sensor BME280
@app.route('/SENSOR_BME/<string:SENSOR_BME_variable>', methods=['PUT'])
def editProduct(SENSOR_BME_variable):
    SENSOR_BMEFound = [sensor for sensor in SENSOR_BME if sensor['variable'] == SENSOR_BME_variable]
    if (len(SENSOR_BMEFound) > 0):

        SENSOR_BMEFound[0]['variable'] = request.json['variable']
        SENSOR_BMEFound[0]['valor'] = request.json['valor']
        return jsonify({
            "mensaje": "Product updated",
            "sensor": SENSOR_BMEFound[0]
        })
    return jsonify({"mensaje": "Variable no encontrada"})

#Modificar valor WIND_SPEED
@app.route('/WIND_SPEED/<string:WIND_SPEED_variable>', methods=['PUT'])
def editWind(WIND_SPEED_variable):
    WIND_SPEEDFound = [WIND_SPEED_ for WIND_SPEED_ in WIND_SPEED if WIND_SPEED_['variable'] == WIND_SPEED_variable]
    if (len(WIND_SPEEDFound) > 0):

        WIND_SPEEDFound[0]['variable'] = request.json['variable']
        WIND_SPEEDFound[0]['valor'] = request.json['valor']
        return jsonify({
            "mensaje": "Product updated",
            "WIND_SPEED_": WIND_SPEEDFound[0]
        })
    return jsonify({"mensaje": "Variable no encontrada"})

#Añadir variable a sensor BME280
@app.route('/SENSOR_BME', methods=['POST'])
def addProduct():
    new_variable= {
        "variable":request.json ['variable'],
        "valor":request.json ['valor'],
    }
    SENSOR_BME.append(new_variable)
    return jsonify({"message": "Variable añadida correctamente", "sensor": SENSOR_BME})


#Eliminar variable concreta sensor BME280
@app.route('/SENSOR_BME/<string:SENSOR_BME_variable>', methods=['DELETE'])
def deleteProduct(SENSOR_BME_variable):
    SENSOR_BMEFound = [sensor for sensor in SENSOR_BME if sensor['variable'] == SENSOR_BME_variable]
    if (len(SENSOR_BMEFound) > 0):
         SENSOR_BME.remove(SENSOR_BMEFound[0])
         return jsonify({
             "mensaje": "Product deleted",
             "SENSOR_BME": SENSOR_BME
             })
    return jsonify({"mensaje": "Variable no encontrada"})

#Eliminar valor  WIND_SPEED
@app.route('/WIND_SPEED/<string:WIND_SPEED_variable>', methods=['DELETE'])
def deleteWind(WIND_SPEED_variable):
    WIND_SPEEDFound = [WIND_SPEED_ for WIND_SPEED_ in WIND_SPEED if WIND_SPEED_['variable'] == WIND_SPEED_variable]
    if (len(WIND_SPEEDFound) > 0):
        WIND_SPEED.remove(WIND_SPEEDFound[0])
        return jsonify({
             "mensaje": "Product deleted",
             "WIND_SPEED": WIND_SPEED
             })
    return jsonify({"mensaje": "Variable no encontrada"})

#Eliminar valor Recomendaciones de riego
@app.route('/RECOMENDACIONES_RIEGO/<string:RECOMENDACIONES_RIEGO_variable>', methods=['DELETE'])
def deleteCalc(RECOMENDACIONES_RIEGO_variable):
    RECOMENDACIONES_RIEGOFound = [calc for calc in RECOMENDACIONES_RIEGO if calc['variable'] == RECOMENDACIONES_RIEGO_variable]
    if (len(RECOMENDACIONES_RIEGOFound) > 0):
        RECOMENDACIONES_RIEGO.remove(RECOMENDACIONES_RIEGOFound[0])
        return jsonify({
             "mensaje": "Product deleted",
             "calculadora": RECOMENDACIONES_RIEGO
             })
    return jsonify({"mensaje": "Variable no encontrada"})

if __name__ == '__main__':
    app.run(debug=True, port=4000, host='0.0.0.0')