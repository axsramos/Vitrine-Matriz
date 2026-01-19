# Tipos de dados para SQLite
Tabela Resumo e Recomendação
| Se você quer armazenar... | Tipos que você pode declarar | Afinidade SQLite | Recomendação |
|---|---|---|---|
| Texto de qualquer tamanho | TEXT, VARCHAR(N), NVARCHAR | TEXT | TEXT |
| Números inteiros | INTEGER, INT, SMALLINT | INTEGER | INTEGER |
| Números com decimais | REAL, FLOAT, DOUBLE | REAL | REAL |
| Dados binários | BLOB | BLOB | BLOB |
| Um número (genérico) | NUMBER, DECIMAL | NUMERIC | Prefira INTEGER ou REAL |
