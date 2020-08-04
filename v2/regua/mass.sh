#!/usr/bin/env zsh
(time python buscas.py "BL" regua1.txt) 1>> relatorio1.txt 2>> tempo.txt
(time python buscas.py "BP" regua1.txt) 1>> relatorio1.txt 2>> tempo.txt
(time python buscas.py "BPL" regua1.txt) 1>> relatorio1.txt 2>> tempo.txt
(time python buscas.py "BPI" regua1.txt) 1>> relatorio1.txt 2>> tempo.txt
(time python buscas.py "BCU" regua1.txt) 1>> relatorio1.txt 2>> tempo.txt
(time python buscas.py "A*" regua1.txt) 1>> relatorio1.txt 2>> tempo.txt
(time python buscas.py "IDA*" regua1.txt) 1>> relatorio1.txt 2>> tempo.txt

(time python buscas.py "BL" regua2.txt) 1>> relatorio2.txt 2>> tempo.txt
(time python buscas.py "BP" regua2.txt) 1>> relatorio2.txt 2>> tempo.txt
(time python buscas.py "BPL" regua2.txt) 1>> relatorio2.txt 2>> tempo.txt
(time python buscas.py "BPI" regua2.txt) 1>> relatorio2.txt 2>> tempo.txt
(time python buscas.py "BCU" regua2.txt) 1>> relatorio2.txt 2>> tempo.txt
(time python buscas.py "A*" regua2.txt) 1>> relatorio2.txt 2>> tempo.txt
(time python buscas.py "IDA*" regua2.txt) 1>> relatorio2.txt 2>> tempo.txt

(time python buscas.py "BL" regua3.txt) 1>> relatorio3.txt 2>> tempo.txt
(time python buscas.py "BP" regua3.txt) 1>> relatorio3.txt 2>> tempo.txt
(time python buscas.py "BPL" regua3.txt) 1>> relatorio3.txt 2>> tempo.txt
(time python buscas.py "BPI" regua3.txt) 1>> relatorio3.txt 2>> tempo.txt
(time python buscas.py "BCU" regua3.txt) 1>> relatorio3.txt 2>> tempo.txt
(time python buscas.py "A*" regua3.txt) 1>> relatorio3.txt 2>> tempo.txt
(time python buscas.py "IDA*" regua3.txt) 1>> relatorio3.txt 2>> tempo.txt
