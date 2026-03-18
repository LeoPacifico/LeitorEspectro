from math import sumprod
from os.path import exists
import re
from statistics import mean

dados,energia, frequencia,EF,frequenciaRelativa=[],[],[],[],[]

print("LAB ESPECTRO - VERSÃ0 01.2026 \nDesenvolvido por: Leonardo Pacífico leonardo.pacifico@uerj.br\n*****************************")

if not exists("config.txt"):
    with open("config.txt","w") as f:
        A=-0.0210622
        B=0.134655
        f.write(f'VALORES DE REFERÊNCIA \n ALTERE-OS CASO NECESSÁRIOS \n Curva de calibração: \n A = {A}; B = {B}')
        f.close()
    print("Arquivo config.txt criado com sucesso! \nRode novamente o progrma")
else:
    print("COLOQUE O ARQUIVO espectro.txt NA MESMA PASTA DO ARQUIVO MAIN")
    padraoA=r"-0\.0\d+"
    padraoB=r"0\.1\d+"
    with open("config.txt","r") as f:
        arquivo = f.read()
        A=re.findall(padraoA,arquivo)
        B=re.findall(padraoB,arquivo)
        print(f'Coeficiente de calibração \nValor de A = {A[0]}; Valor de B = {B[0]}')
        print("VALORES DE REFERÊNCIA. ALTERE-OS CASO NECESSÁRIOS NO ARQUIVO config.txt\n**********************************")
        f.close()

    #Abrindo arquivo do espectro - .txt
    if not exists("espectro.txt"):
        print("Arquivo espectro.txt não encontrado ou nomeado errado!")
        input("Pressione ENTER para sair...")
    else:
        with open("espectro.txt","r") as f:
            f.seek(233)
            dados=[i.split() for i in f if i.strip()]
        #Separando energia e frequencia
        energia=[float(A[0])+float(dados[i][0])*float(B[0]) for i in range(len(dados))]
        frequencia=[float(dados[i][1]) for i in range(len(dados))]
        frequenciaRelativa=[energia[i]*frequencia[i]/sum(frequencia) for i in range(len(dados))]

        #FWHM
        VALOR_MEIA_ALTURA=int(max(frequencia)/2)
        #print(f'Valor máximo a meia altura de frequência = {VALOR_MEIA_ALTURA}')

        amplitude=[]
        for i in range(len(dados)):
            if int(dados[i][1]) < int(1.05*VALOR_MEIA_ALTURA) and int(dados[i][1]) > int(0.95*VALOR_MEIA_ALTURA):
                #print(f'Energia {energia[i]}')
                amplitude.append(energia[i])
                print(amplitude)
        #Achando energia máxima
        aux=[]
        for i in range(len(dados)):
            if int(dados[i][1]) <6 and int(dados[i][0]) > 300:
                if len(aux) < 20:
                    aux.append(float(A[0]) + float(dados[i][0]) * float(B[0]))
                    #print(f'Frequencia: {dados[i][1]} ; energia {float(A[0]) + float(dados[i][0]) * float(B[0])}')

        #Alternativa
        # x_canal=[dados[i][0] for i in range(len(dados)) if  (int(dados[i][1])>=0 and int(dados[i][1])<5)]
        # print(x_canal)
        # print(len(x_canal))
        # x_energia=[float(A[0]) + float(x_canal[i]) * float(B[0]) for i in range(len(x_canal))]
        # print(x_energia)

        energiaMaxima=mean(aux)
        #Resultados
        print("RESULTADOS:")
        energia_media_espectral=round(sumprod(energia,frequenciaRelativa)/sum(frequenciaRelativa),1)
        print(f'Energia média espectral= {energia_media_espectral} keV')
        print(f'Energia mais frequente: {round(energia[frequenciaRelativa.index(max(frequenciaRelativa))],1)} keV')
        print(f'Energia máxima: {round(energiaMaxima, 1)} keV')
        if amplitude==[]:
            print("Não foi possível calcular FWHM. Este erro é mais comum para 120 kV, onde FWM refere-se ao maior pico." )
        else:
            print(f'FWHM {round((max(amplitude)-min(amplitude)),1)} keV')
            print(f'FWHM (%) {round(100*(max(amplitude)-min(amplitude))/energia_media_espectral,1)}')
        input("\nProcessamento concluído. Pressione ENTER para sair...")
