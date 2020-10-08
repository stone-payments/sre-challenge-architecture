# Tech Challenge 

## Ambiente:
### Configurar:
1 Configure o inventory.ini para o ip do server desejado

### Executar:
1 Para subir o ambiente.
  - ``` make run ```
  
2 Para limpar o ambiente.
  - ``` make clean ```

## Teste:
### Configurar:
Para configurar o ambiente de teste de carga,
Ajuste a variavel HOST no makefile, para o ip do servidor e execute o comando:
``` make test-up ```
### Get
1 Execute o comando para efetuar as requisições de get
``` make get ```
### Post
2 Execute o comando para efetuar as requisições de post
``` make post ```