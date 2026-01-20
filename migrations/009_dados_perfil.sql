INSERT INTO T_Usr_Prf (PrfUsrCod, PrfFto, PrfCgo, PrfBio, PrfUrl)
SELECT 
    u.UsrCod,
    u.UsrFto,         -- Pega a foto que estava em T_Usr
    d.DevCgo,         -- Pega o cargo de T_Dev
    d.DevBio,         -- Pega a bio de T_Dev
    d.DevPgeUrl       -- Pega a url de T_Dev
FROM T_Usr u
LEFT JOIN T_Dev d ON d.DevUsrCod = u.UsrCod;