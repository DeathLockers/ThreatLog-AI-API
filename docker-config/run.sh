#!/bin/sh

sed -i '/JWT_SECRET_KEY=""/d' .env
jwt_secret_key="JWT_SECRET_KEY=$(openssl rand -hex 32)"
sed -i -e "11i$jwt_secret_key" .env
python -m app.db.migration