# -*- coding: utf-8 -*-
import re
import os
import commands

def descobrir_tipo_de_aminoacido(aminoacidos):
	aminoacidos_ch, aminoacidos_ph = list(), list()
	#verifica a cor
	#extrair aminoacido conforme sua cor
	ph = '0.102 0.502 0'
	ch = '0 0 0'
	for amino in aminoacidos:
		if amino[0:13]  == ph:
			#print "ponte de hidrogenio:\n" + amino
			ponte_de_hidrogenio = amino[45:-14].strip().strip('o\n').strip('(')
			aminoacidos_ph.append(ponte_de_hidrogenio)
		if amino[0:5] == ch:
			#print "contato hidrofobico\n" + amino
			pass
	#print aminoacidos_ph

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

	aminoacidos_por_arquivo = list()
	arquivos = commands.getoutput("ls " + caminho).split()

	for arquivo in arquivos:
		aminoacidos_por_arquivo.append(procura_aminoacidos(caminho + "/"+ arquivo))

	return aminoacidos_por_arquivo

def separar_as_sub_pastas(diretorio_raiz):

	aminoacidos_da_pasta = list()

	pastas = commands.getoutput("ls " + diretorio_raiz).split()

	for pasta in pastas:
		aminoacidos_da_pasta.append(encontra_arquivos(diretorio_raiz+pasta))

	print aminoacidos_da_pasta

if __name__ == '__main__':
	diretorio_raiz = 'PostScriptVersion/'
	separar_as_sub_pastas(diretorio_raiz)