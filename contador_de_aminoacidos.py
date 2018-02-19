# -*- coding: utf-8 -*-
import re
import os
import commands

def descobrir_tipo_de_aminoacido(aminoacidos):
	aminoacidos_e_seu_tipo = dict()
	ph = '0.102 0.502 0'
	ch = '0 0 0'
	for amino in aminoacidos:

		if amino[0:13]  == ph:
			ponte_de_hidrogenio = amino[45:-14].strip().strip('o\n').strip('(')
			aminoacidos_e_seu_tipo[ponte_de_hidrogenio] = 'PH'

		elif amino[0:5] == ch:
			contatos_hidrofobicos = amino[37:-13].strip().strip('o\n').strip('(').strip(')')
			aminoacidos_e_seu_tipo[contatos_hidrofobicos] = 'CH'
	return aminoacidos_e_seu_tipo

def encontre_aminoacidos_da_regex(nome_do_arquivo_ps):

	arquivo = open(nome_do_arquivo_ps, 'r')
	conteudo = arquivo.readlines()
	arquivo.close()
	regex = r'(0.102 0.502 0 setrgbcolor\n[0-9]{1,3}.[0-9]{1,3} [0-9]{1,3}.[0-9]{1,3} moveto\n\([A-z^bBfFjJkKKqQwWxXzZ]{3}[0-9]{2,3}\) [0-9]{1,2}.[0-9]{1,2} Center)|((0 0 0) setrgbcolor\n[0-9]{1,3}.[0-9]{1,3} [0-9]{1,3}.[0-9]{1,3} moveto\n\([A-z^bBfFjJkKKqQwWxXzZ]{3}[0-9]{2,3}\) [0-9]{1,2}.[0-9]{1,2} Center)'
	all_strings_do_arquivo_ps = ''.join(conteudo)
	results = re.finditer(regex, all_strings_do_arquivo_ps)
	aminoacidos = list()

	for result in results:
		aminoacidos.append(result.group())

	return aminoacidos

def procura_aminoacidos(nome_do_arquivo_ps):
	aminoacidos_da_regex = encontre_aminoacidos_da_regex(nome_do_arquivo_ps)
	aminoacidos_do_arquivo = descobrir_tipo_de_aminoacido(aminoacidos_da_regex)
	return aminoacidos_do_arquivo

def encontra_arquivos(caminho):

	aminoacidos_por_arquivo = dict()
	arquivos = commands.getoutput("ls " + caminho).split()

	for arquivo in arquivos:
		aminoacidos_por_arquivo[arquivo] = procura_aminoacidos(caminho + "/"+ arquivo)

	return aminoacidos_por_arquivo

def separar_as_sub_pastas(diretorio_raiz):

	aminoacidos_da_pasta = dict()

	pastas = commands.getoutput("ls " + diretorio_raiz).split()

	for pasta in pastas:
		aminoacidos_da_pasta[pasta] = encontra_arquivos(diretorio_raiz+pasta)

	return aminoacidos_da_pasta

def organizar_dados(diretorio_raiz, option):
	aminoacidos = []
	if option == 1:
		pastas_com_arquivos_ps = separar_as_sub_pastas(diretorio_raiz)
		for key_pasta in pastas_com_arquivos_ps:
			conteudo_da_pasta = pastas_com_arquivos_ps[key_pasta]
			for key_arquivo in conteudo_da_pasta:
				dados_do_arquivo = conteudo_da_pasta[key_arquivo]
				for key_resultado in dados_do_arquivo:
					aminoacidos.append(key_resultado + " " + dados_do_arquivo[key_resultado])
		return aminoacidos

def imprimir_dados(lista_de_dados):
	conta_frequencia= {x:lista_de_dados.count(x) for x in set(lista_de_dados)}
	for key in conta_frequencia:
		print "\t" + key + ": " + str(conta_frequencia[key]) + "\n"

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
		imprimir_dados(organizar_dados(diretorio_raiz, escolha))

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
	menu(diretorio_raiz)