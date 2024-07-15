
from NetworkConfig import host_list
from API import app, Id


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=host_list[Id]["port"], debug=False, threaded=True)
