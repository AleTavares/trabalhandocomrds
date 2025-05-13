Murilo Miguel de Morais 6323525
🛠️ CRUD para Order Details (Northwind Database)
Este projeto implementa um sistema CRUD (Create, Read, Update, Delete) para a tabela order_details do banco de dados Northwind, utilizando Python, PostgreSQL e uma interface interativa com Streamlit.
📌 Funcionalidades
Este sistema permite:
- Criar (Create): Adicionar novos detalhes de pedidos ao banco.
- Ler (Read): Consultar detalhes de pedidos cadastrados.
- Atualizar (Update): Modificar informações de um pedido.
- Deletar (Delete): Remover um detalhe de pedido.

📂 Estrutura do Projeto
📁 projeto_crud
├── 📜 config.yml       # Arquivo de configuração do banco
├── 📜 crud.py          # Código do CRUD e interface Streamlit
├── 📜 requirements.txt # Lista de dependências
├── 📜 README.md        # Documentação do projeto



🚀 Passos para Executar o Projeto
1️⃣ Configuração do Banco de Dados
Antes de rodar o projeto, configure o arquivo config.yml com as credenciais do seu banco de dados PostgreSQL:
database:
  host: "SEU_HOST"
  user: "SEU_USUARIO"
  password: "SUA_SENHA"
  dbname: "northwind"
  port: 5432


🔹 Observação: O banco de dados Northwind precisa estar disponível e acessível para que as operações funcionem corretamente.

2️⃣ Instalar Dependências
Para garantir que todos os pacotes necessários estejam disponíveis, execute:
pip install -r requirements.txt


Isso instalará os pacotes Streamlit, psycopg2 e PyYAML.

3️⃣ Rodar a Aplicação
Para iniciar a interface interativa, execute:
streamlit run crud.py


Isso abrirá a interface no navegador, onde você pode gerenciar os detalhes dos pedidos.

🖥️ Interface do Streamlit
Quando a aplicação for iniciada, você verá um menu lateral com as opções:
🟢 Criar
Adicione um novo detalhe de pedido informando:
- ID do Pedido (order_id)
- ID do Produto (product_id)
- Preço Unitário (unit_price)
- Quantidade (quantity)
- Desconto (discount)

Após preencher os campos, clique em Adicionar para salvar no banco.

🔵 Ler
Esta seção exibe todos os detalhes de pedidos cadastrados no banco, com as seguintes informações:
- ID do Pedido
- ID do Produto
- Preço Unitário
- Quantidade
- Desconto


🟡 Atualizar
Permite modificar um detalhe de pedido já existente:
- Selecione um ID de Pedido.
- Escolha o ID do Produto dentro daquele pedido.
- Altere os valores de Preço Unitário, Quantidade ou Desconto.
- Clique em Atualizar para salvar a alteração.


🔴 Deletar
Para remover um detalhe de pedido, siga os passos:
- Selecione um ID de Pedido.
- Escolha o ID do Produto dentro do pedido.
- Clique em Deletar para excluir o registro.


✅ Contribuição
Se quiser contribuir com melhorias no projeto, siga estes passos:
- Faça um fork do repositório.
- Clone o projeto:git clone https://github.com/seu-usuario/projeto_crud.git

- Crie uma nova branch:git checkout -b minha-modificacao

- Faça as alterações e commit:git add .
git commit -m "Implementação da melhoria XYZ"

- Envie para o repositório:git push origin minha-modificacao

- Abra um Pull Request no GitHub.


📢 Observações Finais
✔️ Certifique-se de que o PostgreSQL está rodando e que as credenciais estão corretas.
✔️ A tabela order_details deve existir no banco de dados Northwind.
✔️ O projeto pode ser modificado para incluir mais funcionalidades conforme necessário.


