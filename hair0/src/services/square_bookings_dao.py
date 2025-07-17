"""
DAO layer for Square Bookings API
"""

from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from square import Square
from square.environment import SquareEnvironment
from square.requests.search_availability_query import SearchAvailabilityQueryParams
from square.requests.search_availability_filter import SearchAvailabilityFilterParams
from square.requests.time_range import TimeRangeParams
from square.requests.segment_filter import SegmentFilterParams
from square.requests.filter_value import FilterValueParams
from square.requests.booking import BookingParams
from square.requests.appointment_segment import AppointmentSegmentParams
from square.types.catalog_object_item import CatalogObjectItem
from square.types.catalog_object_item_variation import CatalogObjectItemVariation
from datetime import datetime, timedelta
import os
import pytz
import asyncio
import random


class SquareBookingsDao:

    def __init__(self, environment=SquareEnvironment.SANDBOX):
        load_dotenv()
        self.barbershop_location_id = os.getenv("BARBERSHOP_LOCATION_ID")
        self.test_customer_id = os.getenv("TEST_CUSTOMER_ID")
        access_token = os.getenv("SQUARE_ACCESS_TOKEN")
        self.square_client = Square(
            token=access_token,
            environment=environment,
        )


    async def list_bookings(
        self,
        start_at_min: Optional[str] = None,
        start_at_max: Optional[str] = None
    ) -> List[Dict]:
        """
        List bookings within a time range.
        
        Args:
            start_time: ISO format datetime string (optional)
            end_time: ISO format datetime string (optional)
        """
        try:
            bookings = self.square_client.bookings.list(
                start_at_min=start_at_min,
                start_at_max=start_at_max
            )

            
            response = [{
                'id': booking.id,
                'start_at': booking.start_at,
                'customer_id': booking.customer_id,
                'service_variation_id': booking.appointment_segments[0].service_variation_id if booking.appointment_segments is not None else None,
                'duration': booking.appointment_segments[0].duration_minutes if booking.appointment_segments is not None else None,
            } for booking in bookings]
            return response

        except Exception as e:
            raise Exception(f"Failed to list bookings: {str(e)}")
        

    async def create_booking(
        self,
        start_at: datetime,
        service_variation_id: str,
        service_variation_version: int,
        team_member_id: str,
        location_id: Optional[str] = None,
        customer_id: Optional[str] = None,
    ):
        try:
            assert self.barbershop_location_id is not None
            location_id = location_id if location_id else self.barbershop_location_id

            assert self.test_customer_id is not None
            customer_id = customer_id if customer_id else self.test_customer_id

            response =self.square_client.bookings.create(
                booking=BookingParams(
                    customer_id=customer_id,
                    location_id=location_id,
                    start_at=format_datetime_for_square(start_at),
                    appointment_segments=[
                        AppointmentSegmentParams(
                            service_variation_id=service_variation_id,
                            service_variation_version=service_variation_version,
                            team_member_id=team_member_id,
                        ),
                    ],
                )
            )
            if not response.booking:
                raise Exception(f"Call succeeded but booking is None, this is weird, {response}")
            
            return {
                'id': response.booking.id,
                'status': response.booking.status,
                'appointment_time': response.booking.start_at,
            }

        except Exception as e:
            raise Exception(f"Failed to create booking: {str(e)}")        


    async def search_availability(
        self,
        start_date: datetime,
        end_date: datetime,
        service_id: str,
        location_id: str,
        team_member_id: Optional[str] = None,
    ) -> List[Dict]:
        """
        Search for available time slots for a service.
        
        Args:
            service_id: The Square catalog service variation ID
            start_date: Start datetime (defaults to now)
            end_date: End datetime (defaults to 24 hours from start)
            team_member_id: Optional specific staff member ID
        """
        try:
            # Default to now if no start date provided
            if start_date < datetime.now():
                start_date = datetime.now()

            segment_filter_params = (
                SegmentFilterParams(service_variation_id=service_id) if not team_member_id
                else SegmentFilterParams(service_variation_id=service_id, team_member_id_filter=FilterValueParams(any=[team_member_id]))
            )
            query_filter = SearchAvailabilityFilterParams(
                start_at_range=TimeRangeParams(
                    start_at=format_datetime_for_square(start_date),
                    end_at=format_datetime_for_square(end_date),
                ),
                location_id=location_id,
                segment_filters=[segment_filter_params]
            )

            result = self.square_client.bookings.search_availability(query=SearchAvailabilityQueryParams(filter=query_filter))

            if result.availabilities is None:
                print(f"Error searching availability: {result.errors}")
                return []

            # Format the results
            formatted_slots = []
            for slot in result.availabilities:
                formatted_slot = {
                    'start_at': slot.start_at,
                    'location_id': slot.location_id,
                    'appointment_segments': []
                }
                
                # Add segments if they exist
                if slot.appointment_segments is None:
                    print(f"Error searching availability: {result.errors}")
                    return []

                for segment in slot.appointment_segments:
                    formatted_slot['appointment_segments'].append({
                        'service_variation_id': segment.service_variation_id,
                        'team_member_id': segment.team_member_id,
                        'duration_minutes': segment.duration_minutes
                    })
                
                formatted_slots.append(formatted_slot)
            return formatted_slots
        
        except Exception as e:
            print(f"Error in search_availability: {str(e)}")
            return []


    async def get_available_slots(
        self,
        service_id: str,
        start_date: datetime = datetime.now(),
        end_date: datetime = datetime.now() + timedelta(days=5),
        location_id: Optional[str] = None,
        team_member_id: Optional[str] = None,
    ) -> Dict[str, List[str]]:
        """
        Get available slots for the next 7 days, organized by date.
        """

        assert self.barbershop_location_id is not None
        location_id = location_id if location_id else self.barbershop_location_id
        slots = await self.search_availability(
            service_id=service_id,
            start_date=start_date,
            end_date=end_date,
            location_id=location_id,
            team_member_id=team_member_id
        )
        
        # Organize slots by date
        organized_slots = {}
        for slot in slots:
            slot_datetime = datetime.fromisoformat(slot['start_at'].replace('Z', '+00:00'))
            date_key = slot_datetime.strftime('%Y-%m-%d')
            time_str = slot_datetime.strftime('%I:%M %p')
            
            if date_key not in organized_slots:
                organized_slots[date_key] = []
            
            organized_slots[date_key].append(time_str)
        
        return organized_slots
    

    async def list_catalog(self) -> List[Dict[str, Any]]:
        """
        Get all Appointment Services
        """
        try:
            catalog = self.square_client.catalog.list()
            if catalog.items is None:
                return []
            
            appointment_services = []
            for item in catalog.items:
                if not isinstance(item, CatalogObjectItem):
                    continue
                item_data = item.item_data
                if item_data is None:
                    continue
                variations = item_data.variations
                if variations is None:
                    continue
                
                for variation in variations:
                    if not isinstance(variation, CatalogObjectItemVariation):
                        continue
                    variation_data = variation.item_variation_data
                    if variation_data is None:
                        continue
                    if variation_data.name != 'Regular':
                        continue
                    appointment_services.append({
                        'service_name': item_data.name,
                        'service_variation_id': variation.id,
                        'service_variation_version': variation.version,
                        'service_duration': variation_data.service_duration / 600 if variation_data.service_duration is not None else None,
                        'team_member_ids': variation_data.team_member_ids,
                    })
            return appointment_services

        except Exception as e:
            print(f"Error in list_catalog: {str(e)}")
            return []


def format_datetime_for_square(dt: datetime) -> str:
    """
    Format datetime object to RFC3339 format for Square API
    """
    if dt.tzinfo is None:
        # If datetime is naive, make it UTC
        dt = pytz.UTC.localize(dt)
    
    # Format to RFC3339 and ensure Z suffix for UTC
    return dt.isoformat().replace('+00:00', 'Z')


if __name__ == "__main__":
    dao = SquareBookingsDao()

    print("Going to get CRUDDY with Square API!!")
    print("=" * 50)

    bookings = asyncio.run(
        dao.list_bookings()
    )
    print(f"Available bookings: {bookings}\n\n")

    available_services = asyncio.run(
        dao.list_catalog()
    )
    chosen_service = random.choice(available_services)
    print(f"Out of available services: {available_services}\nChosen Service: {chosen_service}\n\n")

    available_slots = asyncio.run(
        dao.get_available_slots(
            service_id=chosen_service['service_variation_id'],
        )
    )
    chosen_day = random.choice(list(available_slots.keys()))
    chosen_time = random.choice(available_slots[chosen_day])
    print(f"Out of available slots: {available_slots}\nChosen Day & Time: {chosen_day} at {chosen_time}\n\n")

    created_booking = asyncio.run(
        dao.create_booking(
            start_at=datetime.strptime(f"{chosen_day} {chosen_time}", "%Y-%m-%d %I:%M %p"),
            service_variation_id=chosen_service['service_variation_id'],
            service_variation_version=chosen_service['service_variation_version'],
            team_member_id=chosen_service['team_member_ids'][0]
        )
    )
    print(f"Booking created! {created_booking}\n\n")

    bookings = asyncio.run(
        dao.list_bookings()
    )
    print(f"Updated available bookings: {bookings}\n\n")
    print("DEMO COMPLETE!")
    