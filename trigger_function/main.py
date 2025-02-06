"""DocumentAI workflow: Classify and Parse
"""

import os
import time
import json
import dataclasses
import decimal
from google.cloud import bigquery, documentai, storage
import functions_framework
from InvoiceUtil import extract_cdata
from InvoiceParsers import parse_cdata_to_invoices

def get_document_content(bucket_name, object_name):
    """Read document content from GCS into memory"""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    content = blob.download_as_bytes()
    return blob.content_type, content

# def process(document, project_id, location, processor_id):
#     """Process document with the specified DocumentAI processor"""
#     processor = get_processor(project_id, location, processor_id)
#     request = documentai.ProcessRequest(name=processor.name, raw_document=document)
#     result = documentai_client.process_document(request)
#     return result.document



# def get_text(doc_element: dict, document: dict):
#     """
#     Document AI identifies form fields by their offsets
#     in document text. This function converts offsets
#     to text snippets.
#     """
#     response = ""
#     # If a text segment spans several lines, it will
#     # be stored in different text segments.
#     for segment in doc_element.text_anchor.text_segments:
#         start_index = (
#             int(segment.start_index)
#             if segment in doc_element.text_anchor.text_segments
#             else 0
#         )
#         end_index = int(segment.end_index)
#         response += document.text[start_index:end_index]
#     return response


def save_invoice(bucket_name, object_name, invoice_str):
    """Moves a blob from one bucket to another."""
    print(f"Saving invoice {object_name} in JSON format.")
    storage_client = storage.Client()
    destination_bucket = storage_client.bucket(bucket_name)

    results_text_blob = destination_bucket.blob(object_name)
    results_text_blob.upload_from_string(invoice_str)

    # print("Saving json results into the output bucket...")
    # results_json = {
    #     "document_file_name": object_name,
    #     "document_content": document_dict,
    #     "document_classes": document_classes,
    #     "document_type": document_type,
    # }
    # results_json = json.dumps(results_json)
    # results_json_name = f"{object_name}.json"
    # results_json_blob = destination_bucket.blob(results_json_name)
    # results_json_blob.upload_from_string(results_json)

    # Move object from input to output bucket
    # print(
    #     f"Moving object {object_name} from {bucket_name} to {destination_bucket_name}"
    # )
    # source_bucket = storage_client.bucket(bucket_name)
    # source_blob = source_bucket.blob(object_name)
    # source_bucket.copy_blob(source_blob, destination_bucket, object_name)
    # source_bucket.delete_blob(object_name)

    # Persist results into BigQuery
    # print("Persisting data to BigQuery...")
    # bq_client = bigquery.Client()
    # table_id = os.getenv("BQ_TABLE_ID")
    # job_config = bigquery.LoadJobConfig(
    #     schema=[
    #         bigquery.SchemaField("document_file_name", "STRING"),
    #         bigquery.SchemaField("document_content", "JSON"),
    #         bigquery.SchemaField("document_classes", "JSON"),
    #         bigquery.SchemaField("document_type", "STRING"),
    #     ],
    #     source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    # )
    # uri = f"gs://{destination_bucket_name}/{results_json_name}"
    # print(f"Load file {uri} into BigQuery")
    # load_job = bq_client.load_table_from_uri(
    #     uri,
    #     table_id,
    #     location=os.getenv(
    #         "BQ_LOCATION"
    #     ),  # Must match the destination dataset location.
    #     job_config=job_config,
    # )
    # load_job.result()

#     print("Process output completed.")
class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        elif isinstance(o, decimal.Decimal):
            return str(o)
        return super().default(o)

def process_invoice(bucket_name, object_name):
    """Process an invoice stored in GCS."""
    print("Invoicing processing started.")
    mime_type, content = get_document_content(bucket_name, object_name)
    cdata_xmls = extract_cdata(content)
    invoices = parse_cdata_to_invoices(cdata_xmls)

    i = 1
    for invoice in invoices:
        if invoice:
            invoice_str = json.dumps(invoice, cls=EnhancedJSONEncoder)
            print(invoice_str)
            save_invoice(bucket_name, object_name[:-4] + "-" + str(i) + ".json", invoice_str)
            i = i + 1

    #print(cdata_xmls)
    # raw_document = documentai.RawDocument(content=content, mime_type=mime_type)

    # project_id = os.getenv("PROJECT_ID")

    # # Classify document
    # document = process(raw_document, project_id, location, classifier_id)
    # document_classes = {}
    # for entity in document.entities:
    #     classification = entity.type_
    #     confidence = entity.confidence
    #     document_classes[f"{classification}"] = confidence

    # # Parse document
    # document = process(raw_document, project_id, location, parser_id)
    # document_text = document.text

    # # Extract key value pairs
    # document_pages = document.pages
    # document_dict = {}
    # for page in document_pages:
    #     for form_field in page.form_fields:
    #         field_name = get_text(form_field.field_name, document)
    #         field_value = get_text(form_field.field_value, document)
    #         document_dict[f"{field_name}"] = field_value

    # print("Document processing complete.")
    # process_output(
    #     bucket_name, object_name, document_text, document_dict, document_classes, mime_type
    # )


@functions_framework.cloud_event
def trigger_gcs(cloud_event):
    """Triggered by a change in a storage bucket"""
    data = cloud_event.data
    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    bucket = data["bucket"]
    name = data["name"]
    metageneration = data["metageneration"]
    created = data["timeCreated"]
    updated = data["updated"]

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket}")
    print(f"File: {name}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {created}")
    print(f"Updated: {updated}")


    if name.endswith(".xml"):
        start_time = time.time()
        process_invoice(bucket, name)
        end_time = time.time()
        total_time = end_time - start_time

        print(f"\nTotal execution time: {total_time:.5f} seconds")

