import bcrypt

from database.db import execute

senha = bcrypt.hashpw(
    "admin123".encode(),
    bcrypt.gensalt()
).decode()

execute("""
INSERT INTO usuarios(usuario, senha)
VALUES(?,?)
""", ("admin", senha))

print("ADMIN CRIADO")