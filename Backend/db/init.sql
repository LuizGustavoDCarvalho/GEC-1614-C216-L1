DROP TABLE IF EXISTS "vendas";
DROP TABLE IF EXISTS "Placas_de_video";

CREATE TABLE "Placas_de_video" (
    "id" SERIAL PRIMARY KEY,
    "Modelo" VARCHAR(255) NOT NULL,
    "Marca" VARCHAR(255) NOT NULL,
    "quantidade" INTEGER NOT NULL,
    "preco" FLOAT NOT NULL
);

CREATE TABLE "vendas" (
    "id" SERIAL PRIMARY KEY,
    "placa_id" INTEGER REFERENCES Placas_de_video(id) ON DELETE CASCADE,
    "quantidade_vendida" INTEGER NOT NULL,
    "valor_venda" FLOAT NOT NULL,
    "data_venda" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO "Placas_de_videos" ("Modelo", "Marca", "quantidade", "preco") VALUES ('RTX 3060Ti 12gb', 'Galax', 10, 1869.00);
INSERT INTO "Placas_de_video" ("Modelo", "Marca", "quantidade", "preco") VALUES ('RTX 4070 super 12gb', 'Gigabyte', 2, 3899.00);
INSERT INTO "Placas_de_video" ("Modelo", "Marca", "quantidade", "preco") VALUES ('RTX 4090 24gb Rog Strix', 'Asus', 3, 13999.00)