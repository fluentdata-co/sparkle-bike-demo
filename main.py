# Author: Juan Carlos Ruiz
# Company: Google Cloud
# Role: Partner Engineer
# Email: juankruiz@google.com

import os
import time
import json
import dataclasses
import decimal
from InvoiceUtil import read_xml_file, extract_cdata
from InvoiceParsers import parse_cdata_to_invoices

class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            elif isinstance(o, decimal.Decimal):
                return str(o)
            return super().default(o)

def process_folder(folder_path, file_count, invoice_count):
    """
    Processes all XML files in the given folder.
    """
    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            try:
                filepath = os.path.join(folder_path, filename)
                xml_data = read_xml_file(filepath)
                cdata_xmls = extract_cdata(xml_data)
                invoices = parse_cdata_to_invoices(cdata_xmls)

                file_count += 1
                invoice_count += len(invoices)

                for invoice in invoices:
                    if invoice:
                        print(json.dumps(invoice, cls=EnhancedJSONEncoder))
                        print(f"Folder: {folder_path}, File: {filename}, UBLVersionID: {invoice.UBLVersionID}, "
                              f"CustomizationID: {invoice.CustomizationID}, ID: {invoice.ID}, IssueDate: {invoice.IssueDate}, "
                              f"DocumentCurrencyCode: {invoice.DocumentCurrencyCode}")

            except Exception as e:
                print(f"Error processing file {filename}: {e}")
    return file_count, invoice_count

if __name__ == "__main__":
    start_time = time.time()
    file_count = 0
    invoice_count = 0

    folders = ["cliente_1", "cliente_2"]
    for folder in folders:
        file_count, invoice_count = process_folder(folder, file_count, invoice_count)

    end_time = time.time()
    total_time = end_time - start_time

    print(f"\nTotal execution time: {total_time:.5f} seconds")
    print(f"Average time per file: {total_time / file_count:.5f} seconds")
    print(f"Average time per invoice: {total_time / invoice_count:.5f} seconds")
    print(f"Total files processed: {file_count}")
    print(f"Total invoices processed: {invoice_count}")