from flask import Flask, request
import json
import redis as redis
from loguru import logger

HISTORY_LENGTH = 10
DATA_KEY = 'engine_temperature'


app = Flask(__name__)

@app.route('/')
def hello():
    # print("HEllo")
    # redis.incr('hits')
    # counter = str(redis.get('hits'),'utf-8')
    return "Welcome to this webapage!, This webpage has been viewed "+" time(s)"


@app.route('/record', methods=['GET', 'POST'])
def record_engine_temperature():
    payload = request.get_json(force=True)
    logger.info(f"(*) record request --- {json.dumps(payload)} (*)")

    engine_temperature = payload.get("engine_temperature")
    logger.info(f"engine temperature to record is: {engine_temperature}")

    database = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
    database.lpush(DATA_KEY, engine_temperature)
    logger.info(f"stashed engine temperature in redis: {engine_temperature}")

    while database.llen(DATA_KEY) > HISTORY_LENGTH:
        database.rpop(DATA_KEY)
    engine_temperature_values = database.lrange(DATA_KEY, 0, -1)
    logger.info(f"engine_temperature list now contains these values: {engine_temperature_values}")

    logger.info(f"record request successful")
    return {"success": True}, 200

@app.route('/collect', methods=['POST'])
def collect_engine_temperature():
    database = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
    engine_temperature_values = database.lrange(DATA_KEY, 0, -1)
    logger.info(f"got engine temperature values from redis: {engine_temperature_values} ")

    sum_temp_values = 0
    for data in engine_temperature_values:
        sum_temp_values += float(data)
    average_engine_temperature = sum_temp_values/len(engine_temperature_values)

    logger.info(f"average engine temperature {average_engine_temperature}")
    logger.info(f"current engine temperature {engine_temperature_values[0]}")

    result = {"current_engine_temperature": engine_temperature_values[0], "average_engine_temperature": average_engine_temperature}
    logger.info(f"collect request successful")

    return result

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

    