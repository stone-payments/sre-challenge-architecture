# Tech Challenge 

* Configure o inventory.ini para o ip do server desejado

### Ambiente:
** Para subir o ambiente.
ansible-playbook -i inventory.ini playbook.yml

** Para limpar o ambiente.
ansible-playbook -i inventory.ini clean.yml