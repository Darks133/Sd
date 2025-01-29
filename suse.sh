#!/bin/bash

echo "🔹 Instalando Tryton y PostgreSQL en openSUSE..."

# 1️⃣ Instalar PostgreSQL y Tryton
sudo zypper refresh
sudo zypper install -y trytond trytond-modules-all postgresql-server

# 2️⃣ Iniciar y habilitar PostgreSQL y Tryton
sudo systemctl enable --now postgresql
sudo systemctl enable --now trytond

# 3️⃣ Configurar PostgreSQL (crear usuario y base de datos)
sudo -u postgres psql <<EOF
CREATE USER tryton WITH PASSWORD 'tryton123';
CREATE DATABASE tryton OWNER tryton;
GRANT ALL PRIVILEGES ON DATABASE tryton TO tryton;
EOF

echo "✅ Base de datos creada con éxito."

# 4️⃣ Permitir accesos remotos a PostgreSQL
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" /var/lib/pgsql/data/postgresql.conf

echo "host    all             all             0.0.0.0/0               md5" | sudo tee -a /var/lib/pgsql/data/pg_hba.conf

# 5️⃣ Configurar Tryton para aceptar conexiones en todas las IPs
sudo sed -i "s/listen = 127.0.0.1:8000/listen = 0.0.0.0:8000/" /etc/trytond.conf

# 6️⃣ Abrir el puerto 8000 en el firewall
sudo firewall-cmd --add-port=8000/tcp --permanent
sudo firewall-cmd --reload

# 7️⃣ Reiniciar servicios para aplicar cambios
sudo systemctl restart postgresql
sudo systemctl restart trytond

echo "✅ Tryton está instalado y accesible en la red local."
echo "🔹 Ahora puedes acceder desde otro equipo en: http://$(hostname -I | awk '{print $1}'):8000"
