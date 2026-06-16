from __future__ import annotations

from uuid import uuid4

from src.models.user import User


class UserFactory:
    @staticmethod
    def build() -> User:
        unique = uuid4().hex[:10]
        return User(
            name=f"QA Lead {unique}",
            email=f"qa.lead.{unique}@example.com",
            password=f"QALead-{unique}-Pass1",
            title="Mr",
            birth_day="12",
            birth_month="6",
            birth_year="1990",
            first_name="QA",
            last_name=f"Lead{unique}",
            company="Hybrid QA Guild",
            address1=f"{unique} Automation Avenue",
            address2="Suite 42",
            country="United States",
            state="California",
            city="San Francisco",
            zipcode="94105",
            mobile_number="15551234567",
        )
