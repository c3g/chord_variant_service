import chord_variant_service
import os

from chord_lib.responses.flask_errors import *
from flask import Flask, jsonify
from werkzeug.exceptions import BadRequest, NotFound

from chord_variant_service.beacon.routes import bp_beacon
from chord_variant_service.constants import DATA_PATH
from chord_variant_service.ingest import bp_ingest
from chord_variant_service.pool import teardown_pool
from chord_variant_service.search import bp_chord_search
from chord_variant_service.tables.routes import bp_tables
from chord_variant_service.tables.vcf import VCFTableManager
from chord_variant_service.workflows import bp_workflows


SERVICE_NAME = "CHORD Variant Service"
SERVICE_TYPE = "ca.c3g.chord:variant:{}".format(chord_variant_service.__version__)
SERVICE_ID = os.environ.get("SERVICE_ID", SERVICE_TYPE)


application = Flask(__name__)

# TODO: How to share this across processes?
table_manager = VCFTableManager(DATA_PATH)
application.config["TABLE_MANAGER"] = table_manager  # TODO: This is wrong
table_manager.update_tables()

application.register_blueprint(bp_beacon)
application.register_blueprint(bp_chord_search)
application.register_blueprint(bp_ingest)
application.register_blueprint(bp_tables)
application.register_blueprint(bp_workflows)


# Generic catch-all
application.register_error_handler(Exception, flask_error_wrap_with_traceback(flask_internal_server_error,
                                                                              service_name=SERVICE_NAME))
application.register_error_handler(BadRequest, flask_error_wrap(flask_bad_request_error))
application.register_error_handler(NotFound, flask_error_wrap(flask_not_found_error))


@application.teardown_appcontext
def app_teardown_pool(err):
    teardown_pool(err)


@application.route("/service-info", methods=["GET"])
def service_info():
    # Spec: https://github.com/ga4gh-discovery/ga4gh-service-info

    return jsonify({
        "id": SERVICE_ID,
        "name": SERVICE_NAME,
        "type": SERVICE_TYPE,
        "description": "Variant service for a CHORD application.",
        "organization": {
            "name": "C3G",
            "url": "http://c3g.ca"
        },
        "contactUrl": "mailto:david.lougheed@mail.mcgill.ca",
        "version": chord_variant_service.__version__
    })
