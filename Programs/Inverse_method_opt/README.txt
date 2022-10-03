# Passos para configurar o otimizador 

1) Extrair os arquivos do .rar em uma mesma pasta;

2) Abir prop_optm_fun.py e alterar:
	> linha 28 - Mudar o diretório onde o arquivo APDL_Und_Variables.txt está;
	> linha 40 - Mudar o diretório onde o executável do MAPDL está, o diretório de output e o diretório onde APDL_Undamaged.txt está;

3) Abrir o APDL_Undamaged.txt e alterar:
	> linha 21 - Alterar o diretório onde APDL_Und_Variables.txt está;
	> linha 371 - Alterar o diretório de output das frequências naturais;
	> linha 390 - ALterar o diretório de output dos modos de vibração (não será usado agora mas precisa ter um diretório válido para rodar);
	> linha 397 - Alterar o diretório dos outros outputs;
	
4) Abrir o arquivo prop_optm_final.py e alterar:
	> linha 22 - Mudar o valor das propriedades da estrutura para os valores medidos;
	> linha 99 - Mudar o número de iterações desejadas;
	
5) Rodar o arquivo prop_optm_final.py para iniciar a otimização;

6) O arquivo prop_optm_final.ipynb contém o notebook do projeto para fins didáticos;

7) FIM;

- Ian Viotti, 2022.