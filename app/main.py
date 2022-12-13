import json
import logging
import os

import requests
from fastapi import FastAPI, Form, HTTPException
from fastapi_versioning import VersionedFastAPI, version

logger = logging.getLogger("uvicorn")

app = FastAPI(
    title="Ver Artis API",
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
)


@app.get("/")
@version(1)
def read_root():
    return {"application": "Ver Artis API"}


@app.post("/contactform")
@version(1)
def send_contact_form(
    first_name: str = Form(),
    last_name: str = Form(),
    email_address: str = Form(),
    message: str = Form(),
    hcaptcha_response: str = Form(alias="h-captcha-response"),
    origin: str = Form(alias="_origin"),
    next_on_success: str = Form(alias="_next_on_success"),
    next_on_failure: str = Form(alias="_next_on_failure"),
):
    # Prepare POST request to verify hCaptcha response with the API endpoint
    hcaptcha_url = "https://hcaptcha.com/siteverify"
    hcaptcha_data = {
        "response": hcaptcha_response,
        "secret": os.getenv("HCAPTCHA_SECRET_KEY"),
        "sitekey": os.getenv("HCAPTCHA_SITEKEY"),
    }
    hcaptcha_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # Prepare POST request to submit form
    formsubmit_url = "https://formsubmit.co/ajax/{}".format(
        os.getenv("FORMSUBMIT_STRING")
    )
    formsubmit_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email_address": email_address,
        "message": message,
        "_template": "box",
        "_captcha": "false",
    }
    formsubmit_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Origin": origin,
        "Referer": origin,
    }

    # Submit POST request to hCaptcha API endpoint
    response = requests.post(hcaptcha_url, data=hcaptcha_data, headers=hcaptcha_headers)
    hcaptcha_verification_response_json = response.json()

    # If hCaptcha is valid, actually submit form
    if hcaptcha_verification_response_json["success"]:
        response = requests.post(
            formsubmit_url, data=json.dumps(formsubmit_data), headers=formsubmit_headers
        )
        form_submission_response_json = response.json()
        logger.info("Form submission posted")
        logger.info(form_submission_response_json)
        location = next_on_success
    else:
        logger.error("hCaptcha verification failure")
        logger.error(hcaptcha_verification_response_json)
        location = next_on_failure

    # Return a 302 error to redirect client to specified location
    raise HTTPException(status_code=302, detail="Found", headers={"Location": location})


app = VersionedFastAPI(app, version_format="{major}", prefix_format="/v{major}")
