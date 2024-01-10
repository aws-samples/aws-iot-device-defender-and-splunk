""" Lambda function for transforming source records from Kinesis Data Firehose.
Designed to transform AWS IoT Device Defender metrics exports for consumption
by Splunk HTTP Event Collector (HEC). """

## Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
## SPDX-License-Identifier: MIT-0

import base64
import json
import logging
import os

# Environment variable for Splunk source type field.
SPLUNK_SOURCE_TYPE = os.environ["SPLUNK_SOURCE_TYPE"]

# Set Python logging.
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# pylint: disable=unused-argument
def lambda_handler(event, context):
    """ Function to transform source records for consumption by
    Splunk HTTP Event Collector (HEC) as JSON events. Deals with
    batch of records. Separates out multiple metrics into separate
    JSON objects. """
    input_records = event["records"]
    output_records = []
    num_events = 0
    logger.info(
            "%s record(s) available for processing...",
            str(len(input_records))
        )
    try:
        for input_record in input_records:
            input_payload = json.loads(base64.b64decode(input_record["data"]))
            # Start payload transformation.
            json_string = ""
            # Splunk HEC accepts multiple events in one API interaction.
            # https://docs.splunk.com/Documentation/SplunkCloud/latest/Data/FormateventsforHTTPEventCollector.
            for metric in input_payload["metrics"]:
                json_string += json.dumps({
                    "sourcetype": SPLUNK_SOURCE_TYPE,
                    "event": metric
                })
                num_events += 1
            print(str(json_string))
            # End payload transformation.
            output_record = {
               "recordId": input_record["recordId"],
               "result": "Ok",
               "data": base64.b64encode(
                        json_string.encode("utf-8")
                    ).decode("utf-8")
            }
            print(str(output_record))
            output_records.append(output_record)
    except Exception as ex:         # pylint: disable=broad-except
        logger.error("Error encountered: %s", str(ex), exc_info=True)
    else:
        logger.info(
                "Successfully transformed %s record(s) containing %s events.",
                str(len(output_records)),
                str(num_events)
            )
    return {"records": output_records}
