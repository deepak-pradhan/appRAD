from models.tenant import Tenant
from db.databases import engine
from datetime import datetime, timezone
from sqlmodel import SQLModel, create_engine, Session

def load_sample_tenants():
    with Session(engine) as db:
        sample_tenants = [
            {
                "name": "Acme Corp",
                "domain": "acme.com",
                "schema_name": "acme_schema",
                "max_users": 100,
                "subscription_plan": "Premium",
                "contact_email": "contact@acme.com",
                "logo_url": "https://acme.com/logo.png",
                "theme_color": "#FF0000",
                "billing_address": "123 Acme St, Acme City, AC 12345",
                # "subscription_start_date": datetime.now(timezone.utc),
                # "subscription_end_date": datetime.now(timezone.utc).replace(year=datetime.now().year + 1),
            },
            {
                "name": "Globex Corporation",
                "domain": "globex.com",
                "schema_name": "globex_schema",
                "max_users": 50,
                "subscription_plan": "Basic",
                "contact_email": "info@globex.com",
                "logo_url": "https://globex.com/logo.png",
                "theme_color": "#00FF00",
                "billing_address": "456 Globex Ave, Globex Town, GT 67890",
                # "subscription_start_date": datetime.now(timezone.utc),
                # "subscription_end_date": datetime.now(timezone.utc).replace(year=datetime.now().year + 1),
            }
        ]

        for tenant_data in sample_tenants:
            try:
                tenant = Tenant(**tenant_data, rec_type="tenant")
                tenant.generate_api_key()
                db.add(tenant)
                db.commit()
                print(f"Tenant created: {tenant.name}")
            except Exception as e:
                db.rollback()
                print(f"Error creating tenant: {e}")
                print(f"Tenant data: {tenant_data}")
                import traceback
                print(traceback.format_exc())

        print("Sample tenants loaded successfully.")
        print("Sample tenants loaded successfully.")