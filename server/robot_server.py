# -*- coding: utf8 -*-
"""Flask application for the Robot.

This module implements the web-API for the Robot.
It respond to HTTP requests to get object category from an image
"""
import sys
import logging
import json
import uuid
import os
import cStringIO
import numpy as np
import uwsgi
from werkzeug.exceptions import HTTPException
from PIL import Image
from flask import Flask, request, Response, abort, make_response

import tensorflow as tf
from NodeLookup import NodeLookup


MODEL_PATH = '/home/robot/visiobotlocal/server/data/classify_image_graph_def.pb'
LABEL_LOOKUP_PATH = '/home/robot/visiobotlocal/server/data/imagenet_synset_to_human_label_map.txt'
UID_LOOKUP_PATH = '/home/robot/visiobotlocal/server/data/imagenet_2012_challenge_label_map_proto.pbtxt'
UPLOAD_PATH = '/home/robot/visiobotlocal/server/www/upload/'


def log_and_abort(msg, code):
    """ Log an error and return an HTTP response with the given code.

    Args:
        msg: Message to log as ERROR.
        code: HTTP code to return.
    """
    logging.error(msg)
    abort(make_response(msg, code))


def initialize_log():
    """Initializes the log file.
    The path to the log file must be defined in a uWSGI placeholder log_file.

    Raises:
        Raises an Exception if the uWSGI placeholder log_file doesn't exist.
    """
    log_format = "[%(levelname)s] [%(asctime)s] [%(message)s] [%(funcName)s]"
    if 'log_file' in uwsgi.opt:
        logging.basicConfig(format=log_format, filename=uwsgi.opt['log_file'], level=logging.DEBUG)
    else:
        raise Exception("log_file is not defined as uWSGI placeholder.")


def initialize_flask_app():
    """Create and initialize the Flask app.

    Returns:
        Flask app
    """
    app = Flask(__name__)
    create_graph()
    app.sess = tf.Session()
    app.node_lookup = NodeLookup(UID_LOOKUP_PATH, LABEL_LOOKUP_PATH)
    return app


def allowed_file(filename):
    """ Check if the filename has an allowed extension.

    Args:
        filename: Name of the file to be checked, with its extension

    Returns:
        True if the extension is allowed.
    """
    allowed_extensions = set(['jpg', 'jpeg', 'gif', 'bmp', 'png'])
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in allowed_extensions


def create_graph():
    """ Creates graph from saved graph_def.pb.
    """
    logging.info('Load graph')
    with tf.gfile.FastGFile(MODEL_PATH, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def predict_image(app, image):
    buffer = cStringIO.StringIO()
    image.save(buffer, format="JPEG")

    softmax_tensor = app.sess.graph.get_tensor_by_name('softmax:0')
    predictions = app.sess.run(softmax_tensor,
                           {'DecodeJpeg/contents:0': buffer.getvalue()})
    return np.squeeze(predictions)


def get_predictions_result(app, predictions):
    # Creates node ID --> English string lookup.
    best_id = predictions.argsort()[-1]
    full_label = app.node_lookup.id_to_string(best_id)
    short_label = full_label.split(',')[0]
    result = {'label': short_label,
              'score': "{:.3f}".format(predictions[best_id])}
    return result


def get_image_in_request():
    """ Get the image in the last request.

    Returns:
        Image in correct format for CNN classification : range [0, 1], 3 channels.
    """
    if 'file' not in request.files:
        log_and_abort(u"Missing field 'file' in request", 400)

    image_file = request.files['file']
    logging.info(u'File name received: %s', image_file.filename)
    #if not image_file or not allowed_file(image_file.filename):
    #    log_and_abort(u"File is not allowed", 403)

    try:
        image = Image.open(image_file)
        image.save(os.path.join(UPLOAD_PATH, str(uuid.uuid1()) + '.jpg'))
    except IOError:
        log_and_abort(u"File is not readable", 403)

    return image


# Create the Flask app.
# We need to create it here, because we need the decorator app.route below.
try:
    initialize_log()
    logging.debug(u'Initializing Flask app ...')
    app = initialize_flask_app()
    logging.debug(u'Flask app initialized!')
except Exception as err:
    error = u"Can't initialize Flask app : %s" % err
    logging.error(error)
    sys.exit(error)


@app.route("/predict", methods=['POST'])
def predict():
    """Predict the object in an image.
    """
    try:
        image = get_image_in_request()
        probas_image = predict_image(app, image)
        result = get_predictions_result(app, probas_image)
    except HTTPException:
        raise
    except Exception as uncatched_err:
        error_desc = u"Uncatched error in predict: {e}".format(e=uncatched_err)
        logging.error(error_desc)
        return Response(response=error_desc, status=500, mimetype="text/plain")

    return Response(response=json.dumps(result), status=200, mimetype="application/json")


@app.route("/available", methods=['GET'])
def available():
    """ Check if the service is available.

    Returns:
        A response with a json {"success": "1"} and status code 200 if the service is available.
    """
    return Response(response=json.dumps({"status": 1}), status=200, mimetype="application/json")


# Only for test.
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=False)
