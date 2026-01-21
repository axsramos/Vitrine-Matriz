ALTER TABLE T_Usr ADD COLUMN UsrFto TEXT;

UPDATE T_Usr
SET UsrFto = (
    SELECT DevFto 
    FROM T_Dev 
    WHERE T_Dev.DevUsrCod = T_Usr.UsrCod
)
WHERE EXISTS (
    SELECT 1 
    FROM T_Dev 
    WHERE T_Dev.DevUsrCod = T_Usr.UsrCod
);
