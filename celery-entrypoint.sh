#!/bin/bash

celery -A favorite_products.main.celery worker
