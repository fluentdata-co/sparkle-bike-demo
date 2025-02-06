# Author: Juan Carlos Ruiz
# Company: Google Cloud
# Role: Partner Engineer
# Email: juankruiz@google.com

from dataclasses import dataclass
from datetime import date, time
from decimal import Decimal
from typing import Optional

@dataclass
class Invoice:
    """
    Represents an invoice. All fields are optional to handle irregular XMLs.
    """
    UBLVersionID: Optional[str] = None
    CustomizationID: Optional[str] = None
    ProfileID: Optional[str] = None
    ID: Optional[str] = None
    UUID: Optional[str] = None
    IssueDate: Optional[date] = None
    IssueTime: Optional[time] = None
    DueDate: Optional[date] = None
    InvoiceTypeCode: Optional[str] = None
    DocumentCurrencyCode: Optional[str] = None
    LineCountNumeric: Optional[int] = None
    AccountingSupplierParty: Optional["Party"] = None
    AccountingCustomerParty: Optional["Party"] = None
    Delivery: Optional["Delivery"] = None
    DeliveryTerms: Optional["DeliveryTerms"] = None
    PaymentMeans: Optional["PaymentMeans"] = None
    TaxTotal: Optional["TaxTotal"] = None
    LegalMonetaryTotal: Optional["LegalMonetaryTotal"] = None
    InvoiceLine: Optional[list["InvoiceLine"]] = None
    AdditionalDocumentReference: Optional[list["AdditionalDocumentReference"]] = None
    DeliveryParty: Optional["DeliveryParty"] = None
    TaxSubtotal: Optional[list["TaxSubtotal"]] = None
    TaxCategory: Optional["TaxCategory"] = None
    Item: Optional["Item"] = None
    Price: Optional["Price"] = None
    ReceiptLineReference: Optional[list["ReceiptLineReference"]] = None
    DocumentReference: Optional[list["DocumentReference"]] = None


@dataclass
class Party:
    PartyName: Optional[str] = None
    PhysicalLocation: Optional["Address"] = None
    PartyTaxScheme: Optional["TaxScheme"] = None
    PartyLegalEntity: Optional["LegalEntity"] = None
    Contact: Optional["Contact"] = None


@dataclass
class Address:
    ID: Optional[str] = None
    CityName: Optional[str] = None
    PostalZone: Optional[str] = None
    CountrySubentity: Optional[str] = None
    CountrySubentityCode: Optional[str] = None
    AddressLine: Optional[str] = None
    Country: Optional[str] = None


@dataclass
class TaxScheme:
    RegistrationName: Optional[str] = None
    CompanyID: Optional[str] = None
    TaxLevelCode: Optional[str] = None
    ID: Optional[str] = None
    Name: Optional[str] = None


@dataclass
class LegalEntity:
    RegistrationName: Optional[str] = None
    CompanyID: Optional[str] = None
    CorporateRegistrationScheme: Optional[str] = None


@dataclass
class Contact:
    Telephone: Optional[str] = None
    ElectronicMail: Optional[str] = None


@dataclass
class Delivery:
    ActualDeliveryDate: Optional[date] = None
    DeliveryAddress: Optional["Address"] = None
    DeliveryParty: Optional["DeliveryParty"] = None


@dataclass
class DeliveryTerms:
    LossRiskResponsibilityCode: Optional[str] = None
    DeliveryLocation: Optional[str] = None


@dataclass
class PaymentMeans:
    ID: Optional[str] = None
    PaymentMeansCode: Optional[str] = None
    PaymentDueDate: Optional[date] = None


@dataclass
class TaxTotal:
    TaxAmount: Optional[Decimal] = None
    TaxSubtotal: Optional[list["TaxSubtotal"]] = None


@dataclass
class LegalMonetaryTotal:
    LineExtensionAmount: Optional[Decimal] = None
    TaxExclusiveAmount: Optional[Decimal] = None
    TaxInclusiveAmount: Optional[Decimal] = None
    PayableAmount: Optional[Decimal] = None


@dataclass
class InvoiceLine:
    ID: Optional[str] = None
    InvoicedQuantity: Optional[Decimal] = None
    LineExtensionAmount: Optional[Decimal] = None
    TaxTotal: Optional["TaxTotal"] = None
    Item: Optional["Item"] = None
    Price: Optional["Price"] = None
    ReceiptLineReference: Optional[list["ReceiptLineReference"]] = None
    DocumentReference: Optional[list["DocumentReference"]] = None


@dataclass
class AdditionalDocumentReference:
    ID: Optional[str] = None
    DocumentTypeCode: Optional[str] = None
    DocumentType: Optional[str] = None


@dataclass
class DeliveryParty:
    PartyName: Optional[str] = None
    PhysicalLocation: Optional["Address"] = None
    PartyTaxScheme: Optional["TaxScheme"] = None
    PartyLegalEntity: Optional["LegalEntity"] = None


@dataclass
class TaxSubtotal:
    TaxableAmount: Optional[Decimal] = None
    TaxAmount: Optional[Decimal] = None
    TaxCategory: Optional["TaxCategory"] = None


@dataclass
class TaxCategory:
    Percent: Optional[Decimal] = None
    TaxScheme: Optional["TaxScheme"] = None


@dataclass
class Item:
    Description: Optional[str] = None
    SellersItemIdentification: Optional[str] = None
    StandardItemIdentification: Optional[str] = None


@dataclass
class Price:
    PriceAmount: Optional[Decimal] = None
    BaseQuantity: Optional[Decimal] = None


@dataclass
class ReceiptLineReference:
    LineID: Optional[str] = None
    DocumentReference: Optional["DocumentReference"] = None


@dataclass
class DocumentReference:
    ID: Optional[str] = None
    DocumentTypeCode: Optional[str] = None
    DocumentType: Optional[str] = None