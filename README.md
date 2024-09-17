## Dashboard de Chamados

Durante meu estágio em Desenvolvimento, construí este Dashboard em Python utilizando a biblioteca Dash, para analisar dados de chamados de um sistema de registros de ponto, incluindo informações sobre categorias de chamados, plataformas, resoluções e datas de abertura.

### Funcionalidades

O dashboard possui as seguintes funcionalidades:

1. **Filtragem de Dados**: Os usuários podem filtrar os dados por categoria e plataforma de chamado.
2. **Visualização de Totais**: Exibe o número total de chamados, chamados resolvidos e chamados não resolvidos.
3. **Gráficos Interativos**: Fornece gráficos interativos para visualização dos dados, incluindo gráficos de pizza, histogramas e gráficos de linha.

### Como Utilizar

Para utilizar o dashboard, siga os seguintes passos:

1. **Instalação de Dependências**: Certifique-se de ter todas as bibliotecas necessárias instaladas. Você pode instalá-las utilizando o comando `pip install -r requirements.txt`.
2. **Execução do Código**: Execute o código Python fornecido no arquivo `dashboard.py`.
3. **Interagindo com o Dashboard**: Após executar o código, abra um navegador da web e acesse o endereço fornecido no console. Você poderá interagir com os filtros e visualizar os gráficos e totais atualizados conforme as seleções feitas.



### Estrutura do Código

O código está organizado da seguinte forma:

- **Importação de Bibliotecas**: Importa as bibliotecas necessárias, incluindo Pandas, Dash e Plotly Express.
- **Carregamento e Preparação dos Dados**: Carrega os dados de chamados de um arquivo CSV e realiza algumas transformações, como conversão de datas e mapeamento de meses em português.
- **Definição do Layout do Aplicativo**: Define a estrutura e o layout do dashboard utilizando HTML e componentes Dash.
- **Callbacks**: Define as funções de callback que são executadas quando eventos específicos ocorrem, como cliques em botões ou alterações em seleções de filtro.
- **Estilos CSS**: Define os estilos CSS para personalização da aparência do dashboard.

### Requisitos

- Python 3.x
- Bibliotecas: Pandas, Dash, Plotly

***
Para mais informações sobre como utilizar o Dash, consulte a [documentação oficial](https://dash.plotly.com/).
***

