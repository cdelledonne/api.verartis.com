import os

from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI, version
from pydantic import BaseModel, Field


class ContactForm(BaseModel):
    first_name: str
    last_name: str
    email_address: str
    message: str
    hcaptcha_response: str = Field(alias="h-captcha-response")
    template: str | None = Field(default=None, alias="_template")
    next: str | None = Field(default=None, alias="_next")
    captcha: str | None = Field(default=None, alias="_captcha")
    honey: str | None = Field(default=None, alias="_honey")


app = FastAPI()


@app.get("/")
@version(1)
def read_root():
    return {"application": "Ver Artis API"}


@app.post("/contactform")
@version(1)
def send_contact_form(form: ContactForm):
    secret_key = os.getenv("HCAPTCHA_SECRET_KEY")
    return form


app = VersionedFastAPI(app, version_format="{major}", prefix_format="/v{major}")
