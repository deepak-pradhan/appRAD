from backend.models.tenant import Tenant
from backend.db.databases import engine
from datetime import datetime, timezone
from sqlmodel import Session
from faker import Faker
import random

def load_sample_tenants():
    fake = Faker()
    
    with Session(engine) as db:
        sample_tenants = []
        
        for _ in range(50):  # Create 10 sample tenants
            tenant_data = {
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.company_email(),
            }
            
            # Set subscription end date to 1 year from start date
            # start_date = tenant_data["subscription_start_date"]
            # tenant_data["subscription_end_date"] = start_date.replace(year=start_date.year + 1)
            
            sample_tenants.append(tenant_data)

        for tenant_data in sample_tenants:
            try:
                tenant = Tenant(**tenant_data, rec_type="tenant")
                tenant.generate_api_key()
                db.add(tenant)
                db.commit()
                print(f"Tenant created: {tenant.first_name}")
            except Exception as e:
                db.rollback()
                print(f"Error creating tenant: {e}")
                print(f"Tenant data: {tenant_data}")
                import traceback
                print(traceback.format_exc())

        print("Sample tenants loaded successfully.")