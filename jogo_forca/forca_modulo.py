

def encaixar_letra(letra_esc: str, palavra_maquina: str, palavra_secreta: str) -> str:

    palavra_lista = list(palavra_secreta)

    for index, letra in enumerate(list(palavra_maquina)):
        if letra == letra_esc:
            palavra_lista[index] = letra_esc
    
    palavra_secreta = "".join(palavra_lista)

    return palavra_secreta