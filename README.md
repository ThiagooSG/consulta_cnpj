
# Consulta CNPJ 📊

## 🚀 Descrição

Este projeto foi desenvolvido para facilitar a consulta de informações relacionadas ao CNPJ de empresas no Brasil. Através da API da [receitaws](https://www.receitaws.com.br/), ele pode retornar informações detalhadas sobre a situação cadastral, adesão ao Simples Nacional e ao MEI, entre outros dados.
Nesse projeto é busco apenas situação da empresa, se optante ou não pelo simples ou mei e o e-mail do responsável cadastrado.

Além disso, ele permite que você faça a consulta de múltiplos CNPJs em uma planilha Excel e exporte os resultados para um novo arquivo.

## 🛠️ Requisitos para Funcionamento

### Ferramentas Necessárias
Sistema Operacional: Windows, macOS ou Linux.  
Editor de Texto/IDE: Visual Studio Code, PyCharm, ou qualquer outro editor de sua preferência.  
Python: Versão 3.x
## Instalação

### Dependências do Projeto

**requests   
pandas   
tkinter  
certifi  
openpyxl**

Para instalar todas as dependências necessárias, execute o seguinte comando:
```bash
    pip install requests pandas openpyxl certifi
```


## 💡 Uso

### Executar a Interface Gráfica

Para executar a interface gráfica, basta rodar o seguinte comando no terminal:

```bash
    python consulta_cnpj.py
```

### Consultar CNPJs a partir de uma Planilha Excel
- Clique no botão "Selecionar Planilha" e escolha a planilha de CNPJs (.xlsx). Para que a aplicação reconheça os CNPJs no arquivo, é necessario que os CNPJs estejam em uma coluna com nome CNPJ e eles podem estar com mascara 99.999.999/9999-99 ou sem 99999999999999.
- Escolha o local e o nome para salvar os resultados.
- O programa processará os CNPJs (sendo 3 consultas por minuto que é a limite da api pública) e salvará os resultados em um novo arquivo Excel.

### Consultar um único CNPJ na interface gráfica
- Insira o CNPJ no campo de entrada.
- Clique no botão "Consultar CNPJ".
- Algumas informações do CNPJ serão exibidas na interface gráfica.
## 🤝 Contribuição

Contribuições são sempre bem-vindas!

Se você deseja contribuir para este projeto, siga os seguintes passos:

### Faça um fork do repositório.

- Crie uma branch para sua feature:

```bash
git checkout -b feature/nova-feature
```
- Realize as alterações e commite as mudanças:

```bash
git commit -m 'Adicionar nova feature'
```
- Envie a branch para o repositório remoto:

```bash
git push origin feature/nova-feature
```
- Abra um Pull Request para revisão.

## 📬 Contato

Para mais informações ou dúvidas, entre em contato:

- [linkedin](https://www.linkedin.com/in/thiago-sg/)
