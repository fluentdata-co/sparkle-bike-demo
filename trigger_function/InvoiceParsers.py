# Author: Juan Carlos Ruiz
# Company: Google Cloud
# Role: Partner Engineer
# Email: juankruiz@google.com

from InvoiceObjects import *
import xml.etree.ElementTree as ET
from typing import List, Optional

namespaces = {
    'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
    'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'
}

def safe_text(element):
    """
    Safely extracts text from an element, returning None if the element is None.
    """
    return element.text if element is not None else None

def parse_cdata_to_invoices(cdata_xmls: List[Optional[str]]) -> List[Optional[Invoice]]:
    """
    Parses a list of CDATA XML strings and returns a list of Invoice objects.
    """
    invoices = []
    for xml_string in cdata_xmls:
        if xml_string:  # Only parse if xml_string is not None
            try:
                invoice = parse_xml_to_object(xml_string)
                if invoice:
                    invoices.append(invoice)
            except Exception as e:
                print(f"Error parsing CDATA XML to Invoice: {e}")
    return invoices

def parse_xml_to_object(xml_string: str) -> Optional[Invoice]:
    """
    Parses an XML string and creates an Invoice object.
    """
    try:
        root = ET.fromstring(xml_string)
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return None

    # Extract data from XML and create nested objects, handling None values directly
    try:
        invoice = Invoice(
            UBLVersionID=safe_text(root.find(".//cbc:UBLVersionID", namespaces=namespaces)),
            CustomizationID=safe_text(root.find(".//cbc:CustomizationID", namespaces=namespaces)),
            ProfileID=safe_text(root.find(".//cbc:ProfileID", namespaces=namespaces)),
            ID=safe_text(root.find(".//cbc:ID", namespaces=namespaces)),
            UUID=safe_text(root.find(".//cbc:UUID", namespaces=namespaces)),
            IssueDate=safe_text(root.find(".//cbc:IssueDate", namespaces=namespaces)),
            IssueTime=safe_text(root.find(".//cbc:IssueTime", namespaces=namespaces)),
            DueDate=safe_text(root.find(".//cbc:DueDate", namespaces=namespaces)),
            InvoiceTypeCode=safe_text(root.find(".//cbc:InvoiceTypeCode", namespaces=namespaces)),
            DocumentCurrencyCode=safe_text(root.find(".//cbc:DocumentCurrencyCode", namespaces=namespaces)),
            LineCountNumeric=int(safe_text(root.find(".//cbc:LineCountNumeric", namespaces=namespaces))) if root.find(".//cbc:LineCountNumeric", namespaces=namespaces) is not None else None,
            AccountingSupplierParty=parse_party(root.find(".//cac:AccountingSupplierParty", namespaces=namespaces), namespaces),
            AccountingCustomerParty=parse_party(root.find(".//cac:AccountingCustomerParty", namespaces=namespaces), namespaces),
            Delivery=parse_delivery(root.find(".//cac:Delivery", namespaces=namespaces), namespaces),
            DeliveryTerms=parse_delivery_terms(root.find(".//cac:DeliveryTerms", namespaces=namespaces), namespaces),
            PaymentMeans=parse_payment_means(root.find(".//cac:PaymentMeans", namespaces=namespaces), namespaces),
            TaxTotal=parse_tax_total(root.find(".//cac:TaxTotal", namespaces=namespaces), namespaces),
            LegalMonetaryTotal=parse_legal_monetary_total(root.find(".//cac:LegalMonetaryTotal", namespaces=namespaces), namespaces),
            InvoiceLine=parse_invoice_line(root.findall(".//cac:InvoiceLine", namespaces=namespaces), namespaces)
        )
    except AttributeError as e:
        print(f"Error extracting data from XML: {e}")
        return None

    return invoice

def parse_party(party_element, namespaces) -> Optional[Party]:
    if party_element is None:
        return None

    return Party(
        PartyName=safe_text(party_element.find(".//cac:PartyName/cbc:Name", namespaces=namespaces)),
        PhysicalLocation=parse_address(party_element.find(".//cac:PhysicalLocation/cac:Address", namespaces=namespaces), namespaces),
        PartyTaxScheme=parse_tax_scheme(party_element.find(".//cac:PartyTaxScheme", namespaces=namespaces), namespaces),
        PartyLegalEntity=parse_legal_entity(party_element.find(".//cac:PartyLegalEntity", namespaces=namespaces), namespaces),
        Contact=parse_contact(party_element.find(".//cac:Contact", namespaces=namespaces), namespaces)
    )

def parse_address(address_element, namespaces) -> Optional[Address]:
    if address_element is None:
        return None

    return Address(
        ID=safe_text(address_element.find(".//cbc:ID", namespaces=namespaces)),
        CityName=safe_text(address_element.find(".//cbc:CityName", namespaces=namespaces)),
        PostalZone=safe_text(address_element.find(".//cbc:PostalZone", namespaces=namespaces)),
        CountrySubentity=safe_text(address_element.find(".//cbc:CountrySubentity", namespaces=namespaces)),
        CountrySubentityCode=safe_text(address_element.find(".//cbc:CountrySubentityCode", namespaces=namespaces)),
        AddressLine=safe_text(address_element.find(".//cac:AddressLine/cbc:Line", namespaces=namespaces)),
        Country=safe_text(address_element.find(".//cac:Country/cbc:IdentificationCode", namespaces=namespaces))
    )

def parse_tax_scheme(tax_scheme_element, namespaces) -> Optional[TaxScheme]:
    if tax_scheme_element is None:
        return None

    tax_scheme_info_element = tax_scheme_element.find(".//cac:TaxScheme", namespaces=namespaces)
    tax_scheme_info = None
    if tax_scheme_info_element is not None:
        tax_scheme_info = TaxScheme(
            ID=safe_text(tax_scheme_info_element.find(".//cbc:ID", namespaces=namespaces)),
            Name=safe_text(tax_scheme_info_element.find(".//cbc:Name", namespaces=namespaces))
        )

    return TaxScheme(
        RegistrationName=safe_text(tax_scheme_element.find(".//cbc:RegistrationName", namespaces=namespaces)),
        CompanyID=safe_text(tax_scheme_element.find(".//cbc:CompanyID", namespaces=namespaces)),
        TaxLevelCode=safe_text(tax_scheme_element.find(".//cbc:TaxLevelCode", namespaces=namespaces)),
        ID=tax_scheme_info.ID if tax_scheme_info else None,
        Name=tax_scheme_info.Name if tax_scheme_info else None
    )

def parse_legal_entity(legal_entity_element, namespaces) -> Optional[LegalEntity]:
    if legal_entity_element is None:
        return None

    return LegalEntity(
        RegistrationName=safe_text(legal_entity_element.find(".//cbc:RegistrationName", namespaces=namespaces)),
        CompanyID=safe_text(legal_entity_element.find(".//cbc:CompanyID", namespaces=namespaces))
    )

def parse_contact(contact_element, namespaces) -> Optional[Contact]:
    if contact_element is None:
        return None

    return Contact(
        Telephone=safe_text(contact_element.find(".//cbc:Telephone", namespaces=namespaces)),
        ElectronicMail=safe_text(contact_element.find(".//cbc:ElectronicMail", namespaces=namespaces))
    )

def parse_delivery(delivery_element, namespaces) -> Optional[Delivery]:
    if delivery_element is None:
        return None

    return Delivery(
        ActualDeliveryDate=safe_text(delivery_element.find(".//cbc:ActualDeliveryDate", namespaces=namespaces)),
        DeliveryAddress=parse_address(delivery_element.find(".//cac:DeliveryAddress", namespaces=namespaces), namespaces)
    )

def parse_delivery_terms(delivery_terms_element, namespaces) -> Optional[DeliveryTerms]:
    if delivery_terms_element is None:
        return None

    return DeliveryTerms(
        LossRiskResponsibilityCode=safe_text(delivery_terms_element.find(".//cbc:LossRiskResponsibilityCode", namespaces=namespaces))
    )

def parse_payment_means(payment_means_element, namespaces) -> Optional[PaymentMeans]:
    if payment_means_element is None:
        return None

    return PaymentMeans(
        ID=safe_text(payment_means_element.find(".//cbc:ID", namespaces=namespaces)),
        PaymentMeansCode=safe_text(payment_means_element.find(".//cbc:PaymentMeansCode", namespaces=namespaces)),
        PaymentDueDate=safe_text(payment_means_element.find(".//cbc:PaymentDueDate", namespaces=namespaces))
    )

def parse_tax_total(tax_total_element, namespaces) -> Optional[TaxTotal]:
    if tax_total_element is None:
        return None

    return TaxTotal(
        TaxAmount=safe_text(tax_total_element.find(".//cbc:TaxAmount", namespaces=namespaces))
    )

def parse_legal_monetary_total(legal_monetary_total_element, namespaces) -> Optional[LegalMonetaryTotal]:
    if legal_monetary_total_element is None:
        return None

    return LegalMonetaryTotal(
        LineExtensionAmount=safe_text(legal_monetary_total_element.find(".//cbc:LineExtensionAmount", namespaces=namespaces)),
        TaxExclusiveAmount=safe_text(legal_monetary_total_element.find(".//cbc:TaxExclusiveAmount", namespaces=namespaces)),
        TaxInclusiveAmount=safe_text(legal_monetary_total_element.find(".//cbc:TaxInclusiveAmount", namespaces=namespaces)),
        PayableAmount=safe_text(legal_monetary_total_element.find(".//cbc:PayableAmount", namespaces=namespaces))
    )

def parse_invoice_line(invoice_line_elements, namespaces) -> Optional[List[InvoiceLine]]:
    """
    Parses a list of invoice line elements and returns a list of InvoiceLine objects.
    """
    invoice_lines = []
    for invoice_line_element in invoice_line_elements:
        invoice_lines.append(InvoiceLine(
            ID=safe_text(invoice_line_element.find(".//cbc:ID", namespaces=namespaces)),
            InvoicedQuantity=Decimal(safe_text(invoice_line_element.find(".//cbc:InvoicedQuantity", namespaces=namespaces))) if invoice_line_element.find(".//cbc:InvoicedQuantity", namespaces=namespaces) is not None else None,
            LineExtensionAmount=safe_text(invoice_line_element.find(".//cbc:LineExtensionAmount", namespaces=namespaces)),
            TaxTotal=parse_tax_total(invoice_line_element.find(".//cac:TaxTotal", namespaces=namespaces), namespaces),
            Item=parse_item(invoice_line_element.find(".//cac:Item", namespaces=namespaces), namespaces),
            Price=parse_price(invoice_line_element.find(".//cac:Price", namespaces=namespaces), namespaces)
        ))
    return invoice_lines

def parse_item(item_element, namespaces) -> Optional[Item]:
    if item_element is None:
        return None

    return Item(
        Description=safe_text(item_element.find(".//cbc:Description", namespaces=namespaces)),
        SellersItemIdentification=safe_text(item_element.find(".//cac:SellersItemIdentification/cbc:ID", namespaces=namespaces))
    )

def parse_price(price_element, namespaces) -> Optional[Price]:
    if price_element is None:
        return None

    return Price(
        PriceAmount=safe_text(price_element.find(".//cbc:PriceAmount", namespaces=namespaces)),
        BaseQuantity=int(safe_text(price_element.find(".//cbc:BaseQuantity", namespaces=namespaces))) if price_element.find(".//cbc:BaseQuantity", namespaces=namespaces) is not None else None
    )