# 1 - Monitorización

## Logs

- Modalidad reactiva:
    - Alerta de actividades sospechosas que requiren más investigación.
    - Dejan rastro de las actividades de un atacante.
    - Asisten en el caso de necesitar recuperar un servidor.
    - ...

- La frecuencia depende en:
    - La cantidad de tráfico que el servidor recibe.
    - Nivel general de riesgo (algunos servidores reciben más ataques que otros).
    - Amenazas específicas (en momentos específicos suceden algunos ataques que necesitan más análisis).
    - Vulnerabilidad del servidor.
    - Valor de los datos y servicios proporcionados por el servidor.


## Audit

En RedHat y similares viene instalado de serie. En Ubuntu:
```bash
sudo apt-get install auditd
```

Si queremos ver las reglas en efecto actualmente:
```bash
sudo auditctl -l
```

Para auditar el fichero `/etc/passwd` en caso de cambios:
```bash
sudo auditctl -w /etc/passwd -p wa -k passwd_changes
#             ______________       _________________
#             Watch this file      Log with key "passwd_changes"
```

Para buscar logs usar el comando `ausearch`:
```bash
sudo ausearch -k passwd_changes -i
```

Para hacer un reporte por tipos de evento:
```bash
sudo aureport -i -k
```

Y para hacer uno por cada evento:
```bash
sudo aureport -i
```

## Ejercicios clase

### Ejercicio 1
```bash
sudo useradd -m alice
sudo passwd alice
#> New password: <alicepass>
#> Retype new password: <alicepass>
sudo usermod -aG sudo alice
```

### Ejercicio 2
```bash
sudo touch /tmp/test.sh
sudo chmod ug+x /tmp/test.sh
```

### Ejercicio 3
```bash
sudo auditctl -a exit,always -F arch=b64 -F euid=0 -S execve -k rootcmd
sudo auditctl -a exit,always -F arch=b32 -F euid=0 -S execve -k rootcmd
```

### Ejercicio 4
Los comandos anteriores añaden una regla que se aplica a todos los eventos "exit" de llamadas al sistema, en arquitecturas archx32 y archx64, que se aplica a todos los comandos ejecutados por el usuario con ID 0. Las define ambas con la clave "rootcmd".

### Ejercicio 5
```bash
sudo grep alice /etc/passwd
```

### Ejercicio 6
```bash
ausearch -ua alice | grep passwd
#> type=EXECVE msg=audit(1632506982.404:245): argc=4 a0="sudo" a1="grep" a2="alice" a3="/etc/passwd"
```

### Ejercicio 7
Aquí podemos ver que se ha ejecutado una llamada al sistema en la que se ha ejecutado un comando con 4 argumentos: sudo, grep, alice y /etc/passwd.

### Ejercicio 8
```bash
sudo /tmp/test.sh foo bar
```

### Ejercicio 9
```bash
ausearch -ua alice | grep test
#> type=EXECVE msg=audit(1632507210.581:262): argc=4 a0="sudo" a1="/tmp/test.sh" a2="foo" a3="bar"
```
Aquí podemos ver que se ha ejecutado una llamada al sistema en la que se ha ejecutado un comando con 4 argumentos: sudo, /tmp/test.sh, foo y bar.
