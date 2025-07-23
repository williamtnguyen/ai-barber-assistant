"""
Wrapper functions as tools for Hair Service Appointment Booking Agent
"""

from datetime import datetime
from typing import Any, Dict, List
from strands import tool
from src.services.square_appointments_dao import SquareAppointmentsDao, CatalogResponse


appointments_dao = SquareAppointmentsDao()


@tool
def list_catalog() -> CatalogResponse:
    return appointments_dao.list_catalog()


@tool
def get_available_slots(service_name: str) -> Dict[str, List[str]]:
    # Need to refetch since Agent LLM call internally processes list_catalog response and
    # customer service selection inputting as service_name string
    catalog_response = appointments_dao.list_catalog()
    if service_name not in catalog_response.available_services:
        raise Exception("Customer selected service does not exist in current catalog!")
    service_variation_id = catalog_response.available_services[service_name].service_variation_id
    response = appointments_dao.get_available_slots(service_id=service_variation_id)
    return response


@tool
def convert_day_time_strings_to_datetime_obj(
    chosen_day: str,
    chosen_time: str,
) -> datetime:
    """
    Given a chosen_day with format such as 2025-07-22, 2025-07-23, 2025-07-24
    and a chosen_time with format such as 08:30 PM, 09:00 PM, 09:30 PM, 10:00 PM, 10:30 PM

    Convert to datetime object in RFC3339 format.
    """
    return datetime.strptime(f"{chosen_day} {chosen_time}", "%Y-%m-%d %I:%M %p")


@tool
def create_appointment_booking(
    start_at: datetime,
    service_variation_id: str,
    service_variation_version: int,
    team_member_id: str,
) -> Dict[str, Any]: 
    return appointments_dao.create_booking(
        start_at=start_at,
        service_variation_id=service_variation_id,
        service_variation_version=service_variation_version,
        team_member_id=team_member_id,
    )
