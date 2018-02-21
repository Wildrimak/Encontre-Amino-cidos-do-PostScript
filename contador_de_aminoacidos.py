# -*- coding: utf-8 -*-
import re
import os
import commands

def descobrir_aminoacido_e_seu_tipo(aminoacidos):

	aminoacidos_com_seu_tipo = []
	encontrar_tipo_do_aminoacido_no_paragrafo = r'(0 0 0)|(0.102 0.502 0)'
	encontra_aminoacido_no_paragrafo = r'(Asp[0-9]{1,5})|(Glu[0-9]{1,5})|(Ala[0-9]{1,5})|(Arg[0-9]{1,5})|(Asn[0-9]{1,5})|(Cys[0-9]{1,5})|(Phe[0-9]{1,5})|(Gly[0-9]{1,5})|(Gln[0-9]{1,5})|(His[0-9]{1,5})|(Ile[0-9]{1,5})|(Leu[0-9]{1,5})|(Lys[0-9]{1,5})|(Met[0-9]{1,5})|(Pyl[0-9]{1,5})|(Pro[0-9]{1,5})|(Ser[0-9]{1,5})|(Sec[0-9]{1,5})|(Tyr[0-9]{1,5})|(Thr[0-9]{1,5})|(Trp[0-9]{1,5})|(Val[0-9]{1,5})'
	transformar_vetor_de_amino_em_string = ' '.join(aminoacidos)
	resultado_de_aminoacidos = re.finditer(encontra_aminoacido_no_paragrafo, transformar_vetor_de_amino_em_string)
	resultado_dos_tipos = re.finditer(encontrar_tipo_do_aminoacido_no_paragrafo, transformar_vetor_de_amino_em_string)

	for result_amino, result_tipo in zip(resultado_de_aminoacidos, resultado_dos_tipos):

		if result_tipo.group() == '0 0 0':
			aminoacidos_com_seu_tipo.append(result_amino.group() + ' ' + 'CH')

		else:
			aminoacidos_com_seu_tipo.append(result_amino.group() + ' ' + 'PH')

	return aminoacidos_com_seu_tipo


def encontre_aminoacidos_da_regex(nome_do_arquivo_ps):

	arquivo = open(nome_do_arquivo_ps, 'r')
	conteudo = arquivo.readlines()
	arquivo.close()
	regex = r'(0.102 0.502 0 setrgbcolor\n[0-9]{1,3}.[0-9]{1,3} [0-9]{1,3}.[0-9]{1,3} moveto\n\([A-z^bBfFjJkKKqQwWxXzZ]{3}[0-9]{2,3}\) [0-9]{1,2}.[0-9]{1,2} Center)|((0 0 0) setrgbcolor\n[0-9]{1,3}.[0-9]{1,3} [0-9]{1,3}.[0-9]{1,3} moveto\n\([A-z^bBfFjJkKKqQwWxXzZ]{3}[0-9]{2,3}\) [0-9]{1,2}.[0-9]{1,2} Center)'
	#transforma vetor em string
	all_strings_do_arquivo_ps = ''.join(conteudo)
	results = re.finditer(regex, all_strings_do_arquivo_ps)
	aminoacidos = list()

	for result in results:
		aminoacidos.append(result.group())

	return aminoacidos

def procura_aminoacidos(nome_do_arquivo_ps):
	aminoacidos_da_regex = encontre_aminoacidos_da_regex(nome_do_arquivo_ps)
	aminoacidos_do_arquivo = descobrir_aminoacido_e_seu_tipo(aminoacidos_da_regex)
	return aminoacidos_do_arquivo

def encontra_arquivos(caminho):

	aminoacidos_por_arquivo = dict()
	arquivos = commands.getoutput("ls " + caminho).split()

	for arquivo in arquivos:
		aminoacidos_por_arquivo[arquivo] = procura_aminoacidos(caminho + "/"+ arquivo)

	return aminoacidos_por_arquivo

def encontrar_as_pastas_dentro_do_diretorio_raiz(diretorio_raiz):

	aminoacidos_da_pasta = dict()

	pastas = commands.getoutput("ls " + diretorio_raiz).split()

	for pasta in pastas:
		aminoacidos_da_pasta[pasta] = encontra_arquivos(diretorio_raiz+pasta)

	return aminoacidos_da_pasta


def contar_os_dados_e_imprimir(lista_de_dados):
	dicionario_de_pastas = lista_de_dados
	dicionario_de_aminoacidos_total = []

	for key_pasta in dicionario_de_pastas:
		dicionario_de_arquivos = dicionario_de_pastas[key_pasta]

		for key_arquivo in dicionario_de_arquivos:
			dicionario_de_aminoacidos = dicionario_de_arquivos[key_arquivo]

			for aminoacido in dicionario_de_aminoacidos:
				dicionario_de_aminoacidos_total.append(aminoacido)

	conta_frequencia= {x:dicionario_de_aminoacidos_total.count(x) for x in set(dicionario_de_aminoacidos_total)}

	for key in conta_frequencia:
		print "\t" + key + ": " + str(conta_frequencia[key])

def menu(diretorio_raiz):
	menu = "\n__________________________________MENU____________________________________________________\n"
	question_1 = "\t1) Exibir contagem total separando por contatos hidrofobicos e pontes de hidrogenio\n"
	question_2 = "\t2) Exibir o mesmo que a primeira questao só que por pasta\n"
	question_2_sub = "\t\tEscolha a pasta:\n"
	question_3 = "\t3) Mostrar dados por arquivo:\n"
	question_3_sub = "\t\tEscolha o arquivo\n:"
	selecao = "\nEscolha uma opcao:\n"
	escolha = input(menu+question_1+question_2+question_3+selecao)

	if escolha == 1:
		#contar_os_dados_e_imprimir(organizar_dados(diretorio_raiz, escolha))
		pass

	elif escolha == 2:
		sub_escolha = input(question_2_sub)
		print "Em contrucao...."
		#chamar uma funcao que exibe so por pasta
	elif escolha == 3:
		sub_escolha = input(question_2_sub)
		print "Em construcao tambem..."
		new_sub_escolha = input(question_3_sub)
		print "Em andamento...."


if __name__ == '__main__':
	diretorio_raiz = 'PostScriptVersion/'
	#menu(diretorio_raiz)
	contar_os_dados_e_imprimir(encontrar_as_pastas_dentro_do_diretorio_raiz(diretorio_raiz))