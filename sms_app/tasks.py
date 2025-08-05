import requests
import os
import logging

from celery import shared_task
from .models import ExchangeRateLog

logger = logging.getLogger("exchange_rate")  # Use a specific logger name

@shared_task
def fetch_usd_to_bdt_rate():
    exchange_rate_api_url = os.environ.get('EXCHANGE_RATE_API_URL')
    logger.info("Starting fetch_usd_to_bdt_rate task")

    try:
        response = requests.get(exchange_rate_api_url)
        data = response.json()

        logger.info(f"API response: {data}")

        if data.get('result') != 'success':
            error_msg = f"API Error: {data.get('error-type', 'Unknown error')}"
            logger.warning(error_msg)
            return error_msg

        rate = data.get('conversion_rate')
        if rate is None:
            logger.warning("Conversion rate not found in API response")
            return "Conversion rate not found in API response"

        # Save to DB
        ExchangeRateLog.objects.create(
            base_currency='USD',
            target_currency='BDT',
            rate=rate
        )
        logger.info(f"Logged USD→BDT rate: {rate}")
        return f"Logged USD→BDT rate: {rate}"

    except Exception as e:
        logger.error(f"Exception occurred: {str(e)}")
        return f"Exception occurred: {str(e)}"

