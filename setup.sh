#!/bin/bash

# Install earthengine-api
pip install earthengine-api

# Authenticate with Earth Engine
earthengine authenticate --email $GEE_EMAIL --project $GEE_PROJECT 