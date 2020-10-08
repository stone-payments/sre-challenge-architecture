# Tech Challenge 

## Ambiente:
### Configurar:
1. Configure o inventory.ini para o ip do server desejado

### Executar:
1. Para subir o ambiente.
  - ``` make run ```
  
2. Para limpar o ambiente.
  - ``` make clean ```

## Teste:
### Configurar:
Para configurar o ambiente de teste de carga,
Ajuste a variavel HOST no makefile, para o ip do servidor e execute o comando:
``` make test-up ```
### Get
1. Execute o comando para efetuar as requisições de get
``` make get ```
### Post
2. Execute o comando para efetuar as requisições de post
``` make post ```

### Tunning
1. Falhas de limite de conexões
   - Postgres:
     - Aumentar o max_connections, atualmente esta em 1000 ou migrar a solução de DB para SaaS.
     EX: AWS RDS
   - API:
     - Se a api, atingir o limite de arquivos abertos, pode subir uma terceira instancia da mesma,
     e adicionar esta nas configurações do Nginx.
   - Nginx:
     - O Suporte deste é bem alto, mas caso atingir, o melhor é levar esta para um load-balance SaaS
     Ex: AWS Elastic Load Balancing