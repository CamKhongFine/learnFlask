from celery import *
from tasks.tasks import long_running_task, short_running_task, chord_running_task, chain_running_task, retry_running_task, chunk_running_task
from celery.result import AsyncResult
from flask import request, jsonify, Blueprint, make_response

task = Blueprint('task', __name__)

@task.route("/task/long", methods=["POST"])
def long_task() -> dict[str, object]:
    iterations = request.args.get('iterations')      # Dung de lay parameter duoc gan vao URL
    result = long_running_task.delay(int(iterations))   # Tra ve mot doi tuong AsyncResult
    return {"result_id" : result.id}

@task.route("/task/short", methods=["POST"])
def short_task() -> dict[str, object]:
    iterations = request.args.get('iterations')      # Dung de lay parameter duoc gan vao URL
    result = short_running_task.delay(int(iterations))   # Tra ve mot doi tuong AsyncResult
    return {"result_id" : result.id}

@task.route("/task/group", methods=["POST"])
def group_task() -> dict[str, object]:
    task_compose = group(long_running_task.s(1), short_running_task.s(1), short_running_task.s(20))
    async_result = task_compose()
    print(async_result.get())
    return {"Success" : async_result.id}

@task.route("/task/chain", methods=["POST"])
def chain_task() -> dict[str, object]:
    task_compose = chain(long_running_task.s(1), chain_running_task.s())
    task_compose()
    return jsonify("Success")

@task.route("/task/chord", methods=["POST"])
def chord_task() -> dict[str, object]:
    chord([long_running_task.s(1), long_running_task.s(1), short_running_task.s(1)])(chord_running_task.s())
    return jsonify("Success")

@task.route("/task/retry", methods=["POST"])
def retry_task() -> dict[str, object]:
    chain(short_running_task.s(1000), retry_running_task.s())()
    return jsonify("Retrying")

@task.route("/task/chunks", methods=["POST"])
def chunk_task() -> dict[str, object]:
    result = chunk_running_task.chunks(zip(range(100), range(100)), 10)()
    result.get()
    return jsonify("Success")

@task.route("/task/map", methods=["POST"])
def map_task() -> dict[str, object]:
    long_running_task.map([1, 1, 1]).apply_async()

    return jsonify("Success")

@task.route("/task/get", methods=["GET"])
def task_result():
    id = request.args.get('id')
    result = AsyncResult(id)           #Lay thong tin ve tac vu
    if result.ready():
        if result.successful():
            return jsonify({
                "Ready" : result.ready(),
                "Successful" : result.successful(),
                "Value" : result.result,
            })
        else:
            return make_response(jsonify({'Message' : str(result.result)}), 400)
    else:
        return make_response(jsonify({'Status': result.status}), 200)